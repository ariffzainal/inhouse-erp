import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import MainLayout from '@/layouts/MainLayout.vue' // Import the new layout
import LoginView from '@/views/LoginView.vue'
import DashboardView from '@/views/DashboardView.vue'
import RegisterView from '@/views/RegisterView.vue'
import CompanySettingsView from '@/views/CompanySettingsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { requiresGuest: true }  // Only accessible if NOT logged in
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      meta: { requiresGuest: true }
    },
    {
      path: '/', // This will be the parent route for authenticated users
      component: MainLayout,
      meta: { requiresAuth: true },
      children: [
        {
          path: '', // Default child route for '/' when authenticated
          name: 'home-dashboard',
          redirect: '/dashboard'
        },
        {
          path: 'dashboard',
          name: 'dashboard',
          component: DashboardView,
        },
        {
          path: 'company-settings/:companyId?',
          name: 'company-settings',
          component: CompanySettingsView,
        }
        // Other authenticated routes will go here
      ]
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
  // If trying to access '/' and authenticated, redirect to dashboard
  else if (to.path === '/' && authStore.isAuthenticated) {
    next('/dashboard')
  }
  else {
    // All good, proceed
    next()
  }
})

export default router
