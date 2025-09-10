<template>
  <div>
    <div class="mb-6">
      <h2 class="text-center text-3xl font-extrabold text-gray-900">
        Create your account
      </h2>
      <p class="mt-2 text-center text-sm text-gray-600">
        Already have an account?
        <RouterLink to="/auth/login" class="font-medium text-primary-600 hover:text-primary-500">
          Sign in
        </RouterLink>
      </p>
    </div>

    <form @submit.prevent="handleSubmit" class="space-y-6">
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div>
          <label for="first_name" class="block text-sm font-medium text-gray-700">
            First name
          </label>
          <div class="mt-1">
            <input
              id="first_name"
              v-model="form.first_name"
              name="first_name"
              type="text"
              autocomplete="given-name"
              class="input-field"
              :class="{ 'border-red-300': errors.first_name }"
            />
            <p v-if="errors.first_name" class="mt-1 text-sm text-red-600">{{ errors.first_name }}</p>
          </div>
        </div>

        <div>
          <label for="last_name" class="block text-sm font-medium text-gray-700">
            Last name
          </label>
          <div class="mt-1">
            <input
              id="last_name"
              v-model="form.last_name"
              name="last_name"
              type="text"
              autocomplete="family-name"
              class="input-field"
              :class="{ 'border-red-300': errors.last_name }"
            />
            <p v-if="errors.last_name" class="mt-1 text-sm text-red-600">{{ errors.last_name }}</p>
          </div>
        </div>
      </div>

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

      <div>
        <label for="password" class="block text-sm font-medium text-gray-700">
          Password
        </label>
        <div class="mt-1">
          <input
            id="password"
            v-model="form.password"
            name="password"
            type="password"
            autocomplete="new-password"
            required
            class="input-field"
            :class="{ 'border-red-300': errors.password }"
          />
          <p v-if="errors.password" class="mt-1 text-sm text-red-600">{{ errors.password }}</p>
        </div>
        <div class="mt-2">
          <div class="text-sm text-gray-500">
            <ul class="space-y-1">
              <li class="flex items-center space-x-2">
                <span :class="passwordValidation.length ? 'text-green-600' : 'text-gray-400'">
                  {{ passwordValidation.length ? '✓' : '○' }}
                </span>
                <span>At least 8 characters</span>
              </li>
              <li class="flex items-center space-x-2">
                <span :class="passwordValidation.uppercase ? 'text-green-600' : 'text-gray-400'">
                  {{ passwordValidation.uppercase ? '✓' : '○' }}
                </span>
                <span>One uppercase letter</span>
              </li>
              <li class="flex items-center space-x-2">
                <span :class="passwordValidation.lowercase ? 'text-green-600' : 'text-gray-400'">
                  {{ passwordValidation.lowercase ? '✓' : '○' }}
                </span>
                <span>One lowercase letter</span>
              </li>
              <li class="flex items-center space-x-2">
                <span :class="passwordValidation.number ? 'text-green-600' : 'text-gray-400'">
                  {{ passwordValidation.number ? '✓' : '○' }}
                </span>
                <span>One number</span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <div>
        <label for="confirmPassword" class="block text-sm font-medium text-gray-700">
          Confirm Password
        </label>
        <div class="mt-1">
          <input
            id="confirmPassword"
            v-model="form.confirmPassword"
            name="confirmPassword"
            type="password"
            autocomplete="new-password"
            required
            class="input-field"
            :class="{ 'border-red-300': errors.confirmPassword }"
          />
          <p v-if="errors.confirmPassword" class="mt-1 text-sm text-red-600">{{ errors.confirmPassword }}</p>
        </div>
      </div>

      <div v-if="error" class="rounded-md bg-red-50 p-4">
        <div class="text-sm text-red-700">
          {{ error }}
        </div>
      </div>

      <div>
        <button
          type="submit"
          :disabled="isLoading || !isFormValid"
          class="btn-primary w-full flex justify-center"
          :class="{ 'opacity-50 cursor-not-allowed': isLoading || !isFormValid }"
        >
          <svg v-if="isLoading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ isLoading ? 'Creating account...' : 'Create account' }}
        </button>
      </div>
    </form>

    <!-- Divider -->
    <div class="mt-6">
      <div class="relative">
        <div class="absolute inset-0 flex items-center">
          <div class="w-full border-t border-gray-300" />
        </div>
        <div class="relative flex justify-center text-sm">
          <span class="px-2 bg-white text-gray-500">Or continue with</span>
        </div>
      </div>

      <!-- OAuth Buttons -->
      <div class="mt-6 grid grid-cols-2 gap-3">
        <button
          @click="handleGoogleLogin"
          class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
        >
          <svg class="h-5 w-5" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
          </svg>
          <span class="ml-2">Google</span>
        </button>

        <button
          @click="handleLinkedInLogin"
          class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
        >
          <svg class="h-5 w-5" fill="#0077B5" viewBox="0 0 24 24">
            <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
          </svg>
          <span class="ml-2">LinkedIn</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuth } from '@/composables/useAuth'

const { register, isLoading, getGoogleAuthUrl, getLinkedInAuthUrl } = useAuth()

const form = reactive({
  email: '',
  password: '',
  confirmPassword: '',
  first_name: '',
  last_name: ''
})

const errors = reactive({
  email: '',
  password: '',
  confirmPassword: '',
  first_name: '',
  last_name: ''
})

const error = ref('')

const passwordValidation = computed(() => ({
  length: form.password.length >= 8,
  uppercase: /[A-Z]/.test(form.password),
  lowercase: /[a-z]/.test(form.password),
  number: /\d/.test(form.password),
}))

const isPasswordValid = computed(() => {
  return Object.values(passwordValidation.value).every(Boolean)
})

const isFormValid = computed(() => {
  return form.email && 
         form.password && 
         form.confirmPassword === form.password &&
         isPasswordValid.value &&
         !Object.values(errors).some(Boolean)
})

const validateForm = () => {
  // Reset errors
  Object.keys(errors).forEach(key => {
    errors[key as keyof typeof errors] = ''
  })
  
  // Email validation
  if (!form.email) {
    errors.email = 'Email is required'
  } else if (!/\S+@\S+\.\S+/.test(form.email)) {
    errors.email = 'Email is invalid'
  }
  
  // Password validation
  if (!form.password) {
    errors.password = 'Password is required'
  } else if (!isPasswordValid.value) {
    errors.password = 'Password does not meet requirements'
  }
  
  // Confirm password validation
  if (!form.confirmPassword) {
    errors.confirmPassword = 'Please confirm your password'
  } else if (form.password !== form.confirmPassword) {
    errors.confirmPassword = 'Passwords do not match'
  }
  
  return !Object.values(errors).some(Boolean)
}

const handleSubmit = async () => {
  if (!validateForm()) return
  
  try {
    error.value = ''
    
    const registrationData: any = {
      email: form.email,
      password: form.password,
    }
    
    // Only include first_name and last_name if they have values
    if (form.first_name) {
      registrationData.first_name = form.first_name
    }
    if (form.last_name) {
      registrationData.last_name = form.last_name  
    }
    
    await register(registrationData)
  } catch (err: any) {
    console.error('Registration error:', err)
    error.value = err.response?.data?.detail || 'Registration failed. Please try again.'
  }
}

const handleGoogleLogin = () => {
  window.location.href = getGoogleAuthUrl()
}

const handleLinkedInLogin = () => {
  window.location.href = getLinkedInAuthUrl()
}
</script>