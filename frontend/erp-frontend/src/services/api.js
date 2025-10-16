// src/services/api.js
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const register = (userData) => {
  return api.post('/api/v1/auth/register', userData)
}

export const login = (email, password) => {
  const formData = new URLSearchParams()
  formData.append('username', email)
  formData.append('password', password)
  
  return api.post('/api/v1/auth/login', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  })
}

export const getCurrentUser = () => {
  return api.get('/api/v1/auth/me')
}

export const getUserCompanies = () => {
  return api.get('/api/v1/companies/')
}

export const selectCompany = (companyId) => {
  return api.post('/api/v1/companies/select', { company_id: companyId })
}

export const testProtected = () => {
  return api.get('/api/v1/auth/protected')
}

export const getCompanyById = (companyId) => {
  return api.get(`/api/v1/companies/${companyId}`)
}

export const updateCompanyProfile = (companyId, companyData) => {
  return api.put(`/api/v1/companies/${companyId}`, companyData)
}

export default api
