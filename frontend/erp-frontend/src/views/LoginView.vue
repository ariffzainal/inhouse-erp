<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 px-4 py-8">
    <!-- Login Card -->
    <div class="max-w-md w-full">
      <!-- Logo/Header -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-primary mb-2">
          🌙 The Skinny Bakers & theprintingshop.co ERP
        </h1>
        <p class="text-gray-600">
          Sign in to your account
        </p>
      </div>

      <!-- Login Form Card -->
      <div class="card">
        <h2 class="text-2xl font-semibold mb-6 text-gray-800">
          Login
        </h2>

        <!-- Error Message -->
        <div v-if="authStore.error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
          <div class="flex items-center">
            <span class="text-xl mr-2">⚠️</span>
            <span>{{ authStore.error }}</span>
          </div>
          <button 
            @click="authStore.clearError" 
            class="text-red-500 hover:text-red-700 text-sm mt-2 underline"
          >
            Dismiss
          </button>
        </div>

        <!-- Login Form -->
        <form @submit.prevent="handleLogin" class="space-y-4">
          <!-- Email Field -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
              Email Address
            </label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              placeholder="admin@erp.com"
              class="input-field"
              :disabled="authStore.loading"
            />
          </div>

          <!-- Password Field -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
              Password
            </label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              required
              placeholder="Enter your password"
              class="input-field"
              :disabled="authStore.loading"
            />
          </div>

          <!-- Remember Me (optional) -->
          <div class="flex items-center justify-between">
            <label class="flex items-center">
              <input type="checkbox" class="rounded border-gray-300 text-primary focus:ring-primary">
              <span class="ml-2 text-sm text-gray-600">Remember me</span>
            </label>
            <a href="#" class="text-sm text-primary hover:text-primary/80">
              Forgot password?
            </a>
          </div>

          <!-- Login Button -->
          <button
            type="submit"
            class="w-full btn-primary py-3 text-lg"
            :disabled="authStore.loading"
          >
            <span v-if="!authStore.loading">Sign In</span>
            <span v-else class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Signing in...
            </span>
          </button>
        </form>

        <!-- Register Link -->
        <div class="mt-6 text-center">
          <p class="text-gray-600">
            Don't have an account?
            <router-link to="/register" class="text-primary hover:text-primary/80 font-medium">
              Register here
            </router-link>
          </p>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Router for navigation
const router = useRouter()

// Auth store for login logic
const authStore = useAuthStore()

// Form data
const form = ref({
  email: '',
  password: ''
})

// Handle login submission
const handleLogin = async () => {
  // Call login function from auth store
  const success = await authStore.login(form.value.email, form.value.password)
  
  if (success) {
    // Login successful! Navigate to dashboard
    console.log('Login successful!')
    router.push('/dashboard')
  } else {
    // Login failed - error is already set in authStore.error
    console.error('Login failed')
  }
}
</script>