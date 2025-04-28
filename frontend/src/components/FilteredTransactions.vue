<template>
  <section class="card glass shadow-lg transition-all duration-300 ease-in-out animate-slide-in-up rounded-2xl overflow-hidden">
    <div class="p-6 bg-white/90 dark:bg-neutral-800/80 border-b border-neutral-200 dark:border-neutral-700">
      <h2 class="text-xl font-semibold text-primary-600 dark:text-primary-300 mb-5 flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 mr-2 text-primary-400">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 0 1-.659 1.591l-5.432 5.432a2.25 2.25 0 0 0-.659 1.591v2.927a2.25 2.25 0 0 1-1.244 2.013L9.75 21v-6.568a2.25 2.25 0 0 0-.659-1.591L3.659 7.409A2.25 2.25 0 0 1 3 5.818V4.774c0-.54.384-1.006.917-1.096A48.32 48.32 0 0 1 12 3Z" />
        </svg>
        Filter Transactions
      </h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-5 items-end">
        <div class="lg:col-span-2">
          <label for="startDate" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Start Date</label>
          <input
            type="date"
            id="startDate"
            v-model="startDate"
            class="w-full border rounded-lg p-2 bg-white dark:bg-gray-700 text-gray-900 dark:text-white border-gray-300 dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200"
          />
        </div>
        <div class="lg:col-span-2">
          <label for="endDate" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">End Date</label>
          <input
            type="date"
            id="endDate"
            v-model="endDate"
            class="w-full border rounded-lg p-2 bg-white dark:bg-gray-700 text-gray-900 dark:text-white border-gray-300 dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200"
          />
        </div>
        <div class="lg:col-span-1">
          <button
            @click="fetchTransactionsByDate"
            :disabled="isLoading"
            class="inline-flex items-center justify-center w-full bg-primary-500 hover:bg-primary-600 focus:bg-primary-600 text-white font-medium py-2 px-4 rounded-lg transition duration-300 ease-in-out disabled:opacity-70 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800"
          >
            <svg v-if="!isLoading" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 mr-2">
              <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
            </svg>
            <svg v-else class="animate-spin h-5 w-5 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>{{ isLoading ? 'Loading...' : 'Filter' }}</span>
          </button>
        </div>
      </div>
    </div>

    <ErrorMessage v-if="error" :message="error" class="mb-4 px-5" /> <!-- Display error above content -->

    <div class="p-5 max-h-[60vh] overflow-y-auto scrollbar scrollbar-thin scrollbar-thumb-gray-300 dark:scrollbar-thumb-gray-600 scrollbar-track-transparent">
      <div v-if="isLoading && filteredTransactions.length === 0" class="text-center py-10 text-neutral-500 dark:text-neutral-400 flex flex-col items-center">
        <svg class="animate-spin h-10 w-10 text-primary-400 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        Loading transactions...
      </div>
      <div v-else-if="filteredTransactions.length > 0" class="space-y-2">
        <TransactionItem
          v-for="transaction in filteredTransactions"
          :key="transaction.id"
          :transaction="transaction"
        />
      </div>
      <div v-else class="text-center text-neutral-500 dark:text-neutral-400 py-8 px-4 bg-neutral-50 dark:bg-neutral-800 rounded-xl border border-neutral-200 dark:border-neutral-700 mt-4">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10 mx-auto mb-3 text-neutral-400">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z" />
        </svg>
        No transactions found for the selected date range. Select dates and click Filter.
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useDataStore } from '@/stores/dataStore';
import TransactionItem from '@/components/TransactionItem.vue';
import ErrorMessage from '@/components/ErrorMessage.vue';
import dayjs from 'dayjs';

const dataStore = useDataStore();

const startDate = ref('');
const endDate = ref('');

const filteredTransactions = computed(() => dataStore.filteredTransactions);
const isLoading = computed(() => dataStore.isLoading);
const error = computed(() => dataStore.error);


const fetchTransactionsByDate = async () => {
  // Clear previous error from the store before a new fetch
  dataStore.error = null;

  if (!startDate.value || !endDate.value) {
    dataStore.error = 'Please select both start and end dates.';
    return;
  }

  // Ensure dates are in YYYY-MM-DD format for the API
  const start = dayjs(startDate.value).format('YYYY-MM-DD');
  const end = dayjs(endDate.value).format('YYYY-MM-DD');

  // The dataStore action handles setting isLoading and error
  await dataStore.fetchTransactionsByDateRange(start, end);
};
</script>

<style scoped>
/* Custom scrollbar styling */
.scrollbar::-webkit-scrollbar {
  width: 6px;
}

.scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.scrollbar::-webkit-scrollbar-thumb {
  background-color: rgb(209, 213, 219);
  border-radius: 3px;
}

.dark .scrollbar::-webkit-scrollbar-thumb {
  background-color: rgb(75, 85, 99);
}

/* Animation for slide-in-up */
@keyframes slide-in-up {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.animate-slide-in-up {
  animation: slide-in-up 0.3s ease-out;
}
</style>
