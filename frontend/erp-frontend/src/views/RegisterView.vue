<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 to-emerald-100 px-4 py-8">
    <div class="max-w-md w-full">
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-primary mb-2">TSB & TPS ERP Platform</h1>
        <p class="text-gray-600">Create your account</p>
      </div>

      <div class="card">
        <h2 class="text-2xl font-semibold mb-6 text-gray-800">Register</h2>

        <div v-if="authStore.error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
          <span>{{ authStore.error }}</span>
        </div>

        <form @submit.prevent="handleRegister" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Full Name</label>
            <input v-model="form.full_name" type="text" required placeholder="John Doe" class="input-field" :disabled="authStore.loading" />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
            <input v-model="form.email" type="email" required placeholder="you@example.com" class="input-field" :disabled="authStore.loading" />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Password</label>
            <input v-model="form.password" type="password" required placeholder="Min 8 characters" class="input-field" :disabled="authStore.loading" />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Role</label>
            <select v-model="form.role" class="input-field" :disabled="authStore.loading">
              <option value="viewer">Viewer</option>
              <option value="inventory_staff">Inventory Staff</option>
              <option value="pos_staff">POS Staff</option>
              <option value="accountant">Accountant</option>
              <option value="manager">Manager</option>
              <option value="admin">Admin</option>
            </select>
          </div>

          <button type="submit" class="w-full btn-primary py-3 text-lg" :disabled="authStore.loading">
            <span v-if="!authStore.loading">Create Account</span>
            <span v-else>Creating...</span>
          </button>
        </form>

        <div class="mt-6 text-center">
          <p class="text-gray-600">
            Already have an account?
            <router-link to="/login" class="text-primary hover:text-primary/80 font-medium">Login here</router-link>
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

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  email: '',
  full_name: '',
  password: '',
  role: 'viewer'
})

const handleRegister = async () => {
  const success = await authStore.register(form.value)
  if (success) {
    router.push('/dashboard')
  }
}
</script>