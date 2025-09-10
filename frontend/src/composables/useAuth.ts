import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { authAPI } from '@/api/auth'
import { USER_ROLES } from '@/constants'
import type { LoginCredentials, RegisterData, MagicLinkRequest } from '@/types'

export const useAuth = () => {
  const router = useRouter()
  const authStore = useAuthStore()

  // Computed properties
  const isAuthenticated = computed(() => authStore.isAuthenticated)
  const isAdmin = computed(() => authStore.isAdmin)
  const isUser = computed(() => authStore.isUser)

  // Actions
  const login = async (credentials: LoginCredentials) => {
    try {
      authStore.setLoading(true)
      const response = await authAPI.login(credentials)
      
      // Store token and user data using auth store
      authStore.setToken(response.access_token)
      authStore.setUser(response.user)

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
      authStore.setLoading(false)
    }
  }

  const register = async (userData: RegisterData) => {
    try {
      authStore.setLoading(true)
      const response = await authAPI.register(userData)
      
      // Store token and user data using auth store
      authStore.setToken(response.access_token)
      authStore.setUser(response.user)

      router.push('/dashboard')
      return response
    } catch (error) {
      console.error('Registration failed:', error)
      throw error
    } finally {
      authStore.setLoading(false)
    }
  }

  const requestMagicLink = async (data: MagicLinkRequest) => {
    try {
      authStore.setLoading(true)
      return await authAPI.requestMagicLink(data)
    } catch (error) {
      console.error('Magic link request failed:', error)
      throw error
    } finally {
      authStore.setLoading(false)
    }
  }

  const verifyMagicLink = async (token: string) => {
    try {
      authStore.setLoading(true)
      const response = await authAPI.verifyMagicLink(token)
      
      // Store token and user data using auth store
      authStore.setToken(response.access_token)
      authStore.setUser(response.user)

      router.push('/dashboard')
      return response
    } catch (error) {
      console.error('Magic link verification failed:', error)
      throw error
    } finally {
      authStore.setLoading(false)
    }
  }

  const logout = () => {
    authStore.clearAuth()
    router.push('/login')
  }

  const initAuth = async () => {
    authStore.initFromStorage()
    
    if (authStore.user) {
      try {
        // Verify token is still valid by fetching current user
        const currentUser = await authAPI.getCurrentUser()
        authStore.setUser(currentUser)
      } catch (error) {
        // Token is invalid, clear auth data
        logout()
      }
    }
  }

  const getGoogleAuthUrl = () => authAPI.getGoogleAuthUrl()
  const getLinkedInAuthUrl = () => authAPI.getLinkedInAuthUrl()

  return {
    user: computed(() => authStore.user),
    isAuthenticated,
    isAdmin,
    isUser,
    isLoading: computed(() => authStore.isLoading),
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