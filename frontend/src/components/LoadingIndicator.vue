<template>
  <div
    class="text-center py-10 text-gray-600 dark:text-gray-400"
  >
    <svg
      class="animate-spin h-8 w-8 text-indigo-600 dark:text-indigo-400 mx-auto mb-3"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        class="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        stroke-width="4"
      ></circle>
      <path
        class="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      ></path>
    </svg>
    Loading dashboard data...
  </div>
</template>

<script setup>
// No script needed for this simple component
</script>
