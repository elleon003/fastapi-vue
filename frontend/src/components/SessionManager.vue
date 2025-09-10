<template>
  <div class="bg-white shadow rounded-lg p-6">
    <div class="mb-4">
      <h3 class="text-lg font-medium text-gray-900">Active Sessions</h3>
      <p class="mt-1 text-sm text-gray-500">
        Manage your active login sessions across devices.
      </p>
    </div>

    <div v-if="isLoading" class="flex justify-center py-8">
      <svg class="animate-spin h-8 w-8 text-primary-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>

    <div v-else-if="error" class="rounded-md bg-red-50 p-4">
      <div class="text-sm text-red-700">
        {{ error }}
      </div>
    </div>

    <div v-else>
      <div class="space-y-4">
        <div v-for="session in sessions" :key="session.id" class="border border-gray-200 rounded-lg p-4">
          <div class="flex items-center justify-between">
            <div class="flex-1">
              <div class="flex items-center space-x-2">
                <div class="flex-shrink-0">
                  <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                  </svg>
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-900">
                    {{ getDeviceName(session.device_info) }}
                    <span v-if="session.is_current" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 ml-2">
                      Current
                    </span>
                  </p>
                  <p class="text-xs text-gray-500">{{ session.ip_address }}</p>
                  <p class="text-xs text-gray-500">
                    Last active: {{ formatDate(session.last_used) }}
                  </p>
                  <p class="text-xs text-gray-500">
                    Created: {{ formatDate(session.created_at) }}
                  </p>
                </div>
              </div>
            </div>
            <div class="flex-shrink-0">
              <button
                v-if="!session.is_current"
                @click="revokeSession(session.id)"
                :disabled="revokingSession === session.id"
                class="inline-flex items-center px-2.5 py-1.5 border border-gray-300 shadow-sm text-xs font-medium rounded text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
              >
                <svg v-if="revokingSession === session.id" class="animate-spin -ml-1 mr-1 h-3 w-3 text-gray-700" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ revokingSession === session.id ? 'Revoking...' : 'Revoke' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="sessions.length > 1" class="mt-6 pt-4 border-t border-gray-200">
        <button
          @click="revokeAllSessions"
          :disabled="revokingAll"
          class="inline-flex items-center px-4 py-2 border border-red-300 shadow-sm text-sm font-medium rounded-md text-red-700 bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
        >
          <svg v-if="revokingAll" class="animate-spin -ml-1 mr-2 h-4 w-4 text-red-700" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ revokingAll ? 'Revoking all...' : 'Revoke all other sessions' }}
        </button>
        <p class="mt-2 text-xs text-gray-500">
          This will sign you out of all devices except this one.
        </p>
      </div>

      <div v-if="sessions.length === 0" class="text-center py-8">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
        </svg>
        <p class="mt-2 text-sm text-gray-500">No active sessions found.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { authAPI } from '@/api/auth'

interface Session {
  id: number
  device_info: string
  ip_address: string
  created_at: string
  last_used: string
  is_current: boolean
}

const sessions = ref<Session[]>([])
const isLoading = ref(true)
const error = ref('')
const revokingSession = ref<number | null>(null)
const revokingAll = ref(false)

const getDeviceName = (deviceInfo: string): string => {
  if (!deviceInfo || deviceInfo === 'Unknown') return 'Unknown Device'
  
  // Extract browser and OS info from user agent
  const ua = deviceInfo.toLowerCase()
  
  let browser = 'Unknown Browser'
  let os = 'Unknown OS'
  
  // Browser detection
  if (ua.includes('chrome')) browser = 'Chrome'
  else if (ua.includes('firefox')) browser = 'Firefox'
  else if (ua.includes('safari')) browser = 'Safari'
  else if (ua.includes('edge')) browser = 'Edge'
  
  // OS detection
  if (ua.includes('windows')) os = 'Windows'
  else if (ua.includes('mac')) os = 'macOS'
  else if (ua.includes('linux')) os = 'Linux'
  else if (ua.includes('android')) os = 'Android'
  else if (ua.includes('ios')) os = 'iOS'
  
  return `${browser} on ${os}`
}

const formatDate = (dateString: string): string => {
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
  } catch {
    return dateString
  }
}

const loadSessions = async () => {
  try {
    isLoading.value = true
    error.value = ''
    sessions.value = await authAPI.getUserSessions()
  } catch (err: any) {
    console.error('Failed to load sessions:', err)
    error.value = 'Failed to load sessions. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const revokeSession = async (sessionId: number) => {
  try {
    revokingSession.value = sessionId
    await authAPI.revokeSession(sessionId)
    
    // Remove the session from the list
    sessions.value = sessions.value.filter(s => s.id !== sessionId)
  } catch (err: any) {
    console.error('Failed to revoke session:', err)
    error.value = 'Failed to revoke session. Please try again.'
  } finally {
    revokingSession.value = null
  }
}

const revokeAllSessions = async () => {
  try {
    revokingAll.value = true
    const response = await authAPI.revokeAllSessions()
    
    // Keep only the current session
    sessions.value = sessions.value.filter(s => s.is_current)
    
    // Show success message
    console.log(`Revoked ${response.revoked_count} sessions`)
  } catch (err: any) {
    console.error('Failed to revoke all sessions:', err)
    error.value = 'Failed to revoke sessions. Please try again.'
  } finally {
    revokingAll.value = false
  }
}

onMounted(() => {
  loadSessions()
})
</script>