<template>
  <div class="min-h-screen flex items-center justify-center bg-dark-neutral px-4 py-8">
    <div class="max-w-md w-full">
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-light-neutral mb-2 drop-shadow-md">TSB & TPS ERP Platform</h1>
        <p class="text-light-neutral drop-shadow-sm">Create your account</p>
      </div>

      <div class="card border border-light-neutral shadow-xl">
        <h2 class="text-2xl font-semibold mb-6 text-dark-neutral">Register</h2>

        <div v-if="authStore.error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
          <span>{{ authStore.error }}</span>
        </div>

        <form @submit.prevent="handleRegister" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-dark-neutral mb-2">Company or Brand Display Name</label>
            <input v-model="form.company_display_name" type="text" required placeholder="Your Company/Brand Display Name" class="input-field" :disabled="authStore.loading" />
          </div>

          <div>
            <label class="block text-sm font-medium text-dark-neutral mb-2">Company Legal Name</label>
            <input v-model="form.company_legal_name" type="text" required placeholder="Your Company Sdn Bhd" class="input-field" :disabled="authStore.loading" />
          </div>

          <div>
            <label class="block text-sm font-medium text-dark-neutral mb-2">Business Registration Number</label>
            <input v-model="form.business_registration_number" type="text" required placeholder="1234567-X" class="input-field" :disabled="authStore.loading" />
          </div>

          <div>
            <label class="block text-sm font-medium text-dark-neutral mb-2">Full Name</label>
            <input v-model="form.full_name" type="text" required placeholder="John Doe" class="input-field" :disabled="authStore.loading" />
          </div>

          <div>
            <label class="block text-sm font-medium text-dark-neutral mb-2">Email</label>
            <input v-model="form.email" type="email" required placeholder="you@example.com" class="input-field" :disabled="authStore.loading" />
          </div>

          <div>
            <label class="block text-sm font-medium text-dark-neutral mb-2">Password</label>
            <input v-model="form.password" type="password" required placeholder="Min 8 characters" class="input-field" :disabled="authStore.loading" />
          </div>


          <button type="submit" class="w-full bg-primary text-white py-3 text-lg rounded-lg hover:bg-primary/90 transition-colors duration-200" :disabled="authStore.loading">
            <span v-if="!authStore.loading">Create Account</span>
            <span v-else>Creating...</span>
          </button>
        </form>

        <div class="mt-6 text-center">
          <p class="text-dark-neutral">
            Already have an account?
            <router-link to="/login" class="text-primary hover:text-accent font-medium">Login here</router-link>
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
  company_display_name: '',
  company_legal_name: '',
  business_registration_number: '',
  email: '',
  full_name: '',
  password: ''
})

const handleRegister = async () => {
  const success = await authStore.register(form.value)
  if (success) {
    router.push('/dashboard')
  }
}
</script>
