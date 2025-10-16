<template>
  <div class="min-h-screen bg-light-neutral flex flex-col">
    <!-- Top Navigation Bar -->
    <nav class="bg-white shadow-md">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <div class="flex justify-between items-center">
          <!-- Logo/App Name -->
          <router-link to="/dashboard" class="text-2xl font-bold text-primary hover:text-primary/90">TSB & TPS ERP Platform</router-link>
          
          <!-- ERP Modules (Top Nav) -->
          <div class="flex items-center space-x-4">
            <!-- These buttons will be dynamically rendered based on user roles/subscriptions -->
            <router-link to="/dashboard" class="text-dark-neutral hover:text-primary font-medium px-3 py-2 rounded-md">Home</router-link>
            <router-link to="/accounting" class="text-dark-neutral hover:text-primary font-medium px-3 py-2 rounded-md">Accounting</router-link>
            <router-link to="/inventory" class="text-dark-neutral hover:text-primary font-medium px-3 py-2 rounded-md">Inventory</router-link>
            <router-link to="/hrm" class="text-dark-neutral hover:text-primary font-medium px-3 py-2 rounded-md">HRM</router-link>
            <!-- Add other ERP modules here -->
          </div>

          <!-- User & Company Selector -->
          <div class="flex items-center gap-4">
            <!-- Company Selector Dropdown -->
            <div class="relative" @mouseleave="showCompanyDropdown = false">
              <button 
                @click="showCompanyDropdown = !showCompanyDropdown" 
                @mouseenter="showCompanyDropdown = true"
                class="bg-primary text-white px-4 py-2 rounded-md flex items-center hover:bg-primary/90 transition-colors duration-200"
              >
                {{ authStore.user?.default_company_name || 'Select Company' }}
                <svg class="ml-2 -mr-0.5 h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </button>
              <div v-if="showCompanyDropdown" class="absolute right-0 mt-2 w-64 bg-white rounded-md shadow-lg py-1 z-20 border border-light-neutral">
                <div class="px-4 py-2 text-xs text-gray-400 border-b border-light-neutral">Current Organization</div>
                <router-link 
                  :to="{ name: 'company-settings', params: { companyId: authStore.user?.current_company_id } }"
                  class="block px-4 py-2 text-sm text-dark-neutral hover:bg-light-neutral"
                  @click="showCompanyDropdown = false"
                >
                  <span class="font-semibold">{{ authStore.user?.current_company_name }}</span>
                  <span class="text-xs text-gray-500 ml-2">(Settings)</span>
                </router-link>
                <router-link 
                  to="/subscription-billing" 
                  class="block px-4 py-2 text-sm text-dark-neutral hover:bg-light-neutral"
                  @click="showCompanyDropdown = false"
                >
                  Subscription and billing
                </router-link>
                
                <div class="px-4 py-2 text-xs text-gray-400 border-t border-b border-light-neutral mt-1">Your Organizations</div>
                <router-link 
                  v-for="company in authStore.userCompanies" 
                  :key="company.id" 
                  :to="{ name: 'dashboard' }" # Will navigate to dashboard and trigger company switch
                  @click="handleCompanySwitch(company.id)"
                  class="block px-4 py-2 text-sm text-dark-neutral hover:bg-light-neutral"
                >
                  {{ company.display_name }}
                </router-link>
                <router-link 
                  to="/add-new-organization" 
                  class="block px-4 py-2 text-sm text-primary hover:bg-light-neutral font-medium border-t border-light-neutral mt-1"
                  @click="showCompanyDropdown = false"
                >
                  + Add new organization
                </router-link>
              </div>
            </div>

            <!-- Profile Icon (replaces email) -->
            <router-link to="/profile" class="text-dark-neutral hover:text-primary">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 0a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </router-link>
            <button @click="handleLogout" class="bg-accent text-white px-4 py-2 rounded-md hover:bg-accent/90 transition-colors duration-200">
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content Area (Side Panel + Router View) -->
    <div class="flex flex-grow">
      <!-- Side Panel/Menu -->
      <aside class="w-64 bg-white shadow-lg p-4 border-r border-light-neutral">
        <h3 class="text-lg font-semibold text-dark-neutral mb-4">Module Functions</h3>
        <!-- Placeholder for dynamic side menu items -->
        <nav class="space-y-2">
          <a href="#" class="block text-dark-neutral hover:text-primary">Function 1</a>
          <a href="#" class="block text-dark-neutral hover:text-primary">Function 2</a>
          <a href="#" class="block text-dark-neutral hover:text-primary">Function 3</a>
        </nav>
      </aside>

      <!-- Main Content Area -->
      <main class="flex-grow p-8">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterView, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const showCompanyDropdown = ref(false)

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const handleCompanySwitch = async (companyId) => {
  if (authStore.user?.current_company_id !== companyId) {
    const success = await authStore.switchCompany(companyId)
    if (success) {
      // Optionally, refresh the page or re-fetch data for the new company context
      router.go(0) // Reloads the current route to reflect new company context
    }
  }
  showCompanyDropdown.value = false
}

onMounted(() => {
  // Ensure user and companies are fetched when layout mounts
  if (!authStore.user) {
    authStore.fetchUser()
  }
  if (authStore.userCompanies.length === 0) {
    authStore.fetchUserCompanies()
  }
})
</script>

<style scoped>
/* Add any specific styles for the layout here if needed */
</style>
