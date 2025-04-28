<template>
  <div
    class="min-h-screen bg-gradient-to-br from-gray-50 via-gray-100 to-indigo-50 dark:from-gray-800 dark:via-gray-900 dark:to-black p-4 sm:p-6 lg:p-8 font-inter text-gray-800 dark:text-gray-200"
  >
    <div class="max-w-7xl mx-auto">
      <DashboardHeader
        @open-add-account="openAddAccountModal"
        @open-add-transaction="openAddTransactionModal"
        @logout="handleLogout"
      />

      <LoadingIndicator v-if="dataStore.isLoading && initialLoad" />
      <ErrorMessage
        v-else-if="dataStore.error && !showAddAccountModal && !showAddTransactionModal"
        :message="dataStore.error"
      />

      <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 space-y-6">
          <AccountsSection />
          <SpendingIncomeChart />
        </div>

        <div class="lg:col-span-1">
          <RecentTransactionsSection :transactions="sortedTransactions" />
        </div>
      </div>
    </div>

    <AddAccountModal
      :show-modal="showAddAccountModal"
      :is-loading="dataStore.isLoading"
      :error="modalError"
      @close="closeAddAccountModal"
      @submit="handleAddAccountSubmit"
    />

    <AddTransactionModal
      :show-modal="showAddTransactionModal"
      :error="modalError"
      @close="closeAddTransactionModal"
      @error="handleModalError"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, reactive, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { useDataStore } from '@/stores/dataStore'
import { apiClient } from '@/stores/authStore'
// Removed Chart.js imports
import {
  ArrowRightOnRectangleIcon,
  ExclamationTriangleIcon,
  PlusIcon,
  ChatBubbleLeftEllipsisIcon,
  XMarkIcon,
  CheckIcon,
} from '@heroicons/vue/24/outline'
import dayjs from 'dayjs'
import utc from 'dayjs/plugin/utc'
import relativeTime from 'dayjs/plugin/relativeTime'
import customParseFormat from 'dayjs/plugin/customParseFormat'
import DashboardHeader from '@/components/DashboardHeader.vue';
import LoadingIndicator from '@/components/LoadingIndicator.vue';
import ErrorMessage from '@/components/ErrorMessage.vue';
import AccountsSection from '@/components/AccountsSection.vue';
import SpendingIncomeChart from '@/components/SpendingIncomeChart.vue';
import RecentTransactionsSection from '@/components/RecentTransactionsSection.vue';
import AddAccountModal from '@/components/AddAccountModal.vue'; // Added import
import AddTransactionModal from '@/components/AddTransactionModal.vue'; // Import the new modal

dayjs.extend(utc)
dayjs.extend(relativeTime)
dayjs.extend(customParseFormat)

// Removed ChartJS registration

const router = useRouter()
const authStore = useAuthStore()
const dataStore = useDataStore()

const initialLoad = ref(true)
const showAddAccountModal = ref(false)
const showAddTransactionModal = ref(false)
// Removed nlpInputText ref
const modalError = ref('') // Keep modalError for potential errors from the modal

// Removed newAccount reactive object

const sortedTransactions = computed(() => {
  return [...dataStore.recentTransactions]
    .filter((tx) => tx && tx.date)
    .sort((a, b) => dayjs(b.date).valueOf() - dayjs(a.date).valueOf())
})

// Removed chartData, chartDataReady, chartOptions computed properties

const formatCurrency = (value, currencyCode = 'INR', compact = false) => {
  if (value === null || value === undefined) return ''
  const options = {
    style: 'currency',
    currency: currencyCode || 'INR', // Default to INR if not provided
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }
  if (compact) {
    options.notation = 'compact'
    options.minimumFractionDigits = 0 // Less precision needed for compact axis labels
    options.maximumFractionDigits = 1
  }
  try {
    return new Intl.NumberFormat('en-IN', options).format(value) // Use en-IN for Indian Rupee formatting
  } catch (e) {
    // Fallback for invalid currency code or other errors
    console.warn('Currency formatting failed:', e)
    options.currency = 'INR' // Fallback to INR
    return new Intl.NumberFormat('en-IN', options).format(value)
  }
}

// Removed formatDate function
// Removed formatDateForInput function
// Removed formatInputDateToISO function

// Add Account Modal Logic
const openAddAccountModal = () => {
  modalError.value = ''
  // Reset form - This logic should be moved to the modal component
  // Object.assign(newAccount, { name: '', type: '', balance: 0, currency_code: 'INR' })
  showAddAccountModal.value = true
}
const closeAddAccountModal = () => {
  showAddAccountModal.value = false
}
const handleAddAccountSubmit = async (accountData) => { // Updated to accept account data
  modalError.value = ''
  // Basic validation - This should ideally be in the modal component
  // if (!newAccount.name || !newAccount.type) {
  //   modalError.value = 'Account name and type are required.'
  //   return
  // }
  // Ensure balance is a number - This should ideally be in the modal component
  // newAccount.balance = Number(newAccount.balance) || 0
  // Uppercase currency code - This should ideally be in the modal component
  // newAccount.currency_code = (newAccount.currency_code || 'INR').toUpperCase()

  const success = await dataStore.addAccount(accountData) // Call Pinia store action with received data
  if (success) {
    closeAddAccountModal()
  } else {
    modalError.value = dataStore.error || 'Failed to add account. Please try again.'
  }
}

// Add Transaction Modal Logic
const openAddTransactionModal = () => {
  modalError.value = '' // Clear any previous error
  // nlpInputText.value = '' // No longer needed here
  dataStore.clearParsedTransactions() // Clear previous results from store
  showAddTransactionModal.value = true
}
const closeAddTransactionModal = () => {
  showAddTransactionModal.value = false
  // The modal component now handles clearing parsed transactions on close
  modalError.value = '' // Clear modal error on close
}

// Handle error emitted from the modal
const handleModalError = (errorMsg) => {
  modalError.value = errorMsg
}

// Removed handleNlpSubmit function
// Removed discardParsedTransaction function
// Removed confirmParsedTransaction function

// Handle user logout
const handleLogout = () => {
  authStore.logout()
  router.push('/login') // Redirect to login page after logout
}

onMounted(async () => {
  await dataStore.fetchInitialData()
  initialLoad.value = false
})

// Removed watch for dataStore.parsedTransactions
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition:
    opacity 0.3s ease,
    transform 0.3s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(-10px);
}
.modal-enter-to,
.modal-leave-from {
  opacity: 1;
  transform: scale(1) translateY(0);
}

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #d1d5db; 
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}
.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background: #4b5563;
}
.dark .custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #6b7280;
}
</style>
