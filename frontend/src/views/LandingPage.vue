<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-indigo-50 via-white to-cyan-50 dark:from-gray-900 dark:via-black dark:to-gray-800 font-inter text-gray-800 dark:text-gray-200">
    <div class="text-center p-8">
      <svg class="w-16 h-16 text-indigo-600 dark:text-indigo-400 mx-auto mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18.75a60.07 60.07 0 0 1 15.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 0 1 3 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 0 0-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 0 1-1.125-1.125V6.375c0-.621.504-1.125 1.125-1.125h.375m18 3.75v.75c0 .414-.336.75-.75.75h-.75a.75.75 0 0 1-.75-.75v-.75m0 0h.375c.621 0 1.125.504 1.125 1.125v.75c0 .621-.504 1.125-1.125 1.125h-.375m-1.5-3h.75a.75.75 0 0 0 .75-.75v-.75a.75.75 0 0 0-.75-.75h-.75M3 12h18M3 15h18" />
        </svg>

      <h1 class="text-4xl md:text-5xl font-extrabold mb-3">
        Welcome to <span class="text-indigo-600 dark:text-indigo-400">Quid.</span>
      </h1>
      <p class="text-lg md:text-xl mb-8 text-gray-600 dark:text-gray-400">
        Take control of your finances effortlessly.
      </p>

      <div class="space-x-4">
        <router-link
          to="/login"
          class="px-6 py-3 bg-indigo-600 text-white rounded-lg shadow hover:bg-indigo-700 transition duration-300 ease-in-out text-base font-medium"
        >
          Login
        </router-link>
        <router-link
          to="/register"
          class="px-6 py-3 bg-gray-200 text-gray-800 rounded-lg shadow hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600 transition duration-300 ease-in-out text-base font-medium"
        >
          Register
        </router-link>
      </div>
    </div>

    </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';

</script>

<style scoped>
.font-inter {
  font-family: 'Inter', sans-serif;
}
</style>

