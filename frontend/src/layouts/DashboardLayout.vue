<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Sidebar -->
    <div class="fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform transition-transform lg:translate-x-0" :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full'">
      <div class="flex items-center justify-between h-16 px-4 border-b">
        <RouterLink to="/" class="flex items-center">
          <h1 class="text-xl font-bold text-primary-600">{{ APP_NAME }}</h1>
        </RouterLink>
        <button @click="sidebarOpen = false" class="lg:hidden">
          <XMarkIcon class="h-6 w-6" />
        </button>
      </div>

      <nav class="mt-8 px-4">
        <div class="space-y-1">
          <!-- User Navigation -->
          <template v-if="!authStore.isAdmin">
            <RouterLink
              to="/dashboard"
              class="nav-link group"
              active-class="nav-link-active"
            >
              <HomeIcon class="h-5 w-5" />
              Dashboard
            </RouterLink>
            <RouterLink
              to="/dashboard/settings"
              class="nav-link group"
              active-class="nav-link-active"
            >
              <Cog6ToothIcon class="h-5 w-5" />
              Settings
            </RouterLink>
          </template>

          <!-- Admin Navigation -->
          <template v-else>
            <RouterLink
              to="/admin"
              class="nav-link group"
              active-class="nav-link-active"
            >
              <ChartBarIcon class="h-5 w-5" />
              Admin Dashboard
            </RouterLink>
            <RouterLink
              to="/admin/users"
              class="nav-link group"
              active-class="nav-link-active"
            >
              <UsersIcon class="h-5 w-5" />
              User Management
            </RouterLink>
            <RouterLink
              to="/dashboard/settings"
              class="nav-link group"
              active-class="nav-link-active"
            >
              <Cog6ToothIcon class="h-5 w-5" />
              Settings
            </RouterLink>
          </template>
        </div>
      </nav>

      <!-- User info at bottom -->
      <div class="absolute bottom-0 left-0 right-0 p-4 border-t">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 bg-primary-600 rounded-full flex items-center justify-center text-white font-medium">
            {{ authStore.userInitials }}
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-gray-900 truncate">
              {{ authStore.user?.first_name || authStore.user?.email }}
            </p>
            <p class="text-xs text-gray-500 truncate">
              {{ authStore.user?.role }}
            </p>
          </div>
          <button @click="logout" class="text-gray-400 hover:text-gray-600">
            <ArrowRightOnRectangleIcon class="h-5 w-5" />
          </button>
        </div>
      </div>
    </div>

    <!-- Main content -->
    <div class="lg:pl-64">
      <!-- Top bar -->
      <div class="sticky top-0 z-40 flex h-16 shrink-0 items-center gap-x-4 border-b border-gray-200 bg-white px-4 shadow-sm sm:gap-x-6 sm:px-6 lg:px-8">
        <button @click="sidebarOpen = !sidebarOpen" class="lg:hidden">
          <Bars3Icon class="h-6 w-6" />
        </button>

        <div class="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
          <div class="flex flex-1"></div>
          <div class="flex items-center gap-x-4 lg:gap-x-6">
            <!-- Notifications could go here -->
          </div>
        </div>
      </div>

      <!-- Page content -->
      <main class="py-10">
        <div class="px-4 sm:px-6 lg:px-8">
          <RouterView />
        </div>
      </main>
    </div>

    <!-- Mobile sidebar overlay -->
    <div
      v-if="sidebarOpen"
      class="fixed inset-0 z-40 bg-gray-600 bg-opacity-75 lg:hidden"
      @click="sidebarOpen = false"
    ></div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { useAuth } from '@/composables/useAuth'
import { APP_NAME } from '@/constants'
import {
  Bars3Icon,
  XMarkIcon,
  HomeIcon,
  Cog6ToothIcon,
  ChartBarIcon,
  UsersIcon,
  ArrowRightOnRectangleIcon,
} from '@heroicons/vue/24/outline'

const authStore = useAuthStore()
const { logout: authLogout } = useAuth()
const sidebarOpen = ref(false)

const logout = () => {
  authLogout()
}
</script>

<style scoped>
.nav-link {
  @apply flex items-center space-x-3 text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md p-2 text-sm font-medium;
}

.nav-link-active {
  @apply bg-primary-50 text-primary-700;
}
</style>