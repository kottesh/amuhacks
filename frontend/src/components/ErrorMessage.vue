<template>
  <div
    class="p-4 mb-6 bg-red-100 dark:bg-red-900 border border-red-300 dark:border-red-700 rounded-lg shadow text-sm text-red-700 dark:text-red-200 flex items-center space-x-2"
  >
    <ExclamationTriangleIcon class="h-5 w-5 flex-shrink-0" aria-hidden="true" />
    <span>{{ message }}</span>
  </div>
</template>

<script setup>
import { ExclamationTriangleIcon } from '@heroicons/vue/24/outline';

defineProps({
  message: {
    type: String,
    required: true,
  },
});
</script>
