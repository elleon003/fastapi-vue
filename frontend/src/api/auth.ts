import type { LoginCredentials, RegisterData, AuthResponse, MagicLinkRequest, User } from '@/types'
import apiClient from './client'

export const authAPI = {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await apiClient.post('/auth/login', credentials)
    return response.data
  },

  async register(userData: RegisterData): Promise<AuthResponse> {
    const response = await apiClient.post('/auth/register', userData)
    return response.data
  },

  async requestMagicLink(data: MagicLinkRequest): Promise<{ message: string; magic_link?: string }> {
    const response = await apiClient.post('/auth/magic-link', data)
    return response.data
  },

  async verifyMagicLink(token: string): Promise<AuthResponse> {
    const response = await apiClient.post(`/auth/magic-link/verify?token=${token}`)
    return response.data
  },

  async getCurrentUser(): Promise<User> {
    const response = await apiClient.get('/auth/me')
    return response.data
  },

  getGoogleAuthUrl(): string {
    return `${apiClient.defaults.baseURL}/auth/google`
  },

  getLinkedInAuthUrl(): string {
    return `${apiClient.defaults.baseURL}/auth/linkedin`
  },
}