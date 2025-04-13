import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios' // Import axios

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:4321/api/v1/' // Provide a fallback

console.log(`API Base URL set to: ${API_BASE_URL}`) // Log the URL being used

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref(localStorage.getItem('accessToken') || null)
  const refreshToken = ref(localStorage.getItem('refreshToken') || null)
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const isLoading = ref(false)
  const error = ref(null)
  const successMessage = ref(null)

  const isAuthenticated = computed(() => !!accessToken.value)

  // Action: Login
  async function login(email, password) {
    isLoading.value = true
    error.value = null
    successMessage.value = null

    const params = new URLSearchParams()
    params.append('username', email) // FastAPI expects 'username' field for email
    params.append('password', password)

    try {
      const response = await apiClient.post('/auth/login', params, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      })
      const data = response.data

      if (data && data.access_token) {
        accessToken.value = data.access_token
        refreshToken.value = data.refresh_token
        localStorage.setItem('accessToken', data.access_token)
        localStorage.setItem('refreshToken', data.refresh_token)
        return true
      }
      return false
    } catch (err) {
      console.error('Login Error:', err)
      const detail = err.response?.data?.detail
      const message = detail || err.message || 'Login failed.'
      error.value = typeof detail === 'object' ? JSON.stringify(detail) : message
      return false
    } finally {
      isLoading.value = false
    }
  }

  // Action: Register
  async function register(email, password, firstName, lastName) {
    isLoading.value = true
    error.value = null
    successMessage.value = null

    const userData = {
      email: email,
      password: password,
      first_name: firstName,
      last_name: lastName,
    }

    try {
      const response = await apiClient.post('/auth/register', userData)
      const data = response.data

      if (data && data.id) {
        return true
      }
      return false
    } catch (err) {
      console.error('Registration Error:', err)
      const detail = err.response?.data?.detail
      const message = detail || err.message || 'Registration failed.'
      error.value = typeof detail === 'object' ? JSON.stringify(detail) : message
      return false
    } finally {
      isLoading.value = false
    }
  }

  // Action: Refresh Token
  async function refreshTokenAction() {
    if (!refreshToken.value) {
      logout()
      return false
    }

    try {
      const response = await apiClient.post(
        '/auth/refresh',
        { refresh_token: refreshToken.value },
        {
          _skipInterceptor: true,
          headers: { 'Content-Type': 'application/json' },
        },
      )
      const data = response.data

      if (data && data.access_token) {
        accessToken.value = data.access_token
        if (data.refresh_token) {
          refreshToken.value = data.refresh_token
          localStorage.setItem('refreshToken', data.refresh_token)
        }
        localStorage.setItem('accessToken', data.access_token)
        console.log('Token refreshed successfully.')
        return true
      } else {
        console.error('Refresh token endpoint did not return access token.')
        logout()
        error.value = 'Session expired. Please login again.'
        return false
      }
    } catch (err) {
      console.error('Token refresh failed:', err.response?.data?.detail || err.message)
      logout()
      error.value = 'Session expired. Please login again.'
      return false
    }
  }

  // Action: Logout
  function logout() {
    accessToken.value = null
    refreshToken.value = null
    user.value = null
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('user')
    clearMessages()
    console.log('User logged out.')
  }

  // Action: Clear error/success messages
  function clearMessages() {
    error.value = null
    successMessage.value = null
  }

  // Action: Set a success message manually
  function setSuccessMessage(message) {
    successMessage.value = message
    error.value = null // Clear error when setting success
  }

  // --- Axios Interceptors ---

  // Request Interceptor: Add token to headers
  apiClient.interceptors.request.use(
    (config) => {
      // Get the latest token value from the ref
      const currentAccessToken = accessToken.value
      // Don't add token to refresh request itself or if skip flag is set
      // Check against the correct refresh endpoint path
      if (currentAccessToken && !config.url.endsWith('/auth/refresh') && !config._skipInterceptor) {
        // Make sure Authorization header is added if not already present
        if (!config.headers.Authorization) {
          config.headers.Authorization = `Bearer ${currentAccessToken}`
        }
      }
      return config
    },
    (error) => {
      return Promise.reject(error)
    },
  )

  apiClient.interceptors.response.use(
    (response) => response, // Simply return successful responses
    async (error) => {
      const originalRequest = error.config

      if (
        error.response?.status === 401 &&
        !originalRequest._retry &&
        !originalRequest.url.endsWith('/auth/refresh')
      ) {
        originalRequest._retry = true // Mark that we're attempting a retry

        console.log('Access token expired or invalid. Attempting refresh...')
        try {
          const refreshed = await refreshTokenAction() // Attempt to refresh the token

          if (refreshed) {
            console.log('Token refresh successful. Retrying original request...')
            // Update the Authorization header of the original request with the NEW token
            originalRequest.headers['Authorization'] = `Bearer ${accessToken.value}`
            // Retry the original request with the new token
            return apiClient(originalRequest)
          } else {
            console.error('Token refresh failed. Original request cannot be retried.')
            return Promise.reject(error) // Reject the original request's promise
          }
        } catch (refreshError) {
          console.error('Error during token refresh attempt:', refreshError)
          return Promise.reject(refreshError)
        }
      }

      const errorMessage = error.response?.data?.detail || error.message || 'An API error occurred.'
      console.error('API Error:', errorMessage, 'Original Request:', originalRequest.url)

      return Promise.reject(error)
    },
  )

  // --- Return ---
  return {
    accessToken,
    refreshToken,
    user,
    isLoading,
    error,
    successMessage,
    isAuthenticated,
    login,
    register,
    logout,
    clearMessages,
    setSuccessMessage,
    refreshTokenAction,
    apiClient,
  }
})
