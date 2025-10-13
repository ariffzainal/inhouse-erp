import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

// Create Pinia instance
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Initialize auth store (check if user is already logged in)
import { useAuthStore } from './stores/auth'
const authStore = useAuthStore()
authStore.initAuth()

app.mount('#app')