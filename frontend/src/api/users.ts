import type { User, UserUpdate } from '@/types'
import apiClient from './client'

export const usersAPI = {
  async getProfile(): Promise<User> {
    const response = await apiClient.get('/users/profile')
    return response.data
  },

  async updateProfile(userData: UserUpdate): Promise<User> {
    const response = await apiClient.put('/users/profile', userData)
    return response.data
  },

  async getAllUsers(skip = 0, limit = 100): Promise<User[]> {
    const response = await apiClient.get(`/users/?skip=${skip}&limit=${limit}`)
    return response.data
  },

  async getUserById(userId: number): Promise<User> {
    const response = await apiClient.get(`/users/${userId}`)
    return response.data
  },

  async updateUserById(userId: number, userData: UserUpdate): Promise<User> {
    const response = await apiClient.put(`/users/${userId}`, userData)
    return response.data
  },

  async deactivateUser(userId: number): Promise<User> {
    const response = await apiClient.delete(`/users/${userId}`)
    return response.data
  },
}