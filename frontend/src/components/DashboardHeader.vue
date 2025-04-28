<template>
  <header
    class="mb-8 flex flex-col sm:flex-row justify-between items-center space-y-4 sm:space-y-0"
  >
    <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
    <div class="flex items-center space-x-3">
      <button
        @click="$emit('open-add-account')"
        title="Add New Account"
        class="p-2 bg-indigo-600 text-white rounded-full shadow-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition duration-300 ease-in-out"
      >
        <PlusIcon class="h-5 w-5" aria-hidden="true" />
      </button>
      <button
        @click="$emit('open-add-transaction')"
        title="Add New Transaction (Quick Add)"
        class="p-2 bg-green-600 text-white rounded-full shadow-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition duration-300 ease-in-out"
      >
        <ChatBubbleLeftEllipsisIcon class="h-5 w-5" aria-hidden="true" />
      </button>
      <button
        @click="$emit('logout')"
        title="Logout"
        class="p-2 bg-red-600 text-white rounded-full shadow-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition duration-300 ease-in-out"
      >
        <ArrowRightOnRectangleIcon class="h-5 w-5" aria-hidden="true" />
      </button>
    </div>
  </header>
</template>

<script setup>
import { PlusIcon, ChatBubbleLeftEllipsisIcon, ArrowRightOnRectangleIcon } from '@heroicons/vue/24/outline';

// Define custom events
defineEmits(['open-add-account', 'open-add-transaction', 'logout']);
</script>
