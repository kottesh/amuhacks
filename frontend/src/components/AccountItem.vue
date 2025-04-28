<template>
  <div
    class="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:shadow-lg hover:scale-[1.02] transition-all duration-200 ease-in-out bg-gray-50 dark:bg-gray-700/50"
  >
    <div class="flex justify-between items-center mb-1">
      <span class="font-medium text-gray-900 dark:text-white truncate">{{ account.name }}</span>
      <BanknotesIcon
        class="h-5 w-5 text-indigo-500 dark:text-indigo-400 flex-shrink-0 ml-2"
      />
    </div>
    <p class="text-sm text-gray-500 dark:text-gray-400 mb-2">{{ account.type }}</p>
    <p class="text-lg font-semibold text-gray-900 dark:text-white">
      {{ formatCurrency(account.balance, account.currency_code) }}
    </p>
  </div>
</template>

<script setup>
import { BanknotesIcon } from '@heroicons/vue/24/outline';
import { computed } from 'vue';
import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc';
import relativeTime from 'dayjs/plugin/relativeTime';
import customParseFormat from 'dayjs/plugin/customParseFormat';

dayjs.extend(utc);
dayjs.extend(relativeTime);
dayjs.extend(customParseFormat);

const props = defineProps({
  account: {
    type: Object,
    required: true,
  },
});

const formatCurrency = (value, currencyCode = 'INR', compact = false) => {
  if (value === null || value === undefined) return '';
  const options = {
    style: 'currency',
    currency: currencyCode || 'INR', // Default to INR if not provided
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  };
  if (compact) {
    options.notation = 'compact';
    options.minimumFractionDigits = 0; // Less precision needed for compact axis labels
    options.maximumFractionDigits = 1;
  }
  try {
    return new Intl.NumberFormat('en-IN', options).format(value); // Use en-IN for Indian Rupee formatting
  } catch (e) {
    // Fallback for invalid currency code or other errors
    console.warn('Currency formatting failed:', e);
    options.currency = 'INR'; // Fallback to INR
    return new Intl.NumberFormat('en-IN', options).format(value);
  }
};
</script>
