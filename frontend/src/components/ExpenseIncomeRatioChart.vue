<template>
  <section
    class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-5 transition-all duration-300 ease-in-out"
  >
    <h2 class="text-xl font-semibold text-gray-800 dark:text-gray-200 mb-4">
      Expense vs Income Ratio (Last 7 Days)
    </h2>
    <div
      v-if="isLoadingChart"
      class="text-center py-10 text-gray-500 dark:text-gray-400"
    >
      Loading chart data...
    </div>
    <div v-else-if="chartDataReady" class="h-64 sm:h-72 flex justify-center items-center">
      <Doughnut :data="chartData" :options="chartOptions" class="max-w-full max-h-full" />
    </div>
    <p v-else class="text-center text-gray-500 dark:text-gray-400 py-10">
      Not enough transaction data for chart.
    </p>
  </section>
</template>

<script setup>
import { computed } from 'vue';
import { useDataStore } from '@/stores/dataStore';
import { Doughnut } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale,
} from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale, ChartDataLabels);

const dataStore = useDataStore();

const isLoadingChart = computed(() => dataStore.isLoadingChart);

const formatCurrency = (value, currencyCode = 'INR') => {
  if (value === null || value === undefined) return '';
  const options = {
    style: 'currency',
    currency: currencyCode || 'INR',
    minimumFractionDigits: 0, // No decimals needed for tooltips/labels here
    maximumFractionDigits: 0,
  };
  try {
    return new Intl.NumberFormat('en-IN', options).format(value);
  } catch (e) {
    console.warn('Currency formatting failed:', e);
    options.currency = 'INR';
    return new Intl.NumberFormat('en-IN', options).format(value);
  }
};

const totals = computed(() => {
  let totalIncome = 0;
  let totalExpense = 0;

  dataStore.chartTransactions.forEach((tx) => {
    if (tx.type === 'INCOME') {
      totalIncome += tx.amount;
    } else if (tx.type === 'EXPENSE') {
      totalExpense += tx.amount;
    }
  });

  return { totalIncome, totalExpense };
});

const chartDataReady = computed(() => {
  // Require both income and expense to be non-zero for a meaningful ratio chart
  return totals.value.totalIncome > 0 || totals.value.totalExpense > 0;
});

const chartData = computed(() => {
  const { totalIncome, totalExpense } = totals.value;

  return {
    labels: ['Expense', 'Income'],
    datasets: [
      {
        backgroundColor: ['rgb(239, 68, 68)', 'rgb(16, 185, 129)'], // Red for Expense, Green for Income
        data: [totalExpense, totalIncome],
      },
    ],
  };
});

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        color: document.documentElement.classList.contains('dark') ? '#e5e7eb' : '#4b5563',
        font: {
          family: 'Inter, sans-serif',
        },
        padding: 20, // Add padding to legend labels
      },
    },
    tooltip: {
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
          let label = context.label || '';
          if (label) {
            label += ': ';
          }
          const value = context.parsed;
          if (value !== null) {
            label += formatCurrency(value, dataStore.accounts[0]?.currency_code || 'INR');
            // Add percentage
            const total = context.dataset.data.reduce((a, b) => a + b, 0);
            const percentage = total > 0 ? ((value / total) * 100).toFixed(1) + '%' : '0%';
            label += ` (${percentage})`;
          }
          return label;
        },
      },
    },
    datalabels: { // Configure chartjs-plugin-datalabels
      formatter: (value, ctx) => {
        const total = ctx.chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
        const percentage = total > 0 ? ((value / total) * 100).toFixed(1) + '%' : '';
        // Only show percentage if it's reasonably large to avoid clutter
        return parseFloat(percentage) > 5 ? percentage : '';
      },
      color: '#fff', // White text for labels
      font: {
        weight: 'bold',
        family: 'Inter, sans-serif',
      },
      // Display labels only if segment is large enough
      display: function(context) {
        var dataset = context.dataset;
        var value = dataset.data[context.dataIndex];
        return value > 0; // Don't display label for zero value segments
      }
    },
  },
  cutout: '60%', // Make it a doughnut chart
}));
</script>
