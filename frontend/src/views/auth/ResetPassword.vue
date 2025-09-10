<template>
  <div>
    <div class="mb-6">
      <h2 class="text-center text-3xl font-extrabold text-gray-900">
        Set new password
      </h2>
      <p class="mt-2 text-center text-sm text-gray-600">
        Enter your new password below.
      </p>
      <p v-if="userEmail" class="mt-1 text-center text-sm text-gray-500">
        Resetting password for: {{ userEmail }}
      </p>
    </div>

    <div v-if="!tokenValid && !isLoading" class="rounded-md bg-red-50 p-4 mb-6">
      <div class="text-sm text-red-700">
        This password reset link is invalid or has expired. Please request a new one.
      </div>
      <div class="mt-2">
        <RouterLink to="/auth/forgot-password" class="text-sm font-medium text-red-600 hover:text-red-500">
          Request new reset link
        </RouterLink>
      </div>
    </div>

    <form v-if="tokenValid" @submit.prevent="handleSubmit" class="space-y-6">
      <div>
        <label for="password" class="block text-sm font-medium text-gray-700">
          New Password
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
          Confirm New Password
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

      <div v-if="successMessage" class="rounded-md bg-green-50 p-4">
        <div class="text-sm text-green-700">
          {{ successMessage }}
        </div>
        <div class="mt-2">
          <RouterLink to="/auth/login" class="text-sm font-medium text-green-600 hover:text-green-500">
            Go to login
          </RouterLink>
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
          {{ isLoading ? 'Resetting password...' : 'Reset password' }}
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
import { ref, reactive, computed, onMounted } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { authAPI } from '@/api/auth'

const route = useRoute()
const router = useRouter()

const form = reactive({
  password: '',
  confirmPassword: ''
})

const errors = reactive({
  password: '',
  confirmPassword: ''
})

const error = ref('')
const successMessage = ref('')
const isLoading = ref(false)
const tokenValid = ref(false)
const userEmail = ref('')
const token = ref('')

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
  return form.password && 
         form.confirmPassword === form.password &&
         isPasswordValid.value &&
         !Object.values(errors).some(Boolean)
})

const validateForm = () => {
  // Reset errors
  Object.keys(errors).forEach(key => {
    errors[key as keyof typeof errors] = ''
  })
  
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

const verifyToken = async () => {
  const tokenParam = route.query.token as string
  if (!tokenParam) {
    tokenValid.value = false
    return
  }
  
  token.value = tokenParam
  
  try {
    isLoading.value = true
    const response = await authAPI.verifyPasswordResetToken(tokenParam)
    tokenValid.value = true
    userEmail.value = response.email
  } catch (err: any) {
    console.error('Token verification error:', err)
    tokenValid.value = false
  } finally {
    isLoading.value = false
  }
}

const handleSubmit = async () => {
  if (!validateForm()) return
  
  try {
    error.value = ''
    successMessage.value = ''
    isLoading.value = true
    
    await authAPI.confirmPasswordReset({
      token: token.value,
      new_password: form.password
    })
    
    successMessage.value = 'Password reset successfully! You can now log in with your new password.'
    
    // Clear form
    form.password = ''
    form.confirmPassword = ''
    
  } catch (err: any) {
    console.error('Password reset error:', err)
    error.value = err.response?.data?.detail || 'Password reset failed. Please try again.'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  verifyToken()
})
</script>