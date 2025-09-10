<template>
  <div>
    <div class="mb-6">
      <h2 class="text-center text-3xl font-extrabold text-gray-900">
        Email Verification
      </h2>
    </div>

    <div v-if="isLoading" class="text-center py-8">
      <svg class="animate-spin mx-auto h-12 w-12 text-primary-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <p class="mt-4 text-gray-600">Verifying your email...</p>
    </div>

    <div v-if="!isLoading && success" class="rounded-md bg-green-50 p-6">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-green-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <h3 class="text-sm font-medium text-green-800">
            Email verified successfully!
          </h3>
          <div class="mt-2 text-sm text-green-700">
            <p>Your email has been verified. You can now access all features of your account.</p>
          </div>
          <div class="mt-4">
            <div class="flex space-x-4">
              <RouterLink to="/dashboard" class="bg-green-100 text-green-800 px-3 py-2 rounded-md text-sm font-medium hover:bg-green-200">
                Go to Dashboard
              </RouterLink>
              <RouterLink to="/auth/login" class="text-green-800 px-3 py-2 rounded-md text-sm font-medium hover:bg-green-100">
                Login
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="!isLoading && !success" class="rounded-md bg-red-50 p-6">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <h3 class="text-sm font-medium text-red-800">
            Email verification failed
          </h3>
          <div class="mt-2 text-sm text-red-700">
            <p>{{ errorMessage }}</p>
          </div>
          <div class="mt-4">
            <div class="flex space-x-4">
              <button 
                v-if="canResend"
                @click="resendVerification"
                :disabled="resendLoading"
                class="bg-red-100 text-red-800 px-3 py-2 rounded-md text-sm font-medium hover:bg-red-200 disabled:opacity-50"
              >
                {{ resendLoading ? 'Sending...' : 'Resend verification email' }}
              </button>
              <RouterLink to="/auth/login" class="text-red-800 px-3 py-2 rounded-md text-sm font-medium hover:bg-red-100">
                Back to Login
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { authAPI } from '@/api/auth'
import { useAuth } from '@/composables/useAuth'

const route = useRoute()
const { user } = useAuth()

const isLoading = ref(true)
const success = ref(false)
const errorMessage = ref('')
const canResend = ref(false)
const resendLoading = ref(false)

const verifyEmail = async () => {
  const token = route.query.token as string
  if (!token) {
    errorMessage.value = 'No verification token provided.'
    isLoading.value = false
    return
  }
  
  try {
    await authAPI.verifyEmail(token)
    success.value = true
  } catch (err: any) {
    console.error('Email verification error:', err)
    success.value = false
    
    if (err.response?.status === 400) {
      errorMessage.value = 'This verification link is invalid or has expired.'
      canResend.value = !!user.value // Show resend only if user is logged in
    } else {
      errorMessage.value = 'Something went wrong. Please try again.'
    }
  } finally {
    isLoading.value = false
  }
}

const resendVerification = async () => {
  if (!user.value) return
  
  try {
    resendLoading.value = true
    await authAPI.resendEmailVerification()
    
    // Show success message
    errorMessage.value = 'A new verification email has been sent to your email address.'
    canResend.value = false
  } catch (err: any) {
    console.error('Resend verification error:', err)
    errorMessage.value = err.response?.data?.detail || 'Failed to resend verification email.'
  } finally {
    resendLoading.value = false
  }
}

onMounted(() => {
  verifyEmail()
})
</script>