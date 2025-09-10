<template>
  <div>
    <div class="mb-6">
      <h2 class="text-center text-3xl font-extrabold text-gray-900">
        Reset your password
      </h2>
      <p class="mt-2 text-center text-sm text-gray-600">
        Enter your email address and we'll send you a link to reset your password.
      </p>
    </div>

    <form @submit.prevent="handleSubmit" class="space-y-6">
      <div>
        <label for="email" class="block text-sm font-medium text-gray-700">
          Email address
        </label>
        <div class="mt-1">
          <input
            id="email"
            v-model="form.email"
            name="email"
            type="email"
            autocomplete="email"
            required
            class="input-field"
            :class="{ 'border-red-300': errors.email }"
          />
          <p v-if="errors.email" class="mt-1 text-sm text-red-600">{{ errors.email }}</p>
        </div>
      </div>

      <div v-if="error" class="rounded-md bg-red-50 p-4">
        <div class="text-sm text-red-700">
          {{ error }}
        </div>
      </div>

      <div v-if="successMessage" class="rounded-md bg-green-50 p-4">
        <div class="text-sm text-green-700">
          {{ successMessage }}
        </div>
        <div v-if="developmentResetLink" class="mt-2">
          <p class="text-xs text-green-600">Development only:</p>
          <a 
            :href="developmentResetLink" 
            class="text-xs text-green-600 underline break-all"
            target="_blank"
          >
            {{ developmentResetLink }}
          </a>
        </div>
      </div>

      <div>
        <button
          type="submit"
          :disabled="isLoading"
          class="btn-primary w-full flex justify-center"
          :class="{ 'opacity-50 cursor-not-allowed': isLoading }"
        >
          <svg v-if="isLoading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ isLoading ? 'Sending...' : 'Send reset link' }}
        </button>
      </div>
    </form>

    <div class="mt-6 text-center">
      <RouterLink to="/auth/login" class="text-sm text-primary-600 hover:text-primary-500">
        Back to login
      </RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { RouterLink } from 'vue-router'
import { authAPI } from '@/api/auth'

const form = reactive({
  email: ''
})

const errors = reactive({
  email: ''
})

const error = ref('')
const successMessage = ref('')
const developmentResetLink = ref('')
const isLoading = ref(false)

const validateForm = () => {
  errors.email = ''
  
  if (!form.email) {
    errors.email = 'Email is required'
  } else if (!/\S+@\S+\.\S+/.test(form.email)) {
    errors.email = 'Email is invalid'
  }
  
  return !errors.email
}

const handleSubmit = async () => {
  if (!validateForm()) return
  
  try {
    error.value = ''
    successMessage.value = ''
    developmentResetLink.value = ''
    isLoading.value = true
    
    const response = await authAPI.requestPasswordReset({ email: form.email })
    
    successMessage.value = response.message
    
    // Show development link if provided
    if (response.reset_link) {
      developmentResetLink.value = response.reset_link
    }
    
  } catch (err: any) {
    console.error('Password reset request error:', err)
    if (err.response?.status === 429) {
      error.value = err.response?.data?.detail || 'Too many requests. Please try again later.'
    } else {
      error.value = 'Something went wrong. Please try again.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>