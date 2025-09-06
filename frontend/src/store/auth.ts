import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types'
import { STORAGE_KEYS, USER_ROLES } from '@/constants'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const isLoading = ref(false)

  // Getters
  const isAuthenticated = computed(() => !!user.value)
  const isAdmin = computed(() => user.value?.role === USER_ROLES.ADMIN)
  const isUser = computed(() => user.value?.role === USER_ROLES.USER)
  const userInitials = computed(() => {
    if (!user.value) return ''
    const first = user.value.first_name?.[0] || ''
    const last = user.value.last_name?.[0] || ''
    return (first + last).toUpperCase() || user.value.email[0].toUpperCase()
  })

  // Actions
  const setUser = (userData: User) => {
    user.value = userData
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(userData))
  }

  const setToken = (token: string) => {
    localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, token)
  }

  const clearAuth = () => {
    user.value = null
    localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN)
    localStorage.removeItem(STORAGE_KEYS.USER)
  }

  const updateUser = (userData: Partial<User>) => {
    if (user.value) {
      user.value = { ...user.value, ...userData }
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(user.value))
    }
  }

  const initFromStorage = () => {
    const savedUser = localStorage.getItem(STORAGE_KEYS.USER)
    if (savedUser) {
      try {
        user.value = JSON.parse(savedUser)
      } catch (error) {
        console.error('Failed to parse saved user data:', error)
        clearAuth()
      }
    }
  }

  return {
    // State
    user: computed(() => user.value),
    isLoading: computed(() => isLoading.value),
    
    // Getters
    isAuthenticated,
    isAdmin,
    isUser,
    userInitials,
    
    // Actions
    setUser,
    setToken,
    clearAuth,
    updateUser,
    initFromStorage,
    setLoading: (loading: boolean) => { isLoading.value = loading }
  }
})