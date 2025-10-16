// src/stores/auth.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as apiLogin, register as apiRegister, getCurrentUser, getUserCompanies, selectCompany } from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!token.value)
  const userRole = computed(() => user.value?.current_role || null)
  const isAdmin = computed(() => user.value?.current_role === 'admin')
  const userCompanies = ref([])

  function initAuth() {
    const savedToken = localStorage.getItem('token')
    const savedUser = localStorage.getItem('user')
    const savedCompanies = localStorage.getItem('userCompanies')
    
    if (savedToken && savedUser) {
      token.value = savedToken
      user.value = JSON.parse(savedUser)
      if (savedCompanies) {
        userCompanies.value = JSON.parse(savedCompanies)
      }
    }
  }

  async function login(email, password) {
    loading.value = true
    error.value = null
    
    try {
      const response = await apiLogin(email, password)
      token.value = response.data.access_token
      localStorage.setItem('token', response.data.access_token)
      await fetchUser()
      await fetchUserCompanies()
      return true
    } catch (err) {
      error.value = err.response?.data?.detail || 'Login failed'
      console.error('Login error:', err)
      return false
    } finally {
      loading.value = false
    }
  }

  async function register(userData) {
    loading.value = true
    error.value = null
    
    try {
      // The backend now expects company_name nested within a 'company' object
      const payload = {
        email: userData.email,
        full_name: userData.full_name,
        password: userData.password,
        company: {
          display_name: userData.company_display_name,
          legal_name: userData.company_legal_name,
          business_registration_number: userData.business_registration_number
        }
      };
      await apiRegister(payload);
      return await login(userData.email, userData.password);
    } catch (err) {
      error.value = err.response?.data?.detail || 'Registration failed';
      console.error('Register error:', err);
      return false;
    } finally {
      loading.value = false;
    }
  }

  async function fetchUser() {
    try {
      const response = await getCurrentUser()
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(response.data))
    } catch (err) {
      console.error('Fetch user error:', err)
      logout()
    }
  }

  async function fetchUserCompanies() {
    try {
      const response = await getUserCompanies()
      userCompanies.value = response.data
      localStorage.setItem('userCompanies', JSON.stringify(response.data))
    } catch (err) {
      console.error('Fetch user companies error:', err)
      // Don't logout, just clear companies if there's an error
      userCompanies.value = []
      localStorage.removeItem('userCompanies')
    }
  }

  async function switchCompany(companyId) {
    loading.value = true
    error.value = null
    try {
      const response = await selectCompany(companyId)
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(response.data))
      return true
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to switch company'
      console.error('Switch company error:', err)
      return false
    } finally {
      loading.value = false
    }
  }

  function logout() {
    user.value = null
    token.value = null
    userCompanies.value = []
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('userCompanies')
  }

  function clearError() {
    error.value = null
  }

  return {
    user,
    token,
    loading,
    error,
    isAuthenticated,
    userRole,
    isAdmin,
    userCompanies,
    initAuth,
    login,
    register,
    fetchUser,
    fetchUserCompanies,
    switchCompany,
    logout,
    clearError,
  }
})
