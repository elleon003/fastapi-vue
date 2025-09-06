<template>
  <div>
    <!-- Header -->
    <div class="mb-8">
      <div class="md:flex md:items-center md:justify-between">
        <div class="flex-1 min-w-0">
          <h1 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
            Admin Dashboard
          </h1>
          <div class="mt-1 flex flex-col sm:flex-row sm:flex-wrap sm:mt-0 sm:space-x-6">
            <div class="mt-2 flex items-center text-sm text-gray-500">
              <ShieldCheckIcon class="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" />
              Administrator Access
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
      <!-- Total Users -->
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <UsersIcon class="h-8 w-8 text-blue-400" />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Total Users</dt>
                <dd class="text-lg font-medium text-gray-900">
                  {{ stats.totalUsers }}
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <!-- Active Users -->
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <CheckCircleIcon class="h-8 w-8 text-green-400" />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Active Users</dt>
                <dd class="text-lg font-medium text-gray-900">
                  {{ stats.activeUsers }}
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <!-- Verified Users -->
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <ShieldCheckIcon class="h-8 w-8 text-purple-400" />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Verified Users</dt>
                <dd class="text-lg font-medium text-gray-900">
                  {{ stats.verifiedUsers }}
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <!-- Admin Users -->
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <CrownIcon class="h-8 w-8 text-yellow-400" />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Administrators</dt>
                <dd class="text-lg font-medium text-gray-900">
                  {{ stats.adminUsers }}
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
          Common administrative tasks and management functions.
        </p>
      </div>
      <div class="px-4 py-5 sm:p-6">
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <RouterLink
            to="/admin/users"
            class="relative p-6 bg-white border border-gray-300 rounded-lg hover:border-primary-500 hover:shadow-md transition-colors group"
          >
            <div>
              <span class="rounded-lg inline-flex p-3 bg-blue-50 text-blue-700 group-hover:bg-blue-100">
                <UsersIcon class="h-6 w-6" />
              </span>
            </div>
            <div class="mt-4">
              <h3 class="text-lg font-medium text-gray-900">
                Manage Users
              </h3>
              <p class="mt-2 text-sm text-gray-500">
                View, edit, and manage user accounts and permissions.
              </p>
            </div>
          </RouterLink>

          <div class="relative p-6 bg-white border border-gray-300 rounded-lg opacity-50 cursor-not-allowed">
            <div>
              <span class="rounded-lg inline-flex p-3 bg-gray-50 text-gray-400">
                <ChartBarIcon class="h-6 w-6" />
              </span>
            </div>
            <div class="mt-4">
              <h3 class="text-lg font-medium text-gray-500">
                Analytics
              </h3>
              <p class="mt-2 text-sm text-gray-400">
                View detailed analytics and user engagement metrics.
              </p>
              <span class="absolute top-2 right-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                Coming Soon
              </span>
            </div>
          </div>

          <div class="relative p-6 bg-white border border-gray-300 rounded-lg opacity-50 cursor-not-allowed">
            <div>
              <span class="rounded-lg inline-flex p-3 bg-gray-50 text-gray-400">
                <CogIcon class="h-6 w-6" />
              </span>
            </div>
            <div class="mt-4">
              <h3 class="text-lg font-medium text-gray-500">
                System Settings
              </h3>
              <p class="mt-2 text-sm text-gray-400">
                Configure application settings and preferences.
              </p>
              <span class="absolute top-2 right-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                Coming Soon
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Users -->
    <div class="bg-white shadow rounded-lg">
      <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-lg leading-6 font-medium text-gray-900">Recent Users</h3>
            <p class="mt-1 max-w-2xl text-sm text-gray-500">
              Latest user registrations and account activities.
            </p>
          </div>
          <RouterLink
            to="/admin/users"
            class="text-primary-600 hover:text-primary-500 text-sm font-medium"
          >
            View all users →
          </RouterLink>
        </div>
      </div>
      <div class="px-4 py-5 sm:p-6">
        <div v-if="isLoadingUsers" class="text-center py-4">
          <div class="animate-spin mx-auto h-8 w-8 text-primary-600">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </div>
        </div>
        
        <div v-else-if="recentUsers.length === 0" class="text-center py-8 text-gray-500">
          No users found.
        </div>
        
        <div v-else class="space-y-4">
          <div
            v-for="user in recentUsers"
            :key="user.id"
            class="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50"
          >
            <div class="flex items-center space-x-4">
              <div class="flex-shrink-0">
                <div class="w-10 h-10 bg-primary-600 rounded-full flex items-center justify-center text-white font-medium">
                  {{ getUserInitials(user) }}
                </div>
              </div>
              <div>
                <p class="text-sm font-medium text-gray-900">
                  {{ user.first_name && user.last_name 
                      ? `${user.first_name} ${user.last_name}` 
                      : user.email }}
                </p>
                <p class="text-sm text-gray-500">{{ user.email }}</p>
                <p class="text-xs text-gray-400">
                  Joined {{ formatDate(user.created_at) }}
                </p>
              </div>
            </div>
            <div class="flex items-center space-x-2">
              <span :class="getBadgeClass(user.role)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                {{ user.role }}
              </span>
              <span :class="user.is_verified ? 'text-green-600' : 'text-gray-400'">
                {{ user.is_verified ? '✓' : '○' }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { usersAPI } from '@/api/users'
import type { User } from '@/types'
import {
  UsersIcon,
  CheckCircleIcon,
  ShieldCheckIcon,
  ChartBarIcon,
  CogIcon,
} from '@heroicons/vue/24/outline'

// Custom crown icon component (since it's not in heroicons)
const CrownIcon = (props: any) => {
  return h('svg', { ...props, fill: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { d: 'M5 16L3 2l5.5 5L12 4l3.5 3L21 2l-2 14H5zm2.7-2h8.6l-.9-7.4L12 9.5 8.6 6.6L7.7 14z' })
  ])
}

const recentUsers = ref<User[]>([])
const isLoadingUsers = ref(true)

const stats = reactive({
  totalUsers: 0,
  activeUsers: 0,
  verifiedUsers: 0,
  adminUsers: 0
})

const loadRecentUsers = async () => {
  try {
    isLoadingUsers.value = true
    const users = await usersAPI.getAllUsers(0, 5) // Get first 5 users
    recentUsers.value = users.sort((a, b) => 
      new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    )
    
    // Calculate stats
    stats.totalUsers = users.length
    stats.activeUsers = users.filter(u => u.is_active).length
    stats.verifiedUsers = users.filter(u => u.is_verified).length
    stats.adminUsers = users.filter(u => u.role === 'admin').length
    
  } catch (error) {
    console.error('Failed to load recent users:', error)
  } finally {
    isLoadingUsers.value = false
  }
}

const getUserInitials = (user: User) => {
  if (user.first_name && user.last_name) {
    return `${user.first_name[0]}${user.last_name[0]}`.toUpperCase()
  }
  return user.email[0].toUpperCase()
}

const getBadgeClass = (role: string) => {
  return role === 'admin' 
    ? 'bg-purple-100 text-purple-800'
    : 'bg-blue-100 text-blue-800'
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now.getTime() - date.getTime())
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 0) return 'today'
  if (diffDays === 1) return 'yesterday'
  if (diffDays < 7) return `${diffDays} days ago`
  
  return date.toLocaleDateString('en-US', { 
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

onMounted(() => {
  loadRecentUsers()
})
</script>

<script lang="ts">
import { h } from 'vue'
</script>