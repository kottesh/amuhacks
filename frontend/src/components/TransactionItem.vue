<template>
  <div
    class="flex justify-between items-center p-3 border-b border-gray-100 dark:border-gray-700/50 last:border-b-0 hover:bg-gray-50 dark:hover:bg-gray-700/30 rounded transition-colors duration-150"
  >
    <div>
      <p class="font-medium text-gray-900 dark:text-white text-sm">
        {{ transaction.description }}
      </p>
      <p class="text-xs text-gray-500 dark:text-gray-400">
        {{ formatDate(transaction.date) }} - {{ transaction.category || 'Uncategorized' }}
      </p>
    </div>
    <span
      :class="[
        transaction.type === 'INCOME'
          ? 'text-green-600 dark:text-green-400'
          : 'text-red-600 dark:text-red-400',
        'font-semibold text-sm flex-shrink-0 ml-2',
      ]"
    >
      {{ formatCurrency(transaction.amount, transaction.currency_code) }}
    </span>
  </div>
</template>

<script setup>
import dayjs from 'dayjs';

const props = defineProps({
  transaction: {
    type: Object,
    required: true,
  },
});

const formatCurrency = (value, currencyCode = 'INR') => {
  if (value === null || value === undefined) return '';
  const options = {
    style: 'currency',
    currency: currencyCode || 'INR',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  };
  try {
    return new Intl.NumberFormat('en-IN', options).format(value);
  } catch (e) {
    console.warn('Currency formatting failed:', e);
    options.currency = 'INR';
    return new Intl.NumberFormat('en-IN', options).format(value);
  }
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  return dayjs(dateString).format('MMM D, YYYY');
};
</script>
