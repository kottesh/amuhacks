<template>
  <AuthLayout>
    <h2 class="text-xl font-semibold text-center text-gray-700 dark:text-gray-300 mb-6">
      Login to your Account
    </h2>

    <form @submit.prevent="handleLogin" class="space-y-5">
      <div>
        <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Email Address</label>
        <div class="relative rounded-md shadow-sm">
          <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
            <EnvelopeIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
          </div>
          <input
            v-model="email"
            type="email"
            name="email"
            id="email"
            required
            class="block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 py-2.5 pl-10 pr-3 text-gray-900 dark:text-white placeholder:text-gray-400 dark:placeholder:text-gray-500 focus:ring-2 focus:ring-inset focus:ring-indigo-600 dark:focus:ring-indigo-500 sm:text-sm sm:leading-6 transition duration-150 ease-in-out"
            placeholder="you@example.com"
          />
        </div>
        <p v-if="!isEmailValid && email" class="mt-1 text-xs text-red-600 dark:text-red-400">Please enter a valid email address.</p>
      </div>

      <div>
        <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Password</label>
        <div class="relative rounded-md shadow-sm">
           <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
            <LockClosedIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
          </div>
          <input
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            name="password"
            id="password"
            required
            minlength="8"
            class="block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 py-2.5 pl-10 pr-10 text-gray-900 dark:text-white placeholder:text-gray-400 dark:placeholder:text-gray-500 focus:ring-2 focus:ring-inset focus:ring-indigo-600 dark:focus:ring-indigo-500 sm:text-sm sm:leading-6 transition duration-150 ease-in-out"
            placeholder="********"
          />
          <button type="button" @click="togglePasswordVisibility" class="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <component :is="showPassword ? EyeSlashIcon : EyeIcon" class="h-5 w-5" aria-hidden="true" />
          </button>
        </div>
         <p v-if="password && password.length < 8" class="mt-1 text-xs text-red-600 dark:text-red-400">Password must be at least 8 characters.</p>
      </div>

      <div v-if="authStore.error" class="p-3 bg-red-100 dark:bg-red-900 border border-red-300 dark:border-red-700 rounded-md text-sm text-red-700 dark:text-red-200">
        <ExclamationTriangleIcon class="h-5 w-5 inline mr-1.5 align-text-bottom" aria-hidden="true" />
        {{ authStore.error }}
      </div>

       <div v-if="authStore.successMessage" class="p-3 bg-green-100 dark:bg-green-900 border border-green-300 dark:border-green-700 rounded-md text-sm text-green-700 dark:text-green-200">
         <CheckCircleIcon class="h-5 w-5 inline mr-1.5 align-text-bottom" aria-hidden="true" />
        {{ authStore.successMessage }}
      </div>

      <div>
        <button
          type="submit"
          :disabled="authStore.isLoading || !isFormValid"
          class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-2.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:opacity-50 disabled:cursor-not-allowed transition duration-150 ease-in-out"
        >
          <svg v-if="authStore.isLoading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ authStore.isLoading ? 'Logging in...' : 'Login' }}
        </button>
      </div>
    </form>

    <p class="mt-6 text-center text-sm text-gray-500 dark:text-gray-400">
      Don't have an account?
      {{ ' ' }}
      <router-link to="/register" class="font-semibold leading-6 text-indigo-600 hover:text-indigo-500 dark:text-indigo-400 dark:hover:text-indigo-300">
        Register here
      </router-link>
    </p>
  </AuthLayout>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue';
import { useRouter, RouterLink } from 'vue-router';
import { useAuthStore } from '@/stores/authStore'; // Adjust path as needed
import AuthLayout from '@/components/AuthLayout.vue'; // Adjust path as needed
import { EnvelopeIcon, LockClosedIcon, EyeIcon, EyeSlashIcon, ExclamationTriangleIcon, CheckCircleIcon } from '@heroicons/vue/24/outline'; // Using outline icons

const router = useRouter();
const authStore = useAuthStore();

// Form state
const email = ref('');
const password = ref('');
const showPassword = ref(false);

// Validation computed properties
const isEmailValid = computed(() => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value));
const isPasswordValid = computed(() => password.value.length >= 8);
const isFormValid = computed(() => isEmailValid.value && isPasswordValid.value);

// Methods
const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

const handleLogin = async () => {
  if (!isFormValid.value) return; // Prevent submission if form is invalid

  // Clear previous messages
  authStore.clearMessages();

  const success = await authStore.login(email.value, password.value);
  if (success) {
    // Redirect to dashboard or home page after successful login
    // Optional: Show success message briefly before redirecting
    // authStore.setSuccessMessage('Login successful! Redirecting...');
    // setTimeout(() => {
         router.push('/dashboard'); // Or your desired route
    // }, 1000);
  }
  // Error message is handled reactively via the store's state
};

// Clear error/success messages when the component is unmounted
onUnmounted(() => {
  authStore.clearMessages();
});
</script>

