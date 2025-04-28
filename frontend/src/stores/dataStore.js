import { defineStore } from 'pinia'
import { ref, reactive } from 'vue'
import { apiClient } from '@/stores/authStore' // Adjust path as needed
import dayjs from 'dayjs'
import utc from 'dayjs/plugin/utc'
import FilteredTransactions from '@/components/FilteredTransactions.vue'

dayjs.extend(utc)

export const useDataStore = defineStore('data', () => {
  const accounts = ref([])
  const recentTransactions = ref([]) // Used for the main transaction list
  const filteredTransactions = ref([]) // Holds transactions for the filtered list
  const chartTransactions = ref([]) // Holds transactions for the last 7 days chart
  const parsedTransactions = ref([]) // Holds results from /parse endpoint

  const isLoading = ref(false) // General loading (primarily for initial load & accounts)
  const isLoadingChart = ref(false) // Specific loading for chart data
  const isLoadingParse = ref(false) // Specific loading for NLP parsing

  const error = ref(null) // General error state

  async function fetchAccounts() {
    console.log('Attempting to fetch accounts...')
    isLoading.value = true // Use general loading for account fetch
    error.value = null
    try {
      const response = await apiClient.get('/accounts/')
      console.log('API Response for /accounts/:', response)
      if (Array.isArray(response.data)) {
        accounts.value = response.data
        console.log('Accounts state updated in store:', accounts.value)
      } else {
        console.warn('/accounts/ endpoint did not return an array. Data:', response.data)
        accounts.value = []
        error.value = 'Received invalid data format for accounts.'
      }
    } catch (err) {
      console.error('Failed to fetch accounts (dataStore):', err)
      const detail = err.response?.data?.detail
      error.value =
        typeof detail === 'object'
          ? JSON.stringify(detail)
          : detail || err.message || 'Failed to fetch accounts'
      accounts.value = []
    } finally {
      isLoading.value = false // Turn off general loading
    }
  }

  async function fetchRecentTransactions(limit = 30) {
    console.log('Attempting to fetch recent transactions...')
    error.value = null // Clear previous errors before fetch
    try {
      const response = await apiClient.get('/transactions/', {
        params: { limit, sort: '-transaction_date' },
      })
      console.log('API Response for /transactions/ (recent):', response)
      if (Array.isArray(response.data)) {
        //recentTransactions.value = response.data
        recentTransactions.value = response.data
        recentTransactions.value.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
        console.log('Recent transactions state updated:', recentTransactions.value)
      } else {
        console.warn(
          '/transactions/ endpoint did not return an array for recent tx. Data:',
          response.data,
        )
        recentTransactions.value = []
        error.value = 'Received invalid data format for recent transactions.'
      }
    } catch (err) {
      console.error('Failed to fetch recent transactions (dataStore):', err)
      const detail = err.response?.data?.detail
      error.value =
        typeof detail === 'object'
          ? JSON.stringify(detail)
          : detail || err.message || 'Failed to fetch recent transactions'
      recentTransactions.value = []
    }
  }

  async function fetchChartData() {
    console.log('Attempting to fetch chart transactions...')
    isLoadingChart.value = true
    error.value = null
    chartTransactions.value = []

    const endDate = dayjs.utc().endOf('day').format('YYYY-MM-DD')
    const startDate = dayjs.utc().subtract(6, 'day').startOf('day').format('YYYY-MM-DD')

    try {
      const response = await apiClient.get('/transactions/', {
        params: { start_date: startDate, end_date: endDate, limit: 1000 }, // <-- Uncommented this line
      })
      console.log('API Response for /transactions/ (chart period):', response)
      if (Array.isArray(response.data)) {
        chartTransactions.value = response.data
        console.log('Chart transactions state updated:', chartTransactions.value)
      } else {
        console.warn(
          '/transactions/ endpoint did not return an array for chart tx. Data:',
          response.data,
        )
        error.value = 'Received invalid data format for chart transactions.'
      }
    } catch (err) {
      console.error('Failed to fetch chart transactions (dataStore):', err)
      const detail = err.response?.data?.detail
      error.value =
        typeof detail === 'object'
          ? JSON.stringify(detail)
          : detail || err.message || 'Failed to fetch chart data'
    } finally {
      isLoadingChart.value = false
    }
  }

  async function fetchTransactionsByDateRange(startDate, endDate) {
    console.log(`Attempting to fetch transactions between ${startDate} and ${endDate}...`);
    isLoading.value = true; // Use general loading for this fetch
    error.value = null;
    filteredTransactions.value = []; // Clear previous results

    try {
      const response = await apiClient.get('/transactions/', {
        params: { start_date: startDate, end_date: endDate, limit: 1000 },
      });
      console.log('API Response for /transactions/ (date range):', response);
      if (Array.isArray(response.data)) {
        filteredTransactions.value = response.data;
        console.log('Filtered transactions state updated:', filteredTransactions.value);
      } else {
        console.warn(
          '/transactions/ endpoint did not return an array for date range tx. Data:',
          response.data,
        );
        error.value = 'Received invalid data format for filtered transactions.';
      }
    } catch (err) {
      console.error('Failed to fetch transactions by date range (dataStore):', err);
      const detail = err.response?.data?.detail;
      error.value =
        typeof detail === 'object'
          ? JSON.stringify(detail)
          : detail || err.message || 'Failed to fetch filtered transactions';
    } finally {
      isLoading.value = false; // Turn off general loading
    }
  }

  async function fetchInitialData() {
    isLoading.value = true
    error.value = null
    console.log('Fetching initial dashboard data...')
    try {
      await Promise.all([fetchAccounts(), fetchRecentTransactions(), fetchChartData()])
      console.log('Initial data fetch complete.')
    } catch (err) {
      // Errors are caught and handled within individual fetch functions,
      // setting the main error state if needed. Promise.all might still reject
      // if an error is re-thrown, but we handle errors internally.
      console.error('Error during initial data fetch (Promise.all):', err)
      if (!error.value) {
        error.value = 'An error occurred while loading dashboard data.'
      }
    } finally {
      isLoading.value = false
    }
  }

  async function addAccount(accountData) {
    isLoading.value = true
    error.value = null
    let success = false
    try {
      const response = await apiClient.post('/accounts/', accountData)
      await fetchAccounts() // Re-fetch accounts after successful creation
      console.log('Account created successfully:', response.data)
      success = true
    } catch (err) {
      console.error('Failed to create account (dataStore):', err)
      const detail = err.response?.data?.detail
      error.value =
        typeof detail === 'object'
          ? JSON.stringify(detail)
          : detail || err.message || 'Failed to create account'
      success = false
    } finally {
      isLoading.value = false
    }
    return success
  }

  async function parseTransactionsNLP(text) {
    isLoadingParse.value = true
    error.value = null
    parsedTransactions.value = []
    let success = false

    try {
      const response = await apiClient.post('/transactions/parse', { text })
      console.log('API Response for /parse:', response)
      if (Array.isArray(response.data) && response.data.length > 0) {
        console.log(response.data)
        parsedTransactions.value = response.data.map((tx, index) => ({
          ...tx,
          date: tx.date ? tx.date.split('T')[0] : '',
          tempId: Date.now() + index, // Unique temporary ID for v-for key
          account_id: '', // Add account_id field, initially empty
          isSaving: false, // Flag for individual save loading state
          saveError: null, // Error message specific to this item's save attempt
        }))
        console.log('Parsed transactions updated:', parsedTransactions.value)
        success = true
      } else if (Array.isArray(response.data) && response.data.length === 0) {
        console.log('NLP parsing returned an empty array.')
        error.value = 'No transactions found in the text.' // More specific feedback
        success = false
      } else {
        console.warn('/parse endpoint did not return an array. Data:', response.data)
        error.value = 'Received invalid data format from parsing service.'
        success = false
      }
    } catch (err) {
      console.error('Failed to parse NLP transactions (dataStore):', err)
      const detail = err.response?.data?.detail
      error.value =
        typeof detail === 'object'
          ? JSON.stringify(detail)
          : detail || err.message || 'Failed to parse transactions'
      parsedTransactions.value = []
      success = false
    } finally {
      isLoadingParse.value = false
    }
    return success
  }

  async function createTransaction(transactionData) {
    error.value = null
    let success = false
    try {
      const response = await apiClient.post('/transactions/', transactionData)
      console.log('Transaction created successfully:', response.data)
      await Promise.all([
        fetchRecentTransactions(), // Update the list
        fetchAccounts(), // Update account balances shown in cards/dropdowns
        fetchChartData(), // Update chart data
      ])
      success = true
    } catch (err) {
      console.error('Failed to create transaction (dataStore):', err)
      const detail = err.response?.data?.detail
      // Set the general error state; the component reads this for the specific item
      error.value =
        typeof detail === 'object'
          ? JSON.stringify(detail)
          : detail || err.message || 'Failed to save transaction'
      success = false
    }
    // No general isLoading management here
    return success
  }

  // --- Actions for Managing Parsed Transactions UI State ---

  /** Clears the list of parsed transactions. */
  function clearParsedTransactions() {
    parsedTransactions.value = []
    console.log('Parsed transactions cleared.')
  }

  /** Removes a transaction from the parsed list by index. */
  function removeParsedTransaction(index) {
    if (index >= 0 && index < parsedTransactions.value.length) {
      parsedTransactions.value.splice(index, 1)
      console.log(`Removed parsed transaction at index ${index}.`)
    }
  }

  /** Updates status flags (isSaving, saveError) on a specific parsed transaction. */
  function setParsedTransactionStatus(index, { isSaving, saveError }) {
    if (index >= 0 && index < parsedTransactions.value.length) {
      const tx = parsedTransactions.value[index]
      if (isSaving !== undefined) tx.isSaving = isSaving
      if (saveError !== undefined) tx.saveError = saveError // Allows clearing error by passing null
    }
  }

  /** Sets the formatted date string used by the date input for a specific parsed transaction. */
  function setParsedTransactionDateFormatted(index, formattedDate) {
    if (index >= 0 && index < parsedTransactions.value.length) {
      parsedTransactions.value[index].transaction_date_formatted = formattedDate
    }
  }

  /** Clears the list of filtered transactions. */
  function clearFilteredTransactions() {
    filteredTransactions.value = [];
    console.log('Filtered transactions cleared.');
  }

  /** Clears all local data (useful on logout). */
  function clearData() {
    accounts.value = []
    recentTransactions.value = []
    filteredTransactions.value = [] // Also clear filtered transactions
    chartTransactions.value = []
    parsedTransactions.value = []
    error.value = null
    isLoading.value = false
    isLoadingChart.value = false
    isLoadingParse.value = false
    console.log('Data store cleared.')
  }

  return {
    accounts,
    recentTransactions,
    filteredTransactions, // Added filteredTransactions to the returned state
    chartTransactions,
    parsedTransactions,
    isLoading,
    isLoadingChart,
    isLoadingParse,
    error,

    fetchAccounts,
    fetchRecentTransactions,
    fetchChartData,
    fetchTransactionsByDateRange, // Added fetchTransactionsByDateRange to the returned actions
    fetchInitialData,
    addAccount,
    parseTransactionsNLP,
    createTransaction,
    clearParsedTransactions, // Added clearFilteredTransactions to the returned actions
    removeParsedTransaction,
    setParsedTransactionStatus,
    setParsedTransactionDateFormatted,
    clearFilteredTransactions, // Added clearFilteredTransactions to the returned actions
    clearData,
  }
})
