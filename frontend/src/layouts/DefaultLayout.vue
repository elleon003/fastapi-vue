<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <RouterLink to="/" class="flex-shrink-0 flex items-center">
              <h1 class="text-2xl font-bold text-primary-600">{{ APP_NAME }}</h1>
            </RouterLink>
          </div>

          <div class="flex items-center space-x-4">
            <template v-if="!authStore.isAuthenticated">
              <RouterLink
                to="/auth/login"
                class="text-gray-500 hover:text-gray-700 px-3 py-2 rounded-md text-sm font-medium"
              >
                Sign in
              </RouterLink>
              <RouterLink
                to="/auth/register"
                class="btn-primary text-sm"
              >
                Sign up
              </RouterLink>
            </template>

            <template v-else>
              <RouterLink
                :to="authStore.isAdmin ? '/admin' : '/dashboard'"
                class="text-gray-500 hover:text-gray-700 px-3 py-2 rounded-md text-sm font-medium"
              >
                Dashboard
              </RouterLink>
              <div class="relative">
                <button
                  @click="showUserMenu = !showUserMenu"
                  class="flex items-center space-x-2 text-gray-500 hover:text-gray-700"
                >
                  <div class="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
                    {{ authStore.userInitials }}
                  </div>
                </button>
                
                <div
                  v-if="showUserMenu"
                  class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-10"
                >
                  <button
                    @click="logout"
                    class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
                  >
                    Sign out
                  </button>
                </div>
              </div>
            </template>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main content -->
    <main>
      <RouterView />
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-gray-200">
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div class="text-center text-sm text-gray-500">
          <p>&copy; 2024 {{ APP_NAME }}. Built with FastAPI and Vue.js.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { APP_NAME } from '@/constants'
import { useAuth } from '@/composables/useAuth'

const authStore = useAuthStore()
const { logout: authLogout } = useAuth()
const showUserMenu = ref(false)

const logout = () => {
  showUserMenu.value = false
  authLogout()
}

const closeUserMenu = (event: Event) => {
  if (!event.target || !(event.target as Element).closest('.relative')) {
    showUserMenu.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', closeUserMenu)
})

onUnmounted(() => {
  document.removeEventListener('click', closeUserMenu)
})
</script>