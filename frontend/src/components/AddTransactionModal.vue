<template>
  <Transition name="modal">
    <div
      v-if="showModal"
      class="fixed inset-0 z-50 overflow-y-auto bg-black bg-opacity-60 flex items-center justify-center p-4"
      @click.self="closeModal"
    >
      <div
        class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full transform transition-all duration-300 ease-out"
      >
        <div
          class="flex justify-between items-center p-4 sm:p-6 border-b border-gray-200 dark:border-gray-700"
        >
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">
            {{
              dataStore.parsedTransactions.length > 0
                ? 'Confirm Transactions'
                : 'Add Transaction (Quick Add)'
            }}
          </h3>
          <button
            @click="closeModal"
            class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
          >
            <XMarkIcon class="h-6 w-6" />
          </button>
        </div>

        <div class="p-4 sm:p-6 space-y-4 max-h-[70vh] overflow-y-auto custom-scrollbar">
          <form
            v-if="dataStore.parsedTransactions.length === 0"
            @submit.prevent="handleNlpSubmit"
            class="space-y-4"
          >
            <div>
              <label
                for="nlpText"
                class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                >Describe your transaction(s)</label
              >
              <textarea
                v-model="nlpInputText"
                id="nlpText"
                rows="3"
                required
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out text-sm"
                placeholder="e.g., ₹1500 groceries yesterday, ₹200 coffee today from HDFC card"
              ></textarea>
            </div>
            <p v-if="localError" class="text-sm text-red-600 dark:text-red-400">
              {{ localError }}
            </p>
            <div class="flex justify-end space-x-3 pt-2">
              <button
                type="button"
                @click="closeModal"
                class="inline-flex justify-center py-2 px-4 border border-gray-300 dark:border-gray-600 shadow-sm text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-offset-gray-800 transition duration-150 ease-in-out"
              >
                Cancel
              </button>
              <button
                type="submit"
                :disabled="dataStore.isLoadingParse"
                class="inline-flex justify-center items-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-offset-gray-800 transition duration-150 ease-in-out disabled:opacity-50"
              >
                <svg
                  v-if="dataStore.isLoadingParse"
                  class="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    class="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    stroke-width="4"
                  ></circle>
                  <path
                    class="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                <span>{{ dataStore.isLoadingParse ? 'Parsing...' : 'Parse Transaction' }}</span>
              </button>
            </div>
          </form>

          <div v-else class="space-y-4">
            <p class="text-sm text-gray-600 dark:text-gray-400">
              Review and confirm the transactions found. You can edit details before saving.
            </p>
            <p v-if="localError" class="text-sm text-red-600 dark:text-red-400">
              {{ localError }}
            </p>

            <div
              v-for="(tx, index) in dataStore.parsedTransactions"
              :key="tx.tempId || index"
              class="border border-gray-200 dark:border-gray-700 rounded-lg p-4 space-y-3 bg-gray-50 dark:bg-gray-800/50 relative"
            >
              <div
                v-if="tx.isSaving"
                class="absolute inset-0 bg-white/70 dark:bg-gray-900/70 flex items-center justify-center rounded-lg z-10"
              >
                <svg
                  class="animate-spin h-6 w-6 text-indigo-600 dark:text-indigo-400"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    class="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    stroke-width="4"
                  ></circle>
                  <path
                    class="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
              </div>
              <p v-if="tx.saveError" class="text-xs text-red-600 dark:text-red-400 mb-2">
                {{ tx.saveError }}
              </p>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label
                    :for="'txDesc-' + index"
                    class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1"
                    >Description</label
                  >
                  <input
                    v-model="tx.description"
                    type="text"
                    :id="'txDesc-' + index"
                    required
                    class="block w-full px-2 py-1 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out text-sm"
                  />
                </div>
                <div>
                  <label
                    :for="'txCategory-' + index"
                    class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1"
                    >Category</label
                  >
                  <input
                    v-model="tx.category"
                    type="text"
                    :id="'txCategory-' + index"
                    class="block w-full px-2 py-1 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out text-sm"
                    placeholder="Optional"
                  />
                </div>
              </div>
              <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
                <div>
                  <label
                    :for="'txAmount-' + index"
                    class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1"
                    >Amount</label
                  >
                  <input
                    v-model.number="tx.amount"
                    type="number"
                    step="0.01"
                    :id="'txAmount-' + index"
                    required
                    class="block w-full px-2 py-1 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out text-sm"
                  />
                </div>
                <div>
                  <label
                    :for="'txType-' + index"
                    class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1"
                    >Type</label
                  >
                  <select
                    v-model="tx.type"
                    :id="'txType-' + index"
                    required
                    class="block w-full px-2 py-1 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out text-sm"
                  >
                    <option>EXPENSE</option>
                    <option>INCOME</option>
                  </select>
                </div>
                <div>
                  <label
                    :for="'txDate-' + index"
                    class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1"
                    >Date</label
                  >
                  <input
                    v-model="tx.date"
                    type="date"
                    :id="'txDate-' + index"
                    required
                    class="block w-full px-2 py-1 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out text-sm"
                  />
                </div>
                <div>
                  <label
                    :for="'txAccount-' + index"
                    class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1"
                    >Account</label
                  >
                  <select
                    v-model="tx.account_id"
                    :id="'txAccount-' + index"
                    required
                    class="block w-full px-2 py-1 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out text-sm"
                  >
                    <option disabled value="">Select</option>
                    <option v-for="acc in dataStore.accounts" :key="acc.id" :value="acc.id">
                      {{ acc.name }}
                    </option>
                  </select>
                </div>
              </div>

              <div class="flex justify-end space-x-2 pt-2">
                <button
                  @click="discardParsedTransaction(index)"
                  type="button"
                  title="Discard this transaction"
                  class="p-1.5 text-gray-500 hover:text-red-600 dark:text-gray-400 dark:hover:text-red-500 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-1 dark:focus:ring-offset-gray-800 transition duration-150 ease-in-out"
                >
                  <XMarkIcon class="h-5 w-5" />
                </button>
                <button
                  @click="confirmParsedTransaction(index)"
                  type="button"
                  title="Confirm and save this transaction"
                  class="p-1.5 text-gray-500 hover:text-green-600 dark:text-gray-400 dark:hover:text-green-500 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-1 dark:focus:ring-offset-gray-800 transition duration-150 ease-in-out"
                >
                  <CheckIcon class="h-5 w-5" />
                </button>
              </div>
            </div>

            <div class="flex justify-end pt-4">
              <button
                type="button"
                @click="closeModal"
                class="inline-flex justify-center py-2 px-4 border border-gray-300 dark:border-gray-600 shadow-sm text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-offset-gray-800 transition duration-150 ease-in-out"
              >
                {{ dataStore.parsedTransactions.length > 0 ? 'Done' : 'Cancel' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { useDataStore } from '@/stores/dataStore'
import { XMarkIcon, CheckIcon } from '@heroicons/vue/24/outline'
import dayjs from 'dayjs'
import utc from 'dayjs/plugin/utc'
import customParseFormat from 'dayjs/plugin/customParseFormat'

dayjs.extend(utc)
dayjs.extend(customParseFormat)

const props = defineProps({
  showModal: {
    type: Boolean,
    required: true,
  },
  error: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['close', 'error'])

const dataStore = useDataStore()
const nlpInputText = ref('')
const localError = ref('') // Use local error state for modal-specific errors

// Watch the prop error and update localError
watch(
  () => props.error,
  (newError) => {
    localError.value = newError
  },
)

// Watch for changes in parsed transactions to format dates for input
watch(
  () => dataStore.parsedTransactions,
  (newTransactions) => {
    if (newTransactions) {
      newTransactions.forEach((tx, index) => {
        // Add the formatted date property if it doesn't exist
        if (!tx.hasOwnProperty('date')) {
          dataStore.setParsedTransactionDateFormatted(
            index,
            formatDateForInput(tx.transaction_date),
          )
        }
        // Add other properties needed for UI state if they don't exist
        if (!tx.hasOwnProperty('isSaving')) {
          dataStore.setParsedTransactionStatus(index, { isSaving: false })
        }
        if (!tx.hasOwnProperty('saveError')) {
          dataStore.setParsedTransactionStatus(index, { saveError: null })
        }
      })
    }
  },
  { deep: true, immediate: true },
)

// Format date for input type="date" (YYYY-MM-DD)
const formatDateForInput = (dateString) => {
  if (!dateString) return dayjs().format('YYYY-MM-DD') // Default to today if no date
  const parsedDate = dayjs(dateString, ['YYYY-MM-DDTHH:mm:ssZ', 'YYYY-MM-DD', dayjs.ISO_8601], true)
  return parsedDate.isValid() ? parsedDate.format('YYYY-MM-DD') : dayjs().format('YYYY-MM-DD')
}

// Convert YYYY-MM-DD (representing a date) back to ISO string (noon UTC of that date) for backend
const formatInputDateToISO = (dateString) => {
  if (!dateString) return dayjs.utc().toISOString(); // Default to now UTC if invalid

  // 1. Parse the date string directly as UTC. This treats 'YYYY-MM-DD' as 00:00:00 UTC.
  const utcDate = dayjs.utc(dateString);
  if (!utcDate.isValid()) return dayjs.utc().toISOString(); // Fallback if parsing fails

  // 2. Set the time to noon UTC to avoid timezone-related shifts at midnight.
  // 3. Format as ISO string.
  return utcDate.hour(12).minute(0).second(0).millisecond(0).toISOString();
}

const closeModal = () => {
  emit('close')
  // Clear local state on close
  nlpInputText.value = ''
  localError.value = ''
  // Important: Clear parsed transactions from the store when closing the modal fully
  dataStore.clearParsedTransactions()
}

// Handle NLP text submission
const handleNlpSubmit = async () => {
  localError.value = '' // Clear previous local error
  if (!nlpInputText.value.trim()) {
    localError.value = 'Please describe the transaction(s).'
    emit('error', localError.value) // Emit error to parent if needed
    return
  }

  const success = await dataStore.parseTransactionsNLP(nlpInputText.value)

  if (!success) {
    localError.value =
      dataStore.error ||
      'Could not parse transactions. Please check the format or try adding manually.'
    emit('error', localError.value) // Emit error to parent
  } else {
    // Clear NLP input on successful parse
    nlpInputText.value = ''
  }
}

const discardParsedTransaction = (index) => {
  dataStore.removeParsedTransaction(index)
  // If it was the last one, close the modal
  if (dataStore.parsedTransactions.length === 0) {
    closeModal()
  }
}

const confirmParsedTransaction = async (index) => {
  const transaction = dataStore.parsedTransactions[index]

  // Clear previous save error for this specific transaction
  dataStore.setParsedTransactionStatus(index, { saveError: null })
  localError.value = '' // Clear general modal error

  // --- Validation ---
  if (!transaction.account_id) {
    dataStore.setParsedTransactionStatus(index, { saveError: 'Please select an account.' })
    return
  }
  if (!transaction.amount || isNaN(transaction.amount) || transaction.amount <= 0) {
    dataStore.setParsedTransactionStatus(index, {
      saveError: 'Please enter a valid positive amount.',
    })
    return
  }
  if (!transaction.description) {
    dataStore.setParsedTransactionStatus(index, { saveError: 'Description cannot be empty.' })
    return
  }
  if (!transaction.date) {
    dataStore.setParsedTransactionStatus(index, { saveError: 'Please select a valid date.' })
    return
  }
  // --- End Validation ---

  const transactionData = {
    account_id: transaction.account_id,
    amount: transaction.amount,
    type: transaction.type,
    category: transaction.category || null,
    description: transaction.description,
    date: formatInputDateToISO(transaction.date), // Use the formatted date
  }

  dataStore.setParsedTransactionStatus(index, { isSaving: true })

  const success = await dataStore.createTransaction(transactionData)

  if (success) {
    dataStore.removeParsedTransaction(index) // Remove on success
    // If it was the last one, close the modal
    if (dataStore.parsedTransactions.length === 0) {
      closeModal()
    }
  } else {
    // Set specific error on the transaction item and potentially a general modal error
    const errorMsg = dataStore.error || 'Failed to save transaction.'
    dataStore.setParsedTransactionStatus(index, {
      isSaving: false,
      saveError: errorMsg,
    })
    localError.value = 'One or more transactions failed to save.' // Set general error
    emit('error', localError.value) // Emit general error
  }
}
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
  background: #d1d5db; /* Light mode scrollbar */
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}
.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background: #4b5563; /* Dark mode scrollbar */
}
.dark .custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #6b7280;
}
</style>
