<template>
  <div class="max-w-4xl mx-auto py-8">
    <h1 class="text-3xl font-bold text-dark-neutral mb-6">Company Settings</h1>

    <div v-if="loading" class="text-dark-neutral">Loading company details...</div>
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
      <span>{{ error }}</span>
    </div>
    <div v-else-if="company">
      <div class="card p-6 mb-6">
        <h2 class="text-2xl font-semibold text-dark-neutral mb-4">Organization Details</h2>
        <form @submit.prevent="handleUpdateCompany" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-dark-neutral mb-2">Display Name</label>
            <input v-model="company.display_name" type="text" required class="input-field" />
          </div>
          <div>
            <label class="block text-sm font-medium text-dark-neutral mb-2">Legal Name</label>
            <input v-model="company.legal_name" type="text" required class="input-field" />
          </div>
          <div>
            <label class="block text-sm font-medium text-dark-neutral mb-2">Business Registration Number</label>
            <input v-model="company.business_registration_number" type="text" required class="input-field" />
          </div>
          <!-- Add more fields for other company details as needed from CompanyUpdate schema -->
          
          <button type="submit" class="bg-primary text-white px-4 py-2 rounded-md hover:bg-primary/90 transition-colors duration-200">
            Update Company Profile
          </button>
        </form>
      </div>
    </div>
    <div v-else class="text-dark-neutral">No company data available.</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getCompanyById, updateCompanyProfile } from '@/services/api'

const route = useRoute()
const authStore = useAuthStore()

const company = ref(null)
const loading = ref(false)
const error = ref(null)

const fetchCompanyDetails = async () => {
  loading.value = true
  error.value = null
  try {
    const companyId = route.params.companyId || authStore.user?.current_company_id
    if (!companyId) {
      throw new Error('Company ID not found.')
    }
    const response = await getCompanyById(companyId)
    company.value = response.data
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to fetch company details.'
    console.error('Fetch company details error:', err)
  } finally {
    loading.value = false
  }
}

const handleUpdateCompany = async () => {
  loading.value = true
  error.value = null
  try {
    if (!company.value || !company.value.id) {
      throw new Error('Company data is missing for update.')
    }
    const updatePayload = {
      display_name: company.value.display_name,
      legal_name: company.value.legal_name,
      business_registration_number: company.value.business_registration_number,
      // Add other fields from the form here
    }
    await updateCompanyProfile(company.value.id, updatePayload)
    alert('Company profile updated successfully!')
    // Optionally, refresh user data to reflect any changes in current company name
    await authStore.fetchUser()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to update company profile.'
    console.error('Update company profile error:', err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchCompanyDetails)
</script>

<style scoped>
/* Add any specific styles for the company settings page here */
</style>
