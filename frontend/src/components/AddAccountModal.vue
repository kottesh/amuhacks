<template>
  <Transition name="modal">
    <div
      v-if="showModal"
      class="fixed inset-0 z-50 overflow-y-auto bg-black bg-opacity-60 flex items-center justify-center p-4"
    >
      <div
        class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full p-6 space-y-4 transform transition-all duration-300 ease-out"
      >
        <div class="flex justify-between items-center">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Add New Account</h3>
          <button
            @click="$emit('close')"
            class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
          >
            <XMarkIcon class="h-6 w-6" />
          </button>
        </div>
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label
              for="accName"
              class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
              >Account Name</label
            >
            <input
              v-model="account.name"
              type="text"
              id="accName"
              required
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out text-sm"
              placeholder="e.g., Main Checking"
            />
          </div>
          <div>
            <label
              for="accType"
              class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
              >Account Type</label
            >
            <select
              v-model="account.type"
              id="accType"
              required
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out text-sm"
            >
              <option disabled value="">Select type</option>
              <option>Checking</option>
              <option>Savings</option>
              <option>Credit Card</option>
              <option>Cash</option>
              <option>Investment</option>
              <option>Loan</option>
              <option>Other</option>
            </select>
          </div>
          <div>
            <label
              for="accBalance"
              class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
              >Initial Balance (Optional)</label
            >
            <input
              v-model.number="account.balance"
              type="number"
              step="0.01"
              id="accBalance"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out text-sm"
              placeholder="0.00"
            />
          </div>
          <div>
            <label
              for="accCurrency"
              class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
              >Currency Code (e.g., INR, USD)</label
            >
            <input
              v-model="account.currency_code"
              type="text"
              id="accCurrency"
              maxlength="3"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-indigo-500 dark:focus:border-indigo-500 transition duration-150 ease-in-out uppercase text-sm"
              placeholder="INR"
            />
          </div>
          <p v-if="error" class="text-sm text-red-600 dark:text-red-400">{{ error }}</p>
          <div class="flex justify-end space-x-3 pt-2">
            <button
              type="button"
              @click="$emit('close')"
              class="inline-flex justify-center py-2 px-4 border border-gray-300 dark:border-gray-600 shadow-sm text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-offset-gray-800 transition duration-150 ease-in-out"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="isLoading"
              class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-offset-gray-800 transition duration-150 ease-in-out disabled:opacity-50"
            >
              <span v-if="!isLoading">Add Account</span> <span v-else>Adding...</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { reactive } from 'vue';
import { XMarkIcon } from '@heroicons/vue/24/outline';

const props = defineProps({
  showModal: {
    type: Boolean,
    required: true,
  },
  isLoading: {
    type: Boolean,
    required: true,
  },
  error: {
    type: String,
    default: '',
  },
});

const emit = defineEmits(['close', 'submit']);

// Initialize with default values
const account = reactive({
  name: '',
  type: '',
  balance: 0,
  currency_code: 'INR',
});

// Reset form when modal is opened
import { watch } from 'vue';

watch(
  () => props.showModal,
  (isOpen) => {
    if (isOpen) {
      // Reset form data when modal is opened
      account.name = '';
      account.type = '';
      account.balance = 0;
      account.currency_code = 'INR';
    }
  }
);

const handleSubmit = () => {
  emit('submit', account);
};
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
</style>
