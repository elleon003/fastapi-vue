<template>
  <div class="text-center">
    <div v-if="isLoading" class="animate-spin mx-auto h-12 w-12 text-primary-600">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>
    
    <div class="mt-4">
      <h3 class="text-lg font-medium text-gray-900">
        {{ isLoading ? 'Completing sign in...' : 'Sign in complete!' }}
      </h3>
      <p class="mt-2 text-sm text-gray-600">
        {{ isLoading ? 'Please wait while we sign you in.' : 'Redirecting you to your dashboard...' }}
      </p>
    </div>

    <div v-if="error" class="mt-6 rounded-md bg-red-50 p-4">
      <div class="text-sm text-red-700">
        {{ error }}
      </div>
      <div class="mt-3">
        <RouterLink to="/auth/login" class="btn-primary">
          Try Again
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { STORAGE_KEYS } from '@/constants'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const isLoading = ref(true)
const error = ref('')

const handleOAuthCallback = async () => {
  try {
    const token = route.query.token as string
    
    if (!token) {
      throw new Error('No authentication token received')
    }

    // Store the token
    localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, token)
    
    // Fetch user data
    const response = await fetch('/api/auth/me', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (!response.ok) {
      throw new Error('Failed to fetch user data')
    }
    
    const userData = await response.json()
    
    // Update auth store
    authStore.setUser(userData)
    authStore.setToken(token)
    
    // Redirect based on user role
    setTimeout(() => {
      if (userData.role === 'admin') {
        router.push('/admin')
      } else {
        router.push('/dashboard')
      }
    }, 1000)
    
  } catch (err: any) {
    console.error('OAuth callback error:', err)
    error.value = err.message || 'Authentication failed. Please try again.'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  handleOAuthCallback()
})
</script>