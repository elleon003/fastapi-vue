<template>
  <div>
    <!-- Header -->
    <div class="mb-8">
      <div class="md:flex md:items-center md:justify-between">
        <div class="flex-1 min-w-0">
          <h1 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
            User Management
          </h1>
          <p class="mt-1 text-sm text-gray-500">
            Manage user accounts, permissions, and settings.
          </p>
        </div>
      </div>
    </div>

    <!-- Filters and Search -->
    <div class="bg-white shadow rounded-lg mb-6">
      <div class="px-4 py-5 sm:p-6">
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-4">
          <!-- Search -->
          <div class="sm:col-span-2">
            <label for="search" class="block text-sm font-medium text-gray-700 mb-1">
              Search users
            </label>
            <div class="relative">
              <input
                id="search"
                v-model="searchQuery"
                type="text"
                placeholder="Search by name or email..."
                class="input-field pr-10"
                @input="handleSearch"
              />
              <div class="absolute inset-y-0 right-0 pr-3 flex items-center">
                <MagnifyingGlassIcon class="h-5 w-5 text-gray-400" />
              </div>
            </div>
          </div>

          <!-- Role Filter -->
          <div>
            <label for="roleFilter" class="block text-sm font-medium text-gray-700 mb-1">
              Role
            </label>
            <select
              id="roleFilter"
              v-model="filters.role"
              class="input-field"
              @change="applyFilters"
            >
              <option value="">All Roles</option>
              <option value="admin">Admin</option>
              <option value="user">User</option>
            </select>
          </div>

          <!-- Status Filter -->
          <div>
            <label for="statusFilter" class="block text-sm font-medium text-gray-700 mb-1">
              Status
            </label>
            <select
              id="statusFilter"
              v-model="filters.status"
              class="input-field"
              @change="applyFilters"
            >
              <option value="">All Statuses</option>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
              <option value="verified">Verified</option>
              <option value="unverified">Unverified</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- User Table -->
    <div class="bg-white shadow rounded-lg">
      <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
        <div class="flex items-center justify-between">
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            Users ({{ filteredUsers.length }})
          </h3>
          <div class="text-sm text-gray-500">
            Showing {{ Math.min(filteredUsers.length, pageSize) }} of {{ filteredUsers.length }}
          </div>
        </div>
      </div>

      <div v-if="isLoading" class="text-center py-8">
        <div class="animate-spin mx-auto h-8 w-8 text-primary-600">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
      </div>

      <div v-else-if="filteredUsers.length === 0" class="text-center py-8 text-gray-500">
        {{ searchQuery ? 'No users match your search criteria.' : 'No users found.' }}
      </div>

      <div v-else class="overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                User
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Role
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Auth Method
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Joined
              </th>
              <th scope="col" class="relative px-6 py-3">
                <span class="sr-only">Actions</span>
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr
              v-for="user in paginatedUsers"
              :key="user.id"
              class="hover:bg-gray-50"
            >
              <!-- User Info -->
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-10 w-10">
                    <div class="h-10 w-10 rounded-full bg-primary-600 flex items-center justify-center text-white font-medium text-sm">
                      {{ getUserInitials(user) }}
                    </div>
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">
                      {{ user.first_name && user.last_name 
                          ? `${user.first_name} ${user.last_name}` 
                          : 'No name set' }}
                    </div>
                    <div class="text-sm text-gray-500">{{ user.email }}</div>
                  </div>
                </div>
              </td>

              <!-- Role -->
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="getRoleBadgeClass(user.role)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                  {{ user.role }}
                </span>
              </td>

              <!-- Status -->
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex flex-col space-y-1">
                  <span :class="getStatusBadgeClass(user.is_active)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                    {{ user.is_active ? 'Active' : 'Inactive' }}
                  </span>
                  <span :class="getVerificationBadgeClass(user.is_verified)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                    {{ user.is_verified ? 'Verified' : 'Unverified' }}
                  </span>
                </div>
              </td>

              <!-- Auth Method -->
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ formatAuthProvider(user.auth_provider) }}
              </td>

              <!-- Joined -->
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(user.created_at) }}
              </td>

              <!-- Actions -->
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div class="flex items-center space-x-2 justify-end">
                  <button
                    @click="viewUser(user)"
                    class="text-primary-600 hover:text-primary-900"
                  >
                    <EyeIcon class="h-5 w-5" />
                  </button>
                  <button
                    v-if="user.id !== authStore.user?.id"
                    @click="toggleUserStatus(user)"
                    :class="user.is_active ? 'text-red-600 hover:text-red-900' : 'text-green-600 hover:text-green-900'"
                  >
                    {{ user.is_active ? 'Deactivate' : 'Activate' }}
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div v-if="filteredUsers.length > pageSize" class="bg-white px-4 py-3 border-t border-gray-200 sm:px-6">
        <div class="flex items-center justify-between">
          <div class="flex-1 flex justify-between sm:hidden">
            <button
              @click="previousPage"
              :disabled="currentPage === 1"
              class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
              :class="{ 'opacity-50 cursor-not-allowed': currentPage === 1 }"
            >
              Previous
            </button>
            <button
              @click="nextPage"
              :disabled="currentPage === totalPages"
              class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
              :class="{ 'opacity-50 cursor-not-allowed': currentPage === totalPages }"
            >
              Next
            </button>
          </div>
          <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p class="text-sm text-gray-700">
                Showing <span class="font-medium">{{ startIndex + 1 }}</span> to 
                <span class="font-medium">{{ Math.min(endIndex, filteredUsers.length) }}</span> of 
                <span class="font-medium">{{ filteredUsers.length }}</span> results
              </p>
            </div>
            <div>
              <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
                <button
                  @click="previousPage"
                  :disabled="currentPage === 1"
                  class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                  :class="{ 'opacity-50 cursor-not-allowed': currentPage === 1 }"
                >
                  <ChevronLeftIcon class="h-5 w-5" />
                </button>
                <button
                  v-for="page in visiblePages"
                  :key="page"
                  @click="goToPage(page)"
                  :class="page === currentPage
                    ? 'bg-primary-50 border-primary-500 text-primary-600'
                    : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'"
                  class="relative inline-flex items-center px-4 py-2 border text-sm font-medium"
                >
                  {{ page }}
                </button>
                <button
                  @click="nextPage"
                  :disabled="currentPage === totalPages"
                  class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                  :class="{ 'opacity-50 cursor-not-allowed': currentPage === totalPages }"
                >
                  <ChevronRightIcon class="h-5 w-5" />
                </button>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- User Detail Modal -->
    <div v-if="selectedUser" class="fixed inset-0 z-50 overflow-y-auto">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="closeUserModal"></div>

        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="mt-3 text-center sm:mt-0 sm:text-left w-full">
                <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                  User Details
                </h3>
                
                <div class="space-y-4">
                  <div class="flex items-center space-x-4">
                    <div class="flex-shrink-0">
                      <div class="w-12 h-12 bg-primary-600 rounded-full flex items-center justify-center text-white font-medium">
                        {{ getUserInitials(selectedUser) }}
                      </div>
                    </div>
                    <div>
                      <p class="text-sm font-medium text-gray-900">
                        {{ selectedUser.first_name && selectedUser.last_name 
                            ? `${selectedUser.first_name} ${selectedUser.last_name}` 
                            : 'No name set' }}
                      </p>
                      <p class="text-sm text-gray-500">{{ selectedUser.email }}</p>
                    </div>
                  </div>

                  <dl class="grid grid-cols-1 gap-4 sm:grid-cols-2">
                    <div>
                      <dt class="text-sm font-medium text-gray-500">User ID</dt>
                      <dd class="mt-1 text-sm text-gray-900">{{ selectedUser.id }}</dd>
                    </div>
                    <div>
                      <dt class="text-sm font-medium text-gray-500">Role</dt>
                      <dd class="mt-1">
                        <span :class="getRoleBadgeClass(selectedUser.role)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                          {{ selectedUser.role }}
                        </span>
                      </dd>
                    </div>
                    <div>
                      <dt class="text-sm font-medium text-gray-500">Status</dt>
                      <dd class="mt-1">
                        <span :class="getStatusBadgeClass(selectedUser.is_active)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                          {{ selectedUser.is_active ? 'Active' : 'Inactive' }}
                        </span>
                      </dd>
                    </div>
                    <div>
                      <dt class="text-sm font-medium text-gray-500">Email Verified</dt>
                      <dd class="mt-1">
                        <span :class="getVerificationBadgeClass(selectedUser.is_verified)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                          {{ selectedUser.is_verified ? 'Verified' : 'Unverified' }}
                        </span>
                      </dd>
                    </div>
                    <div>
                      <dt class="text-sm font-medium text-gray-500">Auth Method</dt>
                      <dd class="mt-1 text-sm text-gray-900">{{ formatAuthProvider(selectedUser.auth_provider) }}</dd>
                    </div>
                    <div>
                      <dt class="text-sm font-medium text-gray-500">Joined</dt>
                      <dd class="mt-1 text-sm text-gray-900">{{ formatDetailDate(selectedUser.created_at) }}</dd>
                    </div>
                    <div v-if="selectedUser.updated_at" class="sm:col-span-2">
                      <dt class="text-sm font-medium text-gray-500">Last Updated</dt>
                      <dd class="mt-1 text-sm text-gray-900">{{ formatDetailDate(selectedUser.updated_at) }}</dd>
                    </div>
                  </dl>
                </div>
              </div>
            </div>
          </div>
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              type="button"
              @click="closeUserModal"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 sm:mt-0 sm:w-auto sm:text-sm"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useAuthStore } from '@/store/auth'
import { usersAPI } from '@/api/users'
import type { User } from '@/types'
import {
  MagnifyingGlassIcon,
  EyeIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
} from '@heroicons/vue/24/outline'

const authStore = useAuthStore()

const users = ref<User[]>([])
const isLoading = ref(true)
const searchQuery = ref('')
const selectedUser = ref<User | null>(null)

const filters = reactive({
  role: '',
  status: ''
})

// Pagination
const currentPage = ref(1)
const pageSize = ref(10)

const filteredUsers = computed(() => {
  let result = users.value

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(user => 
      user.email.toLowerCase().includes(query) ||
      (user.first_name && user.first_name.toLowerCase().includes(query)) ||
      (user.last_name && user.last_name.toLowerCase().includes(query))
    )
  }

  // Role filter
  if (filters.role) {
    result = result.filter(user => user.role === filters.role)
  }

  // Status filter
  if (filters.status) {
    switch (filters.status) {
      case 'active':
        result = result.filter(user => user.is_active)
        break
      case 'inactive':
        result = result.filter(user => !user.is_active)
        break
      case 'verified':
        result = result.filter(user => user.is_verified)
        break
      case 'unverified':
        result = result.filter(user => !user.is_verified)
        break
    }
  }

  return result
})

const totalPages = computed(() => Math.ceil(filteredUsers.value.length / pageSize.value))
const startIndex = computed(() => (currentPage.value - 1) * pageSize.value)
const endIndex = computed(() => startIndex.value + pageSize.value)

const paginatedUsers = computed(() => 
  filteredUsers.value.slice(startIndex.value, endIndex.value)
)

const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, currentPage.value - 2)
  const end = Math.min(totalPages.value, currentPage.value + 2)
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  return pages
})

const loadUsers = async () => {
  try {
    isLoading.value = true
    users.value = await usersAPI.getAllUsers(0, 1000) // Load all users for admin
  } catch (error) {
    console.error('Failed to load users:', error)
  } finally {
    isLoading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1 // Reset to first page when searching
}

const applyFilters = () => {
  currentPage.value = 1 // Reset to first page when filtering
}

const getUserInitials = (user: User) => {
  if (user.first_name && user.last_name) {
    return `${user.first_name[0]}${user.last_name[0]}`.toUpperCase()
  }
  return user.email[0].toUpperCase()
}

const getRoleBadgeClass = (role: string) => {
  return role === 'admin' 
    ? 'bg-purple-100 text-purple-800'
    : 'bg-blue-100 text-blue-800'
}

const getStatusBadgeClass = (isActive: boolean) => {
  return isActive
    ? 'bg-green-100 text-green-800'
    : 'bg-red-100 text-red-800'
}

const getVerificationBadgeClass = (isVerified: boolean) => {
  return isVerified
    ? 'bg-green-100 text-green-800'
    : 'bg-yellow-100 text-yellow-800'
}

const formatAuthProvider = (provider: string) => {
  switch (provider) {
    case 'email':
      return 'Email & Password'
    case 'google':
      return 'Google'
    case 'linkedin':
      return 'LinkedIn'
    case 'magic_link':
      return 'Magic Link'
    default:
      return provider
  }
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { 
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

const formatDetailDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('en-US', { 
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const viewUser = (user: User) => {
  selectedUser.value = user
}

const closeUserModal = () => {
  selectedUser.value = null
}

const toggleUserStatus = async (user: User) => {
  try {
    if (user.is_active) {
      await usersAPI.deactivateUser(user.id)
      user.is_active = false
    } else {
      // Note: We don't have an activate endpoint, so this would need to be implemented
      console.log('Activate user functionality not yet implemented')
    }
  } catch (error) {
    console.error('Failed to toggle user status:', error)
  }
}

// Pagination methods
const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const goToPage = (page: number) => {
  currentPage.value = page
}

onMounted(() => {
  loadUsers()
})
</script>