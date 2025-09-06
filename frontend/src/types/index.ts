export interface User {
  id: number
  email: string
  first_name?: string
  last_name?: string
  is_active: boolean
  is_verified: boolean
  role: 'admin' | 'user'
  auth_provider: 'email' | 'google' | 'linkedin' | 'magic_link'
  avatar_url?: string
  created_at: string
  updated_at?: string
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  password: string
  first_name?: string
  last_name?: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}

export interface ApiError {
  detail: string
}

export interface MagicLinkRequest {
  email: string
}

export interface UserUpdate {
  first_name?: string
  last_name?: string
  avatar_url?: string
}

export type UserRole = 'admin' | 'user'
export type AuthProvider = 'email' | 'google' | 'linkedin' | 'magic_link'