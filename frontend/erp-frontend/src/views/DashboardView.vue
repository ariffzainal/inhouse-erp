<template>
  <div class="min-h-screen bg-light-neutral">
    <!-- Navigation Bar -->
    <nav class="bg-white shadow-md">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <div class="flex justify-between items-center">
          <h1 class="text-2xl font-bold text-primary">TSB & TPS ERP Platform</h1>
          <div class="flex items-center gap-4">
            <span class="text-dark-neutral">{{ authStore.user?.email }}</span>
            <button @click="handleLogout" class="bg-accent text-white px-4 py-2 rounded-md hover:bg-accent/90 transition-colors duration-200">
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 py-8">
      <!-- Welcome Card -->
      <div class="card mb-6">
        <h2 class="text-3xl font-bold text-gray-800 mb-2">
          Welcome, {{ authStore.user?.full_name }}! 👋
        </h2>
        <p class="text-gray-600">
          You're successfully logged in to the TSB & TPS ERP Platform
        </p>
      </div>

      <!-- User Info Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <!-- Email Card -->
        <div class="card">
          <div class="text-sm text-gray-500 mb-1">Email</div>
          <div class="text-lg font-semibold text-gray-800">
            {{ authStore.user?.email }}
          </div>
        </div>

        <!-- Role Card -->
        <div class="card">
          <div class="text-sm text-dark-neutral/70 mb-1">Role</div>
          <div class="text-lg font-semibold text-primary">
            {{ authStore.user?.role }}
          </div>
        </div>

        <!-- Status Card -->
        <div class="card">
          <div class="text-sm text-dark-neutral/70 mb-1">Account Status</div>
          <div class="flex items-center">
            <span class="w-2 h-2 bg-primary rounded-full mr-2"></span>
            <span class="text-lg font-semibold text-primary">Active</span>
          </div>
        </div>
      </div>

      <!-- Account Details Card -->
      <div class="card">
        <h3 class="text-xl font-bold mb-4">Account Details</h3>
        <div class="space-y-3">
          <div class="flex justify-between py-2 border-b">
            <span class="text-gray-600">User ID:</span>
            <span class="font-medium">{{ authStore.user?.id }}</span>
          </div>
          <div class="flex justify-between py-2 border-b">
            <span class="text-gray-600">Full Name:</span>
            <span class="font-medium">{{ authStore.user?.full_name }}</span>
          </div>
          <div class="flex justify-between py-2 border-b">
            <span class="text-gray-600">Email:</span>
            <span class="font-medium">{{ authStore.user?.email }}</span>
          </div>
          <div class="flex justify-between py-2 border-b">
            <span class="text-gray-600">Role:</span>
            <span class="font-medium capitalize">{{ authStore.user?.role }}</span>
          </div>
          <div class="flex justify-between py-2 border-b">
            <span class="text-dark-neutral">Account Active:</span>
            <span class="font-medium text-primary">{{ authStore.user?.is_active ? 'Yes' : 'No' }}</span>
          </div>
          <div class="flex justify-between py-2">
            <span class="text-gray-600">Created At:</span>
            <span class="font-medium">{{ formatDate(authStore.user?.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>
