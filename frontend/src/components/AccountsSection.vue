<template>
  <section
    class="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden transition-all duration-300 ease-in-out"
  >
    <div class="p-5 border-b border-gray-200 dark:border-gray-700">
      <h2 class="text-xl font-semibold text-gray-800 dark:text-gray-200">Your Accounts</h2>
    </div>
    <div class="p-5">
      <div
        v-if="accounts.length > 0"
        class="grid grid-cols-1 md:grid-cols-2 gap-4"
      >
        <AccountItem
          v-for="account in accounts"
          :key="account.id"
          :account="account"
        />
      </div>
      <p v-else class="text-center text-gray-500 dark:text-gray-400 py-4">
        No accounts found. Click the '+' button above to add one!
      </p>
    </div>
  </section>
</template>

<script setup>
import { useDataStore } from '@/stores/dataStore';
import { computed } from 'vue';
import AccountItem from './AccountItem.vue';

const dataStore = useDataStore();

const accounts = computed(() => dataStore.accounts);
</script>
