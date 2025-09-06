export const APP_NAME = 'FastAPI Vue Starter'

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const AUTH_ROUTES = {
  LOGIN: '/login',
  REGISTER: '/register',
  FORGOT_PASSWORD: '/forgot-password',
  MAGIC_LINK: '/magic-link',
} as const

export const DASHBOARD_ROUTES = {
  USER: '/dashboard',
  ADMIN: '/admin',
} as const

export const STORAGE_KEYS = {
  ACCESS_TOKEN: 'access_token',
  REFRESH_TOKEN: 'refresh_token',
  USER: 'user',
} as const

export const USER_ROLES = {
  ADMIN: 'admin',
  USER: 'user',
} as const

export const AUTH_PROVIDERS = {
  EMAIL: 'email',
  GOOGLE: 'google',
  LINKEDIN: 'linkedin',
  MAGIC_LINK: 'magic_link',
} as const