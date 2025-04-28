<template>
  <div
    class="min-h-screen bg-gradient-to-br from-gray-50 via-gray-100 to-indigo-50 dark:from-gray-800 dark:via-gray-900 dark:to-black p-4 sm:p-6 lg:p-8 font-inter text-gray-800 dark:text-gray-200"
  >
    <div class="max-w-7xl mx-auto">
      <h1 class="text-2xl font-bold text-gray-800 dark:text-gray-200 mb-8 flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-7 h-7 mr-2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3v11.25A2.25 2.25 0 0 0 6 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0 1 18 16.5h-2.25m-7.5 0h7.5m-7.5 0-1 3m8.5-3 1 3m0 0 .5 1.5m-.5-1.5h-9.5m0 0-.5 1.5m.75-9 3-3 2.148 2.148A12.061 12.061 0 0 1 16.5 7.605" />
        </svg>
        All Transactions
      </h1>

      <LoadingIndicator v-if="dataStore.isLoading" />
      <ErrorMessage v-else-if="dataStore.error" :message="dataStore.error" />

      <div v-else class="space-y-6">
        <!-- Filtered Transactions Component will go here -->
        <FilteredTransactions />
      </div>
    </div>
  </div>
</template>

<script setup>
import { onUnmounted } from 'vue'; // Import onUnmounted
import FilteredTransactions from '@/components/FilteredTransactions.vue';
import LoadingIndicator from '@/components/LoadingIndicator.vue'; // Import LoadingIndicator
import ErrorMessage from '@/components/ErrorMessage.vue'; // Import ErrorMessage
import { useDataStore } from '@/stores/dataStore'; // Import dataStore

const dataStore = useDataStore(); // Get dataStore instance

onUnmounted(() => {
  console.log('TransactionsView unmounted, clearing filtered transactions...');
  dataStore.clearFilteredTransactions(); // Call the new action
});
</script>
