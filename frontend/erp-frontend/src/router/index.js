import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import LoginView from '@/views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login'  // Redirect root to login
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { requiresGuest: true }  // Only accessible if NOT logged in
    },
    // We'll add more routes here (register, dashboard, etc.)
  ],
})

// Navigation guard - checks authentication before each route
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // Check if route requires authentication
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // Not logged in, redirect to login
    next('/login')
  } 
  // Check if route requires guest (login/register pages)
  else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    // Already logged in, redirect to dashboard
    next('/dashboard')
  } 
  else {
    // All good, proceed
    next()
  }
})

export default router