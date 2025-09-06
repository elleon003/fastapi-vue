<template>
  <div>
    <div class="mb-6">
      <h2 class="text-center text-3xl font-extrabold text-gray-900">
        Sign in with Magic Link
      </h2>
      <p class="mt-2 text-center text-sm text-gray-600">
        Enter your email and we'll send you a secure login link
      </p>
    </div>

    <!-- Step 1: Request Magic Link -->
    <div v-if="!magicLinkSent">
      <form @submit.prevent="handleRequestMagicLink" class="space-y-6">
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
              placeholder="Enter your email address"
            />
            <p v-if="errors.email" class="mt-1 text-sm text-red-600">{{ errors.email }}</p>
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
            :disabled="isLoading || !form.email"
            class="btn-primary w-full flex justify-center"
            :class="{ 'opacity-50 cursor-not-allowed': isLoading || !form.email }"
          >
            <svg v-if="isLoading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ isLoading ? 'Sending...' : 'Send Magic Link' }}
          </button>
        </div>
      </form>

      <div class="mt-6 text-center">
        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-300" />
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-white text-gray-500">Or</span>
          </div>
        </div>

        <div class="mt-6">
          <RouterLink to="/auth/login" class="font-medium text-primary-600 hover:text-primary-500">
            Sign in with password instead
          </RouterLink>
        </div>
      </div>
    </div>

    <!-- Step 2: Magic Link Sent -->
    <div v-else class="text-center">
      <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100">
        <CheckIcon class="h-6 w-6 text-green-600" />
      </div>
      
      <div class="mt-3">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Magic link sent!
        </h3>
        <div class="mt-2">
          <p class="text-sm text-gray-500">
            We've sent a secure login link to <strong>{{ form.email }}</strong>
          </p>
          <p class="text-sm text-gray-500 mt-1">
            The link will expire in 15 minutes.
          </p>
        </div>
      </div>

      <!-- Development only - show magic link -->
      <div v-if="magicLinkUrl" class="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-md">
        <div class="text-sm">
          <p class="text-yellow-800 font-medium mb-2">Development Mode</p>
          <p class="text-yellow-700 mb-3">Click the link below to sign in:</p>
          <a 
            :href="magicLinkUrl" 
            class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-yellow-700 bg-yellow-100 hover:bg-yellow-200"
          >
            Use Magic Link
          </a>
        </div>
      </div>

      <div class="mt-6 flex flex-col space-y-3">
        <button
          @click="resendMagicLink"
          :disabled="cooldownActive"
          class="btn-secondary"
          :class="{ 'opacity-50 cursor-not-allowed': cooldownActive }"
        >
          {{ cooldownActive ? `Resend in ${cooldownTime}s` : 'Resend Magic Link' }}
        </button>
        
        <RouterLink to="/auth/login" class="text-sm text-gray-500 hover:text-gray-700">
          ← Back to sign in
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import { CheckIcon } from '@heroicons/vue/24/outline'

const route = useRoute()
const { requestMagicLink, verifyMagicLink, isLoading } = useAuth()

const form = reactive({
  email: ''
})

const errors = reactive({
  email: ''
})

const error = ref('')
const magicLinkSent = ref(false)
const magicLinkUrl = ref('')
const cooldownActive = ref(false)
const cooldownTime = ref(0)

let cooldownTimer: NodeJS.Timeout | null = null

const validateEmail = () => {
  errors.email = ''
  
  if (!form.email) {
    errors.email = 'Email is required'
  } else if (!/\S+@\S+\.\S+/.test(form.email)) {
    errors.email = 'Email is invalid'
  }
  
  return !errors.email
}

const handleRequestMagicLink = async () => {
  if (!validateEmail()) return
  
  try {
    error.value = ''
    const response = await requestMagicLink({ email: form.email })
    
    magicLinkSent.value = true
    
    // In development, the API returns the magic link
    if (response.magic_link) {
      magicLinkUrl.value = response.magic_link
    }
    
    startCooldown()
  } catch (err: any) {
    console.error('Magic link request error:', err)
    error.value = err.response?.data?.detail || 'Failed to send magic link. Please try again.'
  }
}

const resendMagicLink = async () => {
  if (cooldownActive.value) return
  
  try {
    error.value = ''
    const response = await requestMagicLink({ email: form.email })
    
    if (response.magic_link) {
      magicLinkUrl.value = response.magic_link
    }
    
    startCooldown()
  } catch (err: any) {
    console.error('Magic link resend error:', err)
    error.value = err.response?.data?.detail || 'Failed to resend magic link. Please try again.'
  }
}

const startCooldown = () => {
  cooldownActive.value = true
  cooldownTime.value = 30
  
  cooldownTimer = setInterval(() => {
    cooldownTime.value--
    
    if (cooldownTime.value <= 0) {
      cooldownActive.value = false
      if (cooldownTimer) {
        clearInterval(cooldownTimer)
        cooldownTimer = null
      }
    }
  }, 1000)
}

// Handle magic link verification from URL
const handleMagicLinkFromUrl = async () => {
  const token = route.query.token as string
  
  if (token) {
    try {
      await verifyMagicLink(token)
    } catch (err: any) {
      console.error('Magic link verification error:', err)
      error.value = err.response?.data?.detail || 'Invalid or expired magic link.'
    }
  }
}

onMounted(() => {
  handleMagicLinkFromUrl()
})

onUnmounted(() => {
  if (cooldownTimer) {
    clearInterval(cooldownTimer)
  }
})
</script>