<template>
  <AuthLayout>
    <h2 class="text-xl font-semibold text-center text-gray-700 dark:text-gray-300 mb-6">
      Create your Account
    </h2>

    <form @submit.prevent="handleRegister" class="space-y-5">
        <div class="flex justify-between gap-4">
      <div>
        <label for="firstName" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">First Name</label>
        <div class="relative rounded-md shadow-sm">
          <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
            <UserIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
          </div>
          <input
            v-model="firstName"
            type="text"
            name="firstName"
            id="firstName"
            required
            class="block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 py-2.5 pl-10 pr-3 text-gray-900 dark:text-white placeholder:text-gray-400 dark:placeholder:text-gray-500 focus:ring-2 focus:ring-inset focus:ring-indigo-600 dark:focus:ring-indigo-500 sm:text-sm sm:leading-6 transition duration-150 ease-in-out"
            placeholder="Kamal"
          />
        </div>
         <p v-if="!isFirstNameValid && firstName" class="mt-1 text-xs text-red-600 dark:text-red-400">First name is required.</p>
      </div>

       <div>
        <label for="lastName" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Last Name <span class="text-xs text-gray-500">(Optional)</span></label>
        <div class="relative rounded-md shadow-sm">
          <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
            <UserIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
          </div>
          <input
            v-model="lastName"
            type="text"
            name="lastName"
            id="lastName"
            class="block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 py-2.5 pl-10 pr-3 text-gray-900 dark:text-white placeholder:text-gray-400 dark:placeholder:text-gray-500 focus:ring-2 focus:ring-inset focus:ring-indigo-600 dark:focus:ring-indigo-500 sm:text-sm sm:leading-6 transition duration-150 ease-in-out"
            placeholder="Kannan"
          />
        </div>
      </div>
        </div>
       

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
            placeholder="Choose a strong password"
          />
          <button type="button" @click="togglePasswordVisibility" class="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <component :is="showPassword ? EyeSlashIcon : EyeIcon" class="h-5 w-5" aria-hidden="true" />
          </button>
        </div>
         <p v-if="password && password.length < 8" class="mt-1 text-xs text-red-600 dark:text-red-400">Password must be at least 8 characters.</p>
      </div>

       <div>
        <label for="confirmPassword" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Confirm Password</label>
        <div class="relative rounded-md shadow-sm">
           <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
            <LockClosedIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
          </div>
          <input
            v-model="confirmPassword"
            :type="showConfirmPassword ? 'text' : 'password'"
            name="confirmPassword"
            id="confirmPassword"
            required
            class="block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 py-2.5 pl-10 pr-10 text-gray-900 dark:text-white placeholder:text-gray-400 dark:placeholder:text-gray-500 focus:ring-2 focus:ring-inset focus:ring-indigo-600 dark:focus:ring-indigo-500 sm:text-sm sm:leading-6 transition duration-150 ease-in-out"
            placeholder="Confirm your password"
          />
           <button type="button" @click="toggleConfirmPasswordVisibility" class="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <component :is="showConfirmPassword ? EyeSlashIcon : EyeIcon" class="h-5 w-5" aria-hidden="true" />
          </button>
        </div>
         <p v-if="confirmPassword && password !== confirmPassword" class="mt-1 text-xs text-red-600 dark:text-red-400">Passwords do not match.</p>
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
          {{ authStore.isLoading ? 'Registering...' : 'Register' }}
        </button>
      </div>
    </form>

    <p class="mt-6 text-center text-sm text-gray-500 dark:text-gray-400">
      Already have an account?
      {{ ' ' }}
      <router-link to="/login" class="font-semibold leading-6 text-indigo-600 hover:text-indigo-500 dark:text-indigo-400 dark:hover:text-indigo-300">
        Login here
      </router-link>
    </p>
  </AuthLayout>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue';
import { useRouter, RouterLink } from 'vue-router';
import { useAuthStore } from '@/stores/authStore'; // Adjust path as needed
import AuthLayout from '@/components/AuthLayout.vue'; // Adjust path as needed
// Import UserIcon for name fields
import { UserIcon, EnvelopeIcon, LockClosedIcon, EyeIcon, EyeSlashIcon, ExclamationTriangleIcon, CheckCircleIcon } from '@heroicons/vue/24/outline';

const router = useRouter();
const authStore = useAuthStore();

// Form state
const firstName = ref('');
const lastName = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const showPassword = ref(false);
const showConfirmPassword = ref(false);

// Validation computed properties
const isFirstNameValid = computed(() => firstName.value.trim() !== ''); // First name is required
const isEmailValid = computed(() => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value));
const isPasswordValid = computed(() => password.value.length >= 8);
const doPasswordsMatch = computed(() => password.value === confirmPassword.value && password.value !== '');
// Update form validity check
const isFormValid = computed(() =>
    isFirstNameValid.value &&
    isEmailValid.value &&
    isPasswordValid.value &&
    doPasswordsMatch.value
);

// Methods
const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};
const toggleConfirmPasswordVisibility = () => {
  showConfirmPassword.value = !showConfirmPassword.value;
};

const handleRegister = async () => {
  if (!isFormValid.value) return; // Prevent submission if form is invalid

  // Clear previous messages
   authStore.clearMessages();

  // Call store action with all required fields
  const success = await authStore.register(
      email.value,
      password.value,
      firstName.value.trim(), // Send trimmed first name
      lastName.value.trim() // Send trimmed last name (optional)
  );

  if (success) {
    authStore.setSuccessMessage('Registration successful! Please login.');
    setTimeout(() => {
      router.push('/login');
    }, 2000); // Redirect after 2 seconds
  }
};

onUnmounted(() => {
  authStore.clearMessages();
});

</script>

