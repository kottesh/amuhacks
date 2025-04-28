<template>
  <section
    class="bg-white dark:bg-gray-800 rounded-lg shadow-lg h-full flex flex-col transition-all duration-300 ease-in-out"
  >
    <div class="p-5 border-b border-gray-200 dark:border-gray-700">
      <h2 class="text-xl font-semibold text-gray-800 dark:text-gray-200">
        Recent Transactions
      </h2>
    </div>
    <div
      v-if="transactions.length > 0"
      class="flex-grow overflow-y-auto p-5 space-y-3 max-h-[calc(100vh-16rem)] custom-scrollbar"
    >
      <TransactionItem
        v-for="tx in transactions"
        :key="tx.id"
        :transaction="tx"
      />
    </div>
    <p v-else class="text-center text-gray-500 dark:text-gray-400 py-10 px-5">
      No recent transactions found.
    </p>
  </section>
</template>

<script setup>
import TransactionItem from './TransactionItem.vue';

defineProps({
  transactions: {
    type: Array,
    required: true,
  },
});
</script>

<style scoped>
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
