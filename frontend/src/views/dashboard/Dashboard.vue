<template>
  <div>
    <!-- Welcome Header -->
    <div class="mb-8">
      <div class="md:flex md:items-center md:justify-between">
        <div class="flex-1 min-w-0">
          <h1 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
            Welcome back, {{ displayName }}!
          </h1>
          <div class="mt-1 flex flex-col sm:flex-row sm:flex-wrap sm:mt-0 sm:space-x-6">
            <div class="mt-2 flex items-center text-sm text-gray-500">
              <UserIcon class="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" />
              {{ authStore.user?.role === 'admin' ? 'Administrator' : 'User' }}
            </div>
            <div class="mt-2 flex items-center text-sm text-gray-500">
              <CalendarIcon class="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" />
              Member since {{ memberSince }}
            </div>
          </div>
        </div>
        <div class="mt-4 flex md:mt-0 md:ml-4">
          <RouterLink
            to="/dashboard/settings"
            class="ml-3 inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
          >
            <Cog6ToothIcon class="h-4 w-4 mr-2" />
            Settings
          </RouterLink>
        </div>
      </div>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3 mb-8">
      <!-- Account Status -->
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <CheckCircleIcon class="h-8 w-8 text-green-400" />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Account Status</dt>
                <dd class="text-lg font-medium text-gray-900">
                  {{ authStore.user?.is_verified ? 'Verified' : 'Unverified' }}
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <!-- Auth Provider -->
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <KeyIcon class="h-8 w-8 text-blue-400" />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Sign-in Method</dt>
                <dd class="text-lg font-medium text-gray-900 capitalize">
                  {{ formatAuthProvider(authStore.user?.auth_provider) }}
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <!-- Last Updated -->
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <ClockIcon class="h-8 w-8 text-purple-400" />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Last Updated</dt>
                <dd class="text-lg font-medium text-gray-900">
                  {{ lastUpdated }}
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="bg-white shadow rounded-lg mb-8">
      <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
        <h3 class="text-lg leading-6 font-medium text-gray-900">Quick Actions</h3>
        <p class="mt-1 max-w-2xl text-sm text-gray-500">
          Common tasks and shortcuts for your account.
        </p>
      </div>
      <div class="px-4 py-5 sm:p-6">
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <RouterLink
            to="/dashboard/settings"
            class="relative p-6 bg-white border border-gray-300 rounded-lg hover:border-primary-500 hover:shadow-md transition-colors group"
          >
            <div>
              <span class="rounded-lg inline-flex p-3 bg-primary-50 text-primary-700 group-hover:bg-primary-100">
                <Cog6ToothIcon class="h-6 w-6" />
              </span>
            </div>
            <div class="mt-4">
              <h3 class="text-lg font-medium text-gray-900">
                Update Profile
              </h3>
              <p class="mt-2 text-sm text-gray-500">
                Change your name, email, and other account settings.
              </p>
            </div>
          </RouterLink>

          <div class="relative p-6 bg-white border border-gray-300 rounded-lg opacity-50 cursor-not-allowed">
            <div>
              <span class="rounded-lg inline-flex p-3 bg-gray-50 text-gray-400">
                <DocumentTextIcon class="h-6 w-6" />
              </span>
            </div>
            <div class="mt-4">
              <h3 class="text-lg font-medium text-gray-500">
                View Activity Log
              </h3>
              <p class="mt-2 text-sm text-gray-400">
                See your recent account activity and login history.
              </p>
              <span class="absolute top-2 right-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                Coming Soon
              </span>
            </div>
          </div>

          <div class="relative p-6 bg-white border border-gray-300 rounded-lg opacity-50 cursor-not-allowed">
            <div>
              <span class="rounded-lg inline-flex p-3 bg-gray-50 text-gray-400">
                <ShieldCheckIcon class="h-6 w-6" />
              </span>
            </div>
            <div class="mt-4">
              <h3 class="text-lg font-medium text-gray-500">
                Security Settings
              </h3>
              <p class="mt-2 text-sm text-gray-400">
                Manage two-factor authentication and security preferences.
              </p>
              <span class="absolute top-2 right-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                Coming Soon
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Account Overview -->
    <div class="bg-white shadow rounded-lg">
      <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
        <h3 class="text-lg leading-6 font-medium text-gray-900">Account Overview</h3>
        <p class="mt-1 max-w-2xl text-sm text-gray-500">
          Your account information and current settings.
        </p>
      </div>
      <div class="px-4 py-5 sm:p-6">
        <dl class="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-2">
          <div>
            <dt class="text-sm font-medium text-gray-500">Full name</dt>
            <dd class="mt-1 text-sm text-gray-900">
              {{ authStore.user?.first_name && authStore.user?.last_name 
                  ? `${authStore.user.first_name} ${authStore.user.last_name}`
                  : 'Not set' }}
            </dd>
          </div>
          <div>
            <dt class="text-sm font-medium text-gray-500">Email address</dt>
            <dd class="mt-1 text-sm text-gray-900">{{ authStore.user?.email }}</dd>
          </div>
          <div>
            <dt class="text-sm font-medium text-gray-500">Account type</dt>
            <dd class="mt-1 text-sm text-gray-900 capitalize">{{ authStore.user?.role }}</dd>
          </div>
          <div>
            <dt class="text-sm font-medium text-gray-500">Authentication method</dt>
            <dd class="mt-1 text-sm text-gray-900">{{ formatAuthProvider(authStore.user?.auth_provider) }}</dd>
          </div>
          <div>
            <dt class="text-sm font-medium text-gray-500">Email verified</dt>
            <dd class="mt-1 text-sm text-gray-900">
              <span :class="authStore.user?.is_verified ? 'text-green-600' : 'text-red-600'">
                {{ authStore.user?.is_verified ? 'Yes' : 'No' }}
              </span>
            </dd>
          </div>
          <div>
            <dt class="text-sm font-medium text-gray-500">Account status</dt>
            <dd class="mt-1 text-sm text-gray-900">
              <span :class="authStore.user?.is_active ? 'text-green-600' : 'text-red-600'">
                {{ authStore.user?.is_active ? 'Active' : 'Inactive' }}
              </span>
            </dd>
          </div>
        </dl>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import {
  UserIcon,
  CalendarIcon,
  Cog6ToothIcon,
  CheckCircleIcon,
  KeyIcon,
  ClockIcon,
  DocumentTextIcon,
  ShieldCheckIcon,
} from '@heroicons/vue/24/outline'

const authStore = useAuthStore()

const displayName = computed(() => {
  if (authStore.user?.first_name) {
    return authStore.user.first_name
  }
  return authStore.user?.email?.split('@')[0] || 'User'
})

const memberSince = computed(() => {
  if (!authStore.user?.created_at) return 'Unknown'
  
  const date = new Date(authStore.user.created_at)
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'long' 
  })
})

const lastUpdated = computed(() => {
  if (!authStore.user?.updated_at) return 'Never'
  
  const date = new Date(authStore.user.updated_at)
  const now = new Date()
  const diffTime = Math.abs(now.getTime() - date.getTime())
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 0) return 'Today'
  if (diffDays === 1) return 'Yesterday'
  if (diffDays < 7) return `${diffDays} days ago`
  if (diffDays < 30) return `${Math.ceil(diffDays / 7)} weeks ago`
  
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short',
    day: 'numeric'
  })
})

const formatAuthProvider = (provider: string | undefined) => {
  if (!provider) return 'Unknown'
  
  switch (provider) {
    case 'email':
      return 'Email & Password'
    case 'google':
      return 'Google'
    case 'linkedin':
      return 'LinkedIn'
    case 'magic_link':
      return 'Magic Link'
    default:
      return provider
  }
}
</script>