import httpx
import json
import logging
from datetime import date
from typing import List, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from core.config import settings
from schemas import NlpParsedTransaction, TransactionType

OLLAMA_BASE_URL = str(settings.OLLAMA_API_URL)
OLLAMA_MODEL = settings.OLLAMA_MODEL

# Prompt
PROMPT_TEMPLATE = """
You are an expert financial assistant. Extract all financial transaction details from the following text.

Respond ONLY with a valid JSON array of transaction objects.  If there are multiple transactions, include them all as separate objects in the array.  If there are no transactions, return an empty array.
Each transaction object should contain:
- "amount": (float, required, positive number) The transaction amount.
- "type": (string, required, must be exactly "INCOME" or "EXPENSE") The type of transaction.
- "category": (string, optional) A relevant category (e.g., "Groceries", "Salary", "Dining", "Transport", "Utilities", "Shopping", "Travel", "Entertainment", "Gift", "Freelance", "Rent/Mortgage", "Healthcare", "Education", "Investment", "Other Income", "Other Expense"). If unsure, use "Other Expense" or "Other Income".
- "description": (string, optional) A brief description or merchant name if identifiable.
- "date": (string, format=%Y-%m-%d) The date of the transaction if mentioned, otherwise use current the date.

Rules:
- Infer the 'type' based on keywords (e.g., "spent", "paid", "bought" -> EXPENSE; "received", "got", "salary" -> INCOME).
- If currency symbols (e.g., $, £, €, INR, ₹, USD) are present, ignore them for the 'amount'. Return only the numerical value.
- Extract merchant names or purpose into 'description'.
- If no category is clear, use "Other Expense" or "Other Income" respectively.
- **Crucially:  Identify *all* distinct transactions in the text.  Do not omit any.**
- Respond *only* with the JSON array, no explanations or surrounding text.

Assume the currency is INR unless otherwise specified. Today's date is {current_date}.

Text: "{user_input}"

JSON Output:
"""

KNOWN_CATEGORIES = [
    "Groceries", "Dining", "Transport", "Utilities", "Rent/Mortgage",
    "Salary", "Freelance", "Gift", "Shopping", "Entertainment", "Travel",
    "Healthcare", "Education", "Investment", "Other Income", "Other Expense"
]

async def parse_transaction_nlp(text: str, currency: str = "INR") -> List[NlpParsedTransaction] | None:
    """
    Sends text to Ollama for parsing into structured transactions.
    Handles lists and single transactions, with improved prompt for multiple transaction extraction.
    """
    prompt = PROMPT_TEMPLATE.format(
        user_input=text,
        currency=currency,
        current_date=date.today().isoformat()
    )

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "format": "json",
        "stream": False
    }

    json_string = "[]"
    try:
        logger.info(f"Sending text to Ollama for parsing. Model: {OLLAMA_MODEL}")
        async with httpx.AsyncClient(timeout=httpx.Timeout(None)) as client:
            response = await client.post(f"{OLLAMA_BASE_URL}api/generate", json=payload)
            logger.debug(f"Ollama raw response status: {response.status_code}")
            response.raise_for_status()

            response_data = response.json()
            logger.debug(f"Ollama raw response data: {response_data}")
            json_string = response_data.get("response", "[]")

            if json_string.startswith("```json"):
                json_string = json_string[7:]
            if json_string.endswith("```"):
                json_string = json_string[:-3]
            json_string = json_string.strip()

            if not json_string:
                logger.warning("Ollama returned an empty response string.")
                return []

            logger.debug(f"Cleaned JSON string from Ollama: {json_string}")

            try:
                parsed_data = json.loads(json_string)
                # Check if the response has a "transactions" key
                if "transactions" in parsed_data and isinstance(parsed_data["transactions"], list):
                    parsed_data_list = parsed_data["transactions"]
                elif isinstance(parsed_data, list):
                    parsed_data_list = parsed_data
                else:
                    parsed_data_list = [parsed_data]
            except json.JSONDecodeError as e:
                logger.error(f"Failed to decode JSON response from Ollama: {e}", exc_info=True)
                logger.error(f"Raw response string causing error: {json_string}")
                return None

            validated_transactions: List[NlpParsedTransaction] = []
            for parsed_data in parsed_data_list:
                try:
                    validated_transaction = NlpParsedTransaction(**parsed_data)
                    logger.info(f"Validated NLP result: {validated_transaction}")
                    validated_transactions.append(validated_transaction)
                except Exception as e:
                    logger.error(f"Validation error for a transaction: {e}", exc_info=True)
                    logger.error(f"Data causing validation error: {parsed_data}")

            return validated_transactions

    except httpx.RequestError as e:
        logger.error(f"HTTP request error contacting Ollama at {OLLAMA_BASE_URL}: {e}", exc_info=True)
        return None
    except httpx.HTTPStatusError as e:
        logger.error(f"Ollama request failed with status {e.response.status_code}: {e.response.text}",
                     exc_info=True)
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return None
