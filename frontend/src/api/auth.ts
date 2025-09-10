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

  // Password Reset
  async requestPasswordReset(data: { email: string }): Promise<{ message: string; reset_link?: string }> {
    const response = await apiClient.post('/auth/password-reset/request', data)
    return response.data
  },

  async verifyPasswordResetToken(token: string): Promise<{ message: string; email: string }> {
    const response = await apiClient.post(`/auth/password-reset/verify?token=${token}`)
    return response.data
  },

  async confirmPasswordReset(data: { token: string; new_password: string }): Promise<{ message: string }> {
    const response = await apiClient.post('/auth/password-reset/confirm', data)
    return response.data
  },

  // Email Verification
  async verifyEmail(token: string): Promise<{ message: string; user: User }> {
    const response = await apiClient.post(`/auth/verify-email?token=${token}`)
    return response.data
  },

  async resendEmailVerification(): Promise<{ message: string }> {
    const response = await apiClient.post('/auth/resend-verification')
    return response.data
  },

  // Session Management
  async getUserSessions(): Promise<Array<{
    id: number
    device_info: string
    ip_address: string
    created_at: string
    last_used: string
    is_current: boolean
  }>> {
    const response = await apiClient.get('/auth/sessions')
    return response.data
  },

  async revokeSession(sessionId: number): Promise<{ message: string }> {
    const response = await apiClient.delete(`/auth/sessions/${sessionId}`)
    return response.data
  },

  async revokeAllSessions(): Promise<{ message: string; revoked_count: number }> {
    const response = await apiClient.post('/auth/sessions/revoke-all')
    return response.data
  },
}