import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '@/api/auth'
import { STORAGE_KEYS, USER_ROLES } from '@/constants'
import type { User, LoginCredentials, RegisterData, MagicLinkRequest } from '@/types'

const user = ref<User | null>(null)
const isLoading = ref(false)

export const useAuth = () => {
  const router = useRouter()

  // Computed properties
  const isAuthenticated = computed(() => !!user.value)
  const isAdmin = computed(() => user.value?.role === USER_ROLES.ADMIN)
  const isUser = computed(() => user.value?.role === USER_ROLES.USER)

  // Actions
  const login = async (credentials: LoginCredentials) => {
    try {
      isLoading.value = true
      const response = await authAPI.login(credentials)
      
      // Store token and user data
      localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, response.access_token)
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(response.user))
      user.value = response.user

      // Redirect based on role
      if (response.user.role === USER_ROLES.ADMIN) {
        router.push('/admin')
      } else {
        router.push('/dashboard')
      }

      return response
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const register = async (userData: RegisterData) => {
    try {
      isLoading.value = true
      const response = await authAPI.register(userData)
      
      // Store token and user data
      localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, response.access_token)
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(response.user))
      user.value = response.user

      router.push('/dashboard')
      return response
    } catch (error) {
      console.error('Registration failed:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const requestMagicLink = async (data: MagicLinkRequest) => {
    try {
      isLoading.value = true
      return await authAPI.requestMagicLink(data)
    } catch (error) {
      console.error('Magic link request failed:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const verifyMagicLink = async (token: string) => {
    try {
      isLoading.value = true
      const response = await authAPI.verifyMagicLink(token)
      
      // Store token and user data
      localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, response.access_token)
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(response.user))
      user.value = response.user

      router.push('/dashboard')
      return response
    } catch (error) {
      console.error('Magic link verification failed:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const logout = () => {
    localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN)
    localStorage.removeItem(STORAGE_KEYS.USER)
    user.value = null
    router.push('/login')
  }

  const initAuth = async () => {
    const token = localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN)
    const savedUser = localStorage.getItem(STORAGE_KEYS.USER)

    if (token && savedUser) {
      try {
        user.value = JSON.parse(savedUser)
        // Verify token is still valid by fetching current user
        const currentUser = await authAPI.getCurrentUser()
        user.value = currentUser
        localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(currentUser))
      } catch (error) {
        // Token is invalid, clear auth data
        logout()
      }
    }
  }

  const getGoogleAuthUrl = () => authAPI.getGoogleAuthUrl()
  const getLinkedInAuthUrl = () => authAPI.getLinkedInAuthUrl()

  return {
    user: computed(() => user.value),
    isAuthenticated,
    isAdmin,
    isUser,
    isLoading: computed(() => isLoading.value),
    login,
    register,
    requestMagicLink,
    verifyMagicLink,
    logout,
    initAuth,
    getGoogleAuthUrl,
    getLinkedInAuthUrl,
  }
}