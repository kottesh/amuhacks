<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-gray-100 to-indigo-50 dark:from-gray-800 dark:via-gray-900 dark:to-black p-4 sm:p-6 lg:p-8 font-inter text-gray-800 dark:text-gray-200">
    <div class="max-w-7xl mx-auto">
      <header class="mb-8 flex flex-col sm:flex-row justify-between items-center space-y-4 sm:space-y-0">
        <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">
          Dashboard
        </h1>
        <div class="flex items-center space-x-3">
           <button
            @click="showAddAccountModal = true"
            title="Add New Account"
            class="p-2 bg-indigo-600 text-white rounded-full shadow-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition duration-300 ease-in-out"
          >
            <PlusIcon class="h-5 w-5" aria-hidden="true" />
          </button>
           <button
            @click="showAddTransactionModal = true"
            title="Add New Transaction (NLP)"
            class="p-2 bg-green-600 text-white rounded-full shadow-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition duration-300 ease-in-out"
          >
            <ChatBubbleLeftEllipsisIcon class="h-5 w-5" aria-hidden="true" />
          </button>
          <button
            @click="handleLogout"
            title="Logout"
            class="p-2 bg-red-600 text-white rounded-full shadow-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition duration-300 ease-in-out"
          >
            <ArrowRightOnRectangleIcon class="h-5 w-5" aria-hidden="true" />
          </button>
        </div>
      </header>

      <div v-if="dataStore.isLoading && initialLoad" class="text-center py-10 text-gray-600 dark:text-gray-400">
        <svg class="animate-spin h-8 w-8 text-indigo-600 dark:text-indigo-400 mx-auto mb-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"> <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle> <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path> </svg>
        Loading dashboard data...
      </div>
      <div v-else-if="dataStore.error && !showAddAccountModal && !showAddTransactionModal && !showConfirmTransactionModal" class="p-4 mb-6 bg-red-100 dark:bg-red-900 border border-red-300 dark:border-red-700 rounded-lg shadow text-sm text-red-700 dark:text-red-200 flex items-center space-x-2">
        <ExclamationTriangleIcon class="h-5 w-5 flex-shrink-0" aria-hidden="true" />
        <span>{{ dataStore.error }}</span>
      </div>

      <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 space-y-6">
          <section class="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden transition-all duration-300 ease-in-out">
            <div class="p-5 border-b border-gray-200 dark:border-gray-700"> <h2 class="text-xl font-semibold text-gray-800 dark:text-gray-200">Your Accounts</h2> </div>
            <div class="p-5">
              <div v-if="dataStore.accounts.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div v-for="account in dataStore.accounts" :key="account.id" class="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:shadow-lg hover:scale-[1.02] transition-all duration-200 ease-in-out bg-gray-50 dark:bg-gray-700/50">
                  <div class="flex justify-between items-center mb-1"> <span class="font-medium text-gray-900 dark:text-white truncate">{{ account.name }}</span> <BanknotesIcon class="h-5 w-5 text-indigo-500 dark:text-indigo-400 flex-shrink-0 ml-2" /> </div>
                  <p class="text-sm text-gray-500 dark:text-gray-400 mb-2">{{ account.type }}</p>
                  <p class="text-lg font-semibold text-gray-900 dark:text-white"> {{ formatCurrency(account.balance, account.currency_code) }} </p>
                </div>
              </div>
              <p v-else class="text-center text-gray-500 dark:text-gray-400 py-4">No accounts found. Click the '+' button above to add one!</p>
            </div>
          </section>

          <section class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-5 transition-all duration-300 ease-in-out">
             <h2 class="text-xl font-semibold text-gray-800 dark:text-gray-200 mb-4">Spending (Last 7 Days)</h2>
            <div v-if="chartDataReady" class="h-64 sm:h-72"> <Line :data="chartData" :options="chartOptions" /> </div>
             <p v-else class="text-center text-gray-500 dark:text-gray-400 py-10">Not enough transaction data for chart.</p>
          </section>
        </div>

        <div class="lg:col-span-1">
          <section class="bg-white dark:bg-gray-800 rounded-lg shadow-lg h-full flex flex-col transition-all duration-300 ease-in-out">
             <div class="p-5 border-b border-gray-200 dark:border-gray-700"> <h2 class="text-xl font-semibold text-gray-800 dark:text-gray-200">Recent Transactions</h2> </div>
            <div v-if="sortedTransactions.length > 0" class="flex-grow overflow-y-auto p-5 space-y-3 max-h-[calc(100vh-16rem)]">
              <div v-for="tx in sortedTransactions" :key="tx.id" class="flex justify-between items-center p-3 border-b border-gray-100 dark:border-gray-700/50 last:border-b-0 hover:bg-gray-50 dark:hover:bg-gray-700/30 rounded transition-colors duration-150">
                <div> <p class="font-medium text-gray-900 dark:text-white text-sm">{{ tx.description }}</p> <p class="text-xs text-gray-500 dark:text-gray-400"> {{ formatDate(tx.date) }} - {{ tx.category || 'Uncategorized' }} </p> </div>
                <span :class="[ tx.type === 'INCOME' ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400', 'font-semibold text-sm flex-shrink-0 ml-2' ]"> {{ formatCurrency(tx.amount, tx.currency_code) }} </span>
              </div>
            </div>
            <p v-else class="text-center text-gray-500 dark:text-gray-400 py-10 px-5">No recent transactions found.</p>
          </section>
        </div>
      </div>
    </div>

    <Transition name="modal">
     <div v-if="showAddAccountModal" class="fixed inset-0 z-50 overflow-y-auto bg-black bg-opacity-60 flex items-center justify-center p-4">
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full p-6 space-y-4 transform transition-all duration-300 ease-out">
            <div class="flex justify-between items-center"> <h3 class="text-lg font-medium text-gray-900 dark:text-white">Add New Account</h3> <button @click="closeAddAccountModal" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"> <XMarkIcon class="h-6 w-6"/> </button> </div>
            <form @submit.prevent="handleAddAccountSubmit" class="space-y-4">
                <div>
                    <label for="accName" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Account Name</label>
                    <input v-model="newAccount.name" type="text" id="accName" required class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out text-sm" placeholder="e.g., Main Checking">
                </div>
                <div>
                    <label for="accType" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Account Type</label>
                    <select v-model="newAccount.type" id="accType" required class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out text-sm">
                        <option disabled value="">Select type</option> <option>Checking</option> <option>Savings</option> <option>Credit Card</option> <option>Cash</option> <option>Investment</option> <option>Loan</option> <option>Other</option>
                    </select>
                </div>
                 <div>
                    <label for="accBalance" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Initial Balance (Optional)</label>
                    <input v-model.number="newAccount.balance" type="number" step="0.01" id="accBalance" class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out text-sm" placeholder="0.00">
                </div>
                 <div>
                    <label for="accCurrency" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Currency Code (Optional)</label>
                    <input v-model="newAccount.currency_code" type="text" id="accCurrency" maxlength="3" class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out uppercase text-sm" placeholder="INR">
                </div>
                 <p v-if="modalError" class="text-sm text-red-600 dark:text-red-400">{{ modalError }}</p>
                 <div class="flex justify-end space-x-3 pt-2">
                     <button type="button" @click="closeAddAccountModal" class="inline-flex justify-center py-2 px-4 border border-gray-300 dark:border-gray-600 shadow-sm text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-offset-gray-800 transition duration-150 ease-in-out">Cancel</button>
                     <button type="submit" :disabled="dataStore.isLoading" class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-offset-gray-800 transition duration-150 ease-in-out disabled:opacity-50">
                         <span v-if="!dataStore.isLoading">Add Account</span> <span v-else>Adding...</span>
                     </button>
                 </div>
            </form>
        </div>
     </div>
    </Transition>

    <Transition name="modal">
     <div v-if="showAddTransactionModal" class="fixed inset-0 z-50 overflow-y-auto bg-black bg-opacity-60 flex items-center justify-center p-4">
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-lg w-full p-6 space-y-4 transform transition-all duration-300 ease-out">
             <div class="flex justify-between items-center"> <h3 class="text-lg font-medium text-gray-900 dark:text-white">Add Transaction (Quick Add)</h3> <button @click="closeAddTransactionModal" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"> <XMarkIcon class="h-6 w-6"/> </button> </div>
             <form @submit.prevent="handleNlpSubmit" class="space-y-4">
                <div>
                    <label for="nlpText" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Describe your transaction(s)</label>
                    <textarea v-model="nlpInputText" id="nlpText" rows="3" required class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out text-sm" placeholder="e.g., ₹1500 groceries yesterday, ₹200 coffee today"></textarea>
                </div>
                 <p v-if="modalError" class="text-sm text-red-600 dark:text-red-400">{{ modalError }}</p>
                 <div class="flex justify-end space-x-3 pt-2">
                     <button type="button" @click="closeAddTransactionModal" class="inline-flex justify-center py-2 px-4 border border-gray-300 dark:border-gray-600 shadow-sm text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-offset-gray-800 transition duration-150 ease-in-out">Cancel</button>
                     <button type="submit" :disabled="isLoadingParse" class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-offset-gray-800 transition duration-150 ease-in-out disabled:opacity-50">
                         <span v-if="!isLoadingParse">Parse Transaction</span> <span v-else>Parsing...</span>
                     </button>
                 </div>
             </form>
        </div>
     </div>
     </Transition>

     <Transition name="modal">
     <div v-if="showConfirmTransactionModal && transactionToConfirm" class="fixed inset-0 z-50 overflow-y-auto bg-black bg-opacity-60 flex items-center justify-center p-4">
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-lg w-full p-6 space-y-4 transform transition-all duration-300 ease-out">
             <div class="flex justify-between items-center"> <h3 class="text-lg font-medium text-gray-900 dark:text-white">Confirm Transaction</h3> <button @click="closeConfirmTransactionModal" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"> <XMarkIcon class="h-6 w-6"/> </button> </div>
             <form @submit.prevent="handleConfirmTransactionSubmit" class="space-y-4">
                 <div>
                    <label for="txDesc" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Description</label>
                    <input v-model="transactionToConfirm.description" type="text" id="txDesc" required class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out text-sm">
                 </div>
                 <div class="grid grid-cols-2 gap-4">
                     <div>
                        <label for="txAmount" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Amount</label>
                        <input v-model.number="transactionToConfirm.amount" type="number" step="0.01" id="txAmount" required class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out text-sm">
                     </div>
                     <div>
                        <label for="txType" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Type</label>
                        <select v-model="transactionToConfirm.type" id="txType" required class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out text-sm"> <option>EXPENSE</option> <option>INCOME</option> </select>
                     </div>
                 </div>
                 <div>
                    <label for="txDate" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Date</label>
                    <input v-model="transactionToConfirm.date" type="date" id="txDate" required class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out text-sm">
                 </div>
                  <div>
                    <label for="txCategory" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Category (Optional)</label>
                    <input v-model="transactionToConfirm.category" type="text" id="txCategory" class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out text-sm">
                 </div>
                 <div>
                    <label for="txAccount" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Account</label>
                    <select v-model="transactionToConfirm.account_id" id="txAccount" required class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out text-sm">
                         <option disabled value="">Select account</option>
                         <option v-for="acc in dataStore.accounts" :key="acc.id" :value="acc.id"> {{ acc.name }} ({{ formatCurrency(acc.balance, acc.currency_code || 'INR') }}) </option>
                    </select>
                 </div>
                 <p v-if="modalError" class="text-sm text-red-600 dark:text-red-400">{{ modalError }}</p>
                 <div class="flex justify-end space-x-3 pt-2">
                     <button type="button" @click="closeConfirmTransactionModal" class="inline-flex justify-center py-2 px-4 border border-gray-300 dark:border-gray-600 shadow-sm text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-offset-gray-800 transition duration-150 ease-in-out">Cancel</button>
                     <button type="submit" :disabled="dataStore.isLoading" class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-offset-gray-800 transition duration-150 ease-in-out disabled:opacity-50">
                         <span v-if="!dataStore.isLoading">Save Transaction</span> <span v-else>Saving...</span>
                     </button>
                 </div>
             </form>
        </div>
     </div>
     </Transition>

  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';
import { useDataStore } from '@/stores/dataStore';
import { apiClient } from '@/stores/authStore'; // Adjust path as needed
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement } from 'chart.js';
import {
    BanknotesIcon, ArrowRightOnRectangleIcon, ExclamationTriangleIcon,
    PlusIcon, ChatBubbleLeftEllipsisIcon, XMarkIcon
} from '@heroicons/vue/24/outline';

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement);
const router = useRouter();
const authStore = useAuthStore();
const dataStore = useDataStore();
const initialLoad = ref(true);
const chartSummary = ref(null);
const modalError = ref('');
const showAddAccountModal = ref(false);
// Update default currency for new account
const newAccount = reactive({ name: '', type: '', balance: 0, currency_code: 'INR' });
const showAddTransactionModal = ref(false);
const nlpInputText = ref('');
const isLoadingParse = ref(false);
const parsedTransactions = ref([]);
const showConfirmTransactionModal = ref(false);
const transactionToConfirm = ref(null);

const sortedTransactions = computed(() => {
    if (!dataStore.recentTransactions || dataStore.recentTransactions.length === 0) return [];
    return [...dataStore.recentTransactions].sort((a, b) => new Date(b.date) - new Date(a.date));
});
const chartDataReady = computed(() => chartSummary.value && chartSummary.value.labels?.length > 0);
const chartData = computed(() => {
  if (!chartDataReady.value) return { labels: [], datasets: [] };
  return {
    labels: chartSummary.value.labels,
    datasets: [{
        label: 'Spending',
        backgroundColor: 'rgba(79, 70, 229, 0.2)',
        borderColor: 'rgb(79, 70, 229)',
        borderWidth: 2, tension: 0.4, fill: true,
        data: chartSummary.value.spendingData,
    }],
    incomeCounts: chartSummary.value.incomeCounts,
    expenseCounts: chartSummary.value.expenseCounts,
  };
});

// --- Chart Configuration ---
const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  interaction: { mode: 'index', intersect: false, },
  plugins: {
    legend: { display: false },
    tooltip: {
        callbacks: {
             label: function(context) {
                 let label = context.dataset.label || '';
                 if (label) label += ': ';
                 // Use INR formatting in tooltip
                 if (context.parsed.y !== null) label += formatCurrency(context.parsed.y, 'INR');
                 return label;
             },
             afterBody: function(context) {
                 const dataIndex = context[0]?.dataIndex;
                 if (dataIndex !== undefined && chartData.value.incomeCounts && chartData.value.expenseCounts) {
                     const incomeCount = chartData.value.incomeCounts[dataIndex] || 0;
                     const expenseCount = chartData.value.expenseCounts[dataIndex] || 0;
                     return [ `Income Tx: ${incomeCount}`, `Expense Tx: ${expenseCount}` ];
                 }
                 return '';
             }
         }
    },
  },
  scales: {
        x: { grid: { display: false }, ticks: { color: '#6b7280' } },
        y: {
            grid: { color: '#e5e7eb' },
            ticks: {
                color: '#6b7280',
                // Use formatCurrency for Y-axis ticks
                callback: function(value) { return formatCurrency(value, 'INR'); }
            }
    },
  },
});

function getISODateString(date) {
    if (!(date instanceof Date) || isNaN(date)) { console.error("Invalid date provided to getISODateString"); return null; }
    const pad = (num) => num.toString().padStart(2, '0');
    return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`;
}

function formatCurrency(amount, currencyCode = 'INR') {
  try {
      const numericAmount = Number(amount);
      if (isNaN(numericAmount)) return `${currencyCode} ---`;
      return new Intl.NumberFormat('en-IN', { style: 'currency', currency: currencyCode }).format(numericAmount);
  } catch (e) {
      console.error("Error formatting currency:", amount, currencyCode, e);
      return `${currencyCode} ${amount}`;
  }
}

function formatDate(dateString) {
    if (!dateString) return ''; const options = { year: 'numeric', month: 'short', day: 'numeric' }; try { const date = new Date(dateString); if (isNaN(date)) return dateString; return new Intl.DateTimeFormat('en-US', options).format(date); } catch (e) { console.error("Err fmt date:", dateString, e); return dateString; }
}
function processChartData(weeklyTransactions) {
    const today = new Date(); const labels = []; const dailySpending = {}; const dailyIncomeCounts = {}; const dailyExpenseCounts = {};
    for (let i = 6; i >= 0; i--) { const date = new Date(today); date.setDate(today.getDate() - i); const label = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }); labels.push(label); const dateKey = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`; dailySpending[dateKey] = 0; dailyIncomeCounts[dateKey] = 0; dailyExpenseCounts[dateKey] = 0; }
    weeklyTransactions.forEach(tx => { const txDate = new Date(tx.date); if (!isNaN(txDate)) { const dateKey = `${txDate.getFullYear()}-${(txDate.getMonth() + 1).toString().padStart(2, '0')}-${txDate.getDate().toString().padStart(2, '0')}`; if (dailySpending.hasOwnProperty(dateKey)) { if (tx.type === 'EXPENSE') { dailySpending[dateKey] += tx.amount; dailyExpenseCounts[dateKey]++; } else if (tx.type === 'INCOME') { dailyIncomeCounts[dateKey]++; } } } else { console.warn("Invalid date in transaction:", tx); } });
    const mapDateKey = (label) => { let targetDate; try { const currentYear = today.getFullYear(); targetDate = new Date(`${label}, ${currentYear}`); if (Math.abs(targetDate.getMonth() - today.getMonth()) > 6) { targetDate = new Date(`${label}, ${targetDate.getMonth() > today.getMonth() ? currentYear - 1 : currentYear + 1}`); } } catch(e) { return null; } if (isNaN(targetDate)) return null; return `${targetDate.getFullYear()}-${(targetDate.getMonth() + 1).toString().padStart(2, '0')}-${targetDate.getDate().toString().padStart(2, '0')}`; };
    const spendingData = labels.map(label => dailySpending[mapDateKey(label)] || 0); const incomeCounts = labels.map(label => dailyIncomeCounts[mapDateKey(label)] || 0); const expenseCounts = labels.map(label => dailyExpenseCounts[mapDateKey(label)] || 0);
    chartSummary.value = { labels, spendingData, incomeCounts, expenseCounts };   
}

async function fetchDashboardData() {
  if (initialLoad.value) dataStore.isLoading = true;
  dataStore.error = null;
  try {
    const endDate = new Date(); const startDate = new Date(); startDate.setDate(endDate.getDate() - 6); startDate.setHours(0, 0, 0, 0); const startDateString = getISODateString(startDate); const endDateString = getISODateString(endDate); if (!startDateString || !endDateString) throw new Error("Invalid date range.");
    const [_, __, weeklyTransactions] = await Promise.all([ dataStore.fetchAccounts(), dataStore.fetchRecentTransactions(), dataStore.fetchTransactionsForPeriod(startDateString, endDateString) ]);
    processChartData(weeklyTransactions);
  } catch (err) { console.error("Failed fetch dashboard:", err); if (!dataStore.error) { dataStore.error = err.message || 'Unknown error loading dashboard.'; } }
  finally { dataStore.isLoading = false; initialLoad.value = false; }
}

// --- Modal Methods ---
function closeAddAccountModal() { showAddAccountModal.value = false; modalError.value = ''; Object.assign(newAccount, { name: '', type: '', balance: 0, currency_code: 'INR' }); } // Reset with INR
function closeAddTransactionModal() { showAddTransactionModal.value = false; modalError.value = ''; nlpInputText.value = ''; parsedTransactions.value = []; }
function closeConfirmTransactionModal() { showConfirmTransactionModal.value = false; modalError.value = ''; transactionToConfirm.value = null; }

async function handleAddAccountSubmit() {
    modalError.value = ''; if (!newAccount.name || !newAccount.type) { modalError.value = 'Name and type required.'; return; }
    try { const payload = { name: newAccount.name, type: newAccount.type, balance: newAccount.balance === null || newAccount.balance === '' ? 0 : Number(newAccount.balance), currency_code: newAccount.currency_code?.toUpperCase() || 'INR' }; await dataStore.createAccount(payload); closeAddAccountModal(); } catch (err) { modalError.value = dataStore.error || 'Failed to create account.'; }
}

async function handleNlpSubmit() {
    modalError.value = ''; if (!nlpInputText.value.trim()) { modalError.value = 'Enter transaction details.'; return; }
    isLoadingParse.value = true;
    try { const response = await apiClient.post('/transactions/parse', { text: nlpInputText.value }); parsedTransactions.value = response.data || []; if (parsedTransactions.value.length === 0) { modalError.value = 'Could not parse transactions.'; } else { closeAddTransactionModal(); openConfirmModal(parsedTransactions.value[0]); } } catch (err) { console.error('NLP Parse Error:', err); const detail = err.response?.data?.detail; modalError.value = typeof detail === 'object' ? JSON.stringify(detail) : (detail || err.message || 'Failed to parse.'); parsedTransactions.value = []; } finally { isLoadingParse.value = false; }
}

function openConfirmModal(parsedTx) {
    modalError.value = ''; const date = parsedTx.date ? new Date(parsedTx.date) : new Date(); const formattedDate = !isNaN(date) ? date.toISOString().split('T')[0] : '';
    transactionToConfirm.value = reactive({ description: parsedTx.description || '', amount: parsedTx.amount || 0, date: formattedDate, category: parsedTx.category || '', type: parsedTx.type || (parsedTx.amount < 0 ? 'EXPENSE' : 'INCOME'), account_id: '', currency_code: parsedTx.currency_code || 'INR' }); // Default/fallback to INR
    showConfirmTransactionModal.value = true;
}

async function handleConfirmTransactionSubmit() {
     modalError.value = ''; if (!transactionToConfirm.value?.account_id) { modalError.value = 'Select an account.'; return; }
     let isoDate; try { const dateObj = new Date(transactionToConfirm.value.date); if(isNaN(dateObj)) throw new Error('Invalid date'); dateObj.setHours(12, 0, 0, 0); isoDate = getISODateString(dateObj); if (!isoDate) throw new Error('Could not format date'); } catch (e) { modalError.value = 'Invalid date format.'; return; }
     const payload = { description: transactionToConfirm.value.description, amount: Number(transactionToConfirm.value.amount), date: isoDate, category: transactionToConfirm.value.category || null, account_id: Number(transactionToConfirm.value.account_id), type: transactionToConfirm.value.type, };
     try { await dataStore.createTransaction(payload); closeConfirmTransactionModal(); await fetchDashboardData(); } catch (err) { modalError.value = dataStore.error || 'Failed to save transaction.'; }
}

// --- Logout Method ---
function handleLogout() { authStore.logout(); dataStore.clearData(); router.push('/login'); }

// --- Lifecycle Hooks ---
onMounted(() => { fetchDashboardData(); watch(() => authStore.isAuthenticated, (isAuth) => { if (!isAuth) dataStore.clearData(); }); });

</script>

<style scoped>
/* Modal Transition styles remain */
.modal-enter-active, .modal-leave-active { transition: opacity 0.3s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-active .transform, .modal-leave-active .transform { transition: all 0.3s ease; }
.modal-enter-from .transform, .modal-leave-to .transform { opacity: 0; transform: translateY(-20px) scale(0.95); }
.modal-enter-to .transform, .modal-leave-from .transform { opacity: 1; transform: translateY(0) scale(1); }

/* Other styles remain */
.font-inter { font-family: 'Inter', sans-serif; }
.max-h-\[calc\(100vh-16rem\)\] { max-height: calc(100vh - 16rem); }
.max-h-\[calc\(100vh-16rem\)\]::-webkit-scrollbar { width: 6px; }
.max-h-\[calc\(100vh-16rem\)\]::-webkit-scrollbar-track { background: transparent; }
.max-h-\[calc\(100vh-16rem\)\]::-webkit-scrollbar-thumb { background-color: rgba(161, 161, 170, 0.5); border-radius: 3px; }
.max-h-\[calc\(100vh-16rem\)\]::-webkit-scrollbar-thumb:hover { background-color: rgba(113, 113, 122, 0.5); }
.h-64 { height: 16rem; }
.sm\:h-72 { height: 18rem; }
</style>

