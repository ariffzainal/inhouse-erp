<template>
  <div class="max-w-7xl mx-auto py-8">
    <!-- Welcome Card -->
    <div class="card mb-6">
      <h2 class="text-3xl font-bold text-dark-neutral mb-2">
        Welcome, {{ authStore.user?.full_name }}! 👋
      </h2>
      <p class="text-dark-neutral">
        You're successfully logged in to the TSB & TPS ERP Platform
        <span v-if="authStore.user?.current_company_name"> for {{ authStore.user?.current_company_name }}</span>.
      </p>
    </div>

    <!-- User Info Grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      <!-- Company Name Card -->
      <div class="card">
        <div class="text-sm text-dark-neutral/70 mb-1">Current Company</div>
        <div class="text-lg font-semibold text-primary">
          {{ authStore.user?.current_company_name || 'N/A' }}
        </div>
      </div>

      <!-- Email Card -->
      <div class="card">
        <div class="text-sm text-dark-neutral/70 mb-1">Email</div>
        <div class="text-lg font-semibold text-dark-neutral">
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
          <span
            class="w-2 h-2 rounded-full mr-2"
            :class="authStore.user?.is_active ? 'bg-green-500' : 'bg-red-500'"
          ></span>
          <span
            class="text-lg font-semibold"
            :class="authStore.user?.is_active ? 'text-green-600' : 'text-red-600'"
          >
            {{ authStore.user?.is_active ? 'Active' : 'Inactive' }}
          </span>
        </div>
      </div>
    </div>

    <!-- Account Details Card -->
    <div class="card">
      <h3 class="text-xl font-bold mb-4">Account Details</h3>
      <div class="space-y-3">
        <div class="flex justify-between py-2 border-b">
          <span class="text-dark-neutral">User ID:</span>
          <span class="font-medium">{{ authStore.user?.id }}</span>
        </div>
        <div class="flex justify-between py-2 border-b">
          <span class="text-dark-neutral">Full Name:</span>
          <span class="font-medium">{{ authStore.user?.full_name }}</span>
        </div>
        <div class="flex justify-between py-2 border-b">
          <span class="text-dark-neutral">Email:</span>
          <span class="font-medium">{{ authStore.user?.email }}</span>
        </div>
        <div class="flex justify-between py-2 border-b">
          <span class="text-dark-neutral">Role:</span>
          <span class="font-medium capitalize">{{ authStore.user?.current_role }}</span>
        </div>
        <div class="flex justify-between py-2 border-b">
          <span class="text-dark-neutral">Account Active:</span>
          <span
            class="font-medium"
            :class="authStore.user?.is_active ? 'text-green-600' : 'text-red-600'"
          >
            {{ authStore.user?.is_active ? 'Yes' : 'No' }}
          </span>
        </div>
        <div class="flex justify-between py-2 border-b">
          <span class="text-dark-neutral">Company Name:</span>
          <span class="font-medium">{{ authStore.user?.current_company_name || 'N/A' }}</span>
        </div>
        <div class="flex justify-between py-2">
          <span class="text-dark-neutral">Created At:</span>
          <span class="font-medium">{{ formatDate(authStore.user?.created_at) }}</span>
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

// handleLogout is now handled by MainLayout, but kept here for local testing if needed
// const handleLogout = () => {
//   authStore.logout()
//   router.push('/login')
// }

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>
