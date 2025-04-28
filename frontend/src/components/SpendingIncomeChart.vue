<template>
  <section
    class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-5 transition-all duration-300 ease-in-out"
  >
    <h2 class="text-xl font-semibold text-gray-800 dark:text-gray-200 mb-4">
      Spending & Income (Last 7 Days)
    </h2>
    <div
      v-if="isLoadingChart"
      class="text-center py-10 text-gray-500 dark:text-gray-400"
    >
      Loading chart data...
    </div>
    <div v-else-if="chartDataReady" class="h-64 sm:h-72">
      <Line :data="chartData" :options="chartOptions" />
    </div>
    <p v-else class="text-center text-gray-500 dark:text-gray-400 py-10">
      Not enough transaction data for chart.
    </p>
  </section>
</template>

<script setup>
import { computed } from 'vue';
import { useDataStore } from '@/stores/dataStore';
import { Line } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Filler,
} from 'chart.js';
import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc';

dayjs.extend(utc);

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Filler,
);

const dataStore = useDataStore();

const isLoadingChart = computed(() => dataStore.isLoadingChart);

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

const chartData = computed(() => {
  const labels = [];
  const incomeData = [];
  const expenseData = [];
  const daysMap = new Map();

  const todayUTC = dayjs.utc();

  for (let i = 6; i >= 0; i--) {
    const date = todayUTC.subtract(i, 'day');
    const formattedDate = date.format('YYYY-MM-DD');
    const label = date.format('ddd');
    labels.push(label);
    daysMap.set(formattedDate, { income: 0, expense: 0 });
  }

  dataStore.chartTransactions.forEach((tx) => {
    const parsedDate = dayjs(tx.date);
    if (!parsedDate.isValid()) {
      console.warn(`Invalid transaction date for tx.id=${tx.id}:`, tx.date);
      return;
    }
    const dateKey = parsedDate.utc().format('YYYY-MM-DD');

    if (daysMap.has(dateKey)) {
      const dayTotal = daysMap.get(dateKey);
      if (tx.type === 'INCOME') {
        dayTotal.income += tx.amount;
      } else if (tx.type === 'EXPENSE') {
        dayTotal.expense += tx.amount;
      }
    }
  });

  daysMap.forEach((totals) => {
    incomeData.push(totals.income);
    expenseData.push(totals.expense);
  });

  return {
    labels,
    datasets: [
      {
        label: 'Income',
        backgroundColor: 'rgba(16, 185, 129, 0.2)',
        borderColor: 'rgb(16, 185, 129)',
        data: incomeData,
        tension: 0.3,
        fill: true,
      },
      {
        label: 'Expense',
        backgroundColor: 'rgba(239, 68, 68, 0.2)',
        borderColor: 'rgb(239, 68, 68)',
        data: expenseData,
        tension: 0.3,
        fill: true,
      },
    ],
  };
});

const chartDataReady = computed(() => {
  return dataStore.chartTransactions.length > 0;
});

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
      labels: {
        color: document.documentElement.classList.contains('dark') ? '#e5e7eb' : '#4b5563',
        font: {
          family: 'Inter, sans-serif',
        },
      },
    },
    tooltip: {
      mode: 'index',
      intersect: false,
      backgroundColor: document.documentElement.classList.contains('dark')
        ? 'rgba(31, 41, 55, 0.9)'
        : 'rgba(255, 255, 255, 0.9)',
      titleColor: document.documentElement.classList.contains('dark') ? '#f3f4f6' : '#1f2937',
      bodyColor: document.documentElement.classList.contains('dark') ? '#d1d5db' : '#374151',
      borderColor: document.documentElement.classList.contains('dark') ? '#4b5563' : '#e5e7eb',
      borderWidth: 1,
      padding: 10,
      callbacks: {
        label: function (context) {
          let label = context.dataset.label || '';
          if (label) {
            label += ': ';
          }
          if (context.parsed.y !== null) {
            label += formatCurrency(context.parsed.y, dataStore.accounts[0]?.currency_code || 'INR');
          }
          return label;
        },
      },
    },
  },
  scales: {
    x: {
      grid: {
        display: false,
      },
      ticks: {
        color: document.documentElement.classList.contains('dark') ? '#9ca3af' : '#6b7280',
        font: { family: 'Inter, sans-serif' },
      },
      border: {
        color: document.documentElement.classList.contains('dark') ? '#4b5563' : '#e5e7eb',
      },
    },
    y: {
      grid: {
        color: document.documentElement.classList.contains('dark') ? '#374151' : '#e5e7eb',
        drawBorder: false,
      },
      ticks: {
        color: document.documentElement.classList.contains('dark') ? '#9ca3af' : '#6b7280',
        font: { family: 'Inter, sans-serif' },
        callback: function (value) {
          return formatCurrency(value, dataStore.accounts[0]?.currency_code || 'INR', true);
        },
      },
      border: {
        display: false,
      },
    },
  },
}));
</script>
