<template>
  <div class="text-center">
    <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100">
      <ExclamationTriangleIcon class="h-6 w-6 text-red-600" />
    </div>
    
    <div class="mt-3">
      <h3 class="text-lg leading-6 font-medium text-gray-900">
        Authentication Error
      </h3>
      <div class="mt-2">
        <p class="text-sm text-gray-500">
          {{ errorMessage }}
        </p>
      </div>
    </div>

    <div class="mt-6 flex flex-col space-y-3">
      <RouterLink to="/auth/login" class="btn-primary">
        Try Again
      </RouterLink>
      <RouterLink to="/" class="text-sm text-gray-500 hover:text-gray-700">
        ← Back to home
      </RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { ExclamationTriangleIcon } from '@heroicons/vue/24/outline'

const route = useRoute()

const errorMessage = computed(() => {
  const error = route.query.error as string
  
  switch (error) {
    case 'oauth_failed':
      return 'OAuth authentication failed. Please try again or use a different sign-in method.'
    case 'access_denied':
      return 'Access was denied. Please grant the necessary permissions to continue.'
    case 'invalid_request':
      return 'The authentication request was invalid. Please try again.'
    case 'server_error':
      return 'A server error occurred during authentication. Please try again later.'
    default:
      return 'An unexpected error occurred during authentication. Please try again.'
  }
})
</script>