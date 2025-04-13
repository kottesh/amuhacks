import { defineStore } from 'pinia';
import { ref } from 'vue';
import { apiClient } from '@/stores/authStore'; // Adjust path if needed

export const useDataStore = defineStore('data', () => {
  // --- State ---
  const accounts = ref([]);
  const recentTransactions = ref([]);
  const isLoading = ref(false);
  const error = ref(null);

  // --- Actions ---

  // Fetch all accounts for the user
  async function fetchAccounts() {
    console.log("Attempting to fetch accounts..."); // Log start
    try {
      // Use the correctly imported apiClient
      const response = await apiClient.get('/accounts/'); // GET /api/v1/accounts/
      console.log("API Response for /accounts/:", response); // Log raw response
      // Ensure response.data is an array before assigning
      if (Array.isArray(response.data)) {
          accounts.value = response.data;
          console.log("Accounts state updated in store:", accounts.value); // Log updated state
      } else {
          console.warn("/accounts/ endpoint did not return an array. Data:", response.data);
          accounts.value = []; // Reset to empty array if data format is wrong
          error.value = "Received invalid data format for accounts."; // Set specific error
      }
    } catch (err) {
      console.error('Failed to fetch accounts (dataStore):', err);
      const detail = err.response?.data?.detail;
      error.value = typeof detail === 'object' ? JSON.stringify(detail) : (detail || err.message || 'Failed to fetch accounts');
      accounts.value = [];
      throw err; // Re-throw error so Promise.all can catch it
    }
  }

  // Fetch the most recent transactions
  async function fetchRecentTransactions(limit = 30) {
    console.log("Attempting to fetch recent transactions...");
    try {
       // Use the correctly imported apiClient
      const response = await apiClient.get('/transactions/', { params: { limit } }); // GET /api/v1/transactions/?limit=30
       console.log("API Response for /transactions/ (recent):", response);
       if (Array.isArray(response.data)) {
           recentTransactions.value = response.data;
           console.log("Recent transactions state updated:", recentTransactions.value);
       } else {
            console.warn("/transactions/ endpoint did not return an array for recent tx. Data:", response.data);
            recentTransactions.value = [];
            error.value = "Received invalid data format for recent transactions.";
       }
    } catch (err) {
      console.error('Failed to fetch recent transactions (dataStore):', err);
      const detail = err.response?.data?.detail;
      error.value = typeof detail === 'object' ? JSON.stringify(detail) : (detail || err.message || 'Failed to fetch recent transactions');
      recentTransactions.value = [];
       throw err; // Re-throw error
    }
  }

  // Fetch transactions for a specific period
  async function fetchTransactionsForPeriod(startDate, endDate) {
     console.log(`Attempting to fetch transactions for period: ${startDate} to ${endDate}`);
    try {
       // Use the correctly imported apiClient
      const response = await apiClient.get('/transactions/', {
        params: { start_date: startDate, end_date: endDate, limit: 1000 }
      });
       console.log("API Response for /transactions/ (period):", response);
       if (Array.isArray(response.data)) {
            return response.data; // Return the fetched data
       } else {
            console.warn("/transactions/ endpoint did not return an array for period tx. Data:", response.data);
            error.value = "Received invalid data format for period transactions.";
            return []; // Return empty array on format error
       }
    } catch (err) {
      console.error('Failed to fetch transactions for period (dataStore):', err);
      const detail = err.response?.data?.detail;
      error.value = typeof detail === 'object' ? JSON.stringify(detail) : (detail || err.message || 'Failed to fetch transactions for period');
       throw err; // Re-throw error
    }
  }

  // Create a new account
  async function createAccount(accountData) {
      isLoading.value = true; error.value = null;
      try {
           // Use the correctly imported apiClient
          const response = await apiClient.post('/accounts/', accountData);
          await fetchAccounts(); // Re-fetch accounts after creation
          return response.data;
      } catch (err) {
          console.error('Failed to create account (dataStore):', err);
          const detail = err.response?.data?.detail;
          error.value = typeof detail === 'object' ? JSON.stringify(detail) : (detail || err.message || 'Failed to create account');
          throw err;
      } finally { isLoading.value = false; }
  }

   // Create a new transaction
  async function createTransaction(transactionData) {
       isLoading.value = true; error.value = null;
       try {
            // Use the correctly imported apiClient
           const response = await apiClient.post('/transactions/', transactionData);
           // Re-fetch recent transactions AND accounts after creation
           await Promise.all([
               fetchRecentTransactions(),
               fetchAccounts()
           ]);
           return response.data;
       } catch (err) {
           console.error('Failed to create transaction (dataStore):', err);
           const detail = err.response?.data?.detail;
           error.value = typeof detail === 'object' ? JSON.stringify(detail) : (detail || err.message || 'Failed to create transaction');
           throw err;
       } finally { isLoading.value = false; }
   }

  // Action to clear data
  function clearData() {
      accounts.value = [];
      recentTransactions.value = [];
      error.value = null;
      isLoading.value = false; // Ensure loading is reset
      console.log("Data store cleared.");
   }

  // --- Return Store API ---
  // Ensure all needed state and actions are returned
  return {
    // State
    accounts,
    recentTransactions,
    isLoading,
    error,
    // Actions
    fetchAccounts,
    fetchRecentTransactions,
    fetchTransactionsForPeriod,
    createAccount,
    createTransaction,
    clearData,
  };

});
