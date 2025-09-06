<template>
  <div>
    <div class="mb-8">
      <h1 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl">
        Account Settings
      </h1>
      <p class="mt-1 text-sm text-gray-500">
        Manage your account information and preferences.
      </p>
    </div>

    <div class="space-y-6">
      <!-- Profile Information -->
      <div class="bg-white shadow rounded-lg">
        <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
          <h3 class="text-lg leading-6 font-medium text-gray-900">Profile Information</h3>
          <p class="mt-1 max-w-2xl text-sm text-gray-500">
            Update your personal information and profile details.
          </p>
        </div>
        <div class="px-4 py-5 sm:p-6">
          <form @submit.prevent="handleUpdateProfile" class="space-y-6">
            <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
              <div>
                <label for="first_name" class="block text-sm font-medium text-gray-700">
                  First name
                </label>
                <div class="mt-1">
                  <input
                    id="first_name"
                    v-model="profileForm.first_name"
                    name="first_name"
                    type="text"
                    autocomplete="given-name"
                    class="input-field"
                    :class="{ 'border-red-300': errors.first_name }"
                  />
                  <p v-if="errors.first_name" class="mt-1 text-sm text-red-600">{{ errors.first_name }}</p>
                </div>
              </div>

              <div>
                <label for="last_name" class="block text-sm font-medium text-gray-700">
                  Last name
                </label>
                <div class="mt-1">
                  <input
                    id="last_name"
                    v-model="profileForm.last_name"
                    name="last_name"
                    type="text"
                    autocomplete="family-name"
                    class="input-field"
                    :class="{ 'border-red-300': errors.last_name }"
                  />
                  <p v-if="errors.last_name" class="mt-1 text-sm text-red-600">{{ errors.last_name }}</p>
                </div>
              </div>
            </div>

            <div>
              <label for="email" class="block text-sm font-medium text-gray-700">
                Email address
              </label>
              <div class="mt-1">
                <input
                  id="email"
                  :value="authStore.user?.email"
                  type="email"
                  disabled
                  class="input-field bg-gray-50 text-gray-500 cursor-not-allowed"
                />
                <p class="mt-1 text-sm text-gray-500">
                  Email address cannot be changed. Contact support if you need to update this.
                </p>
              </div>
            </div>

            <div v-if="profileSuccess" class="rounded-md bg-green-50 p-4">
              <div class="flex">
                <div class="flex-shrink-0">
                  <CheckCircleIcon class="h-5 w-5 text-green-400" />
                </div>
                <div class="ml-3">
                  <p class="text-sm font-medium text-green-800">
                    Profile updated successfully!
                  </p>
                </div>
              </div>
            </div>

            <div v-if="profileError" class="rounded-md bg-red-50 p-4">
              <div class="text-sm text-red-700">
                {{ profileError }}
              </div>
            </div>

            <div class="flex justify-end">
              <button
                type="submit"
                :disabled="isUpdatingProfile"
                class="btn-primary"
                :class="{ 'opacity-50 cursor-not-allowed': isUpdatingProfile }"
              >
                <svg v-if="isUpdatingProfile" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ isUpdatingProfile ? 'Saving...' : 'Save Changes' }}
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Account Information -->
      <div class="bg-white shadow rounded-lg">
        <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
          <h3 class="text-lg leading-6 font-medium text-gray-900">Account Information</h3>
          <p class="mt-1 max-w-2xl text-sm text-gray-500">
            View your account details and current settings.
          </p>
        </div>
        <div class="px-4 py-5 sm:p-6">
          <dl class="divide-y divide-gray-200">
            <div class="py-4 sm:grid sm:grid-cols-3 sm:gap-4">
              <dt class="text-sm font-medium text-gray-500">Account ID</dt>
              <dd class="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
                {{ authStore.user?.id }}
              </dd>
            </div>
            <div class="py-4 sm:grid sm:grid-cols-3 sm:gap-4">
              <dt class="text-sm font-medium text-gray-500">Account type</dt>
              <dd class="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium" 
                      :class="authStore.user?.role === 'admin' ? 'bg-purple-100 text-purple-800' : 'bg-blue-100 text-blue-800'">
                  {{ authStore.user?.role === 'admin' ? 'Administrator' : 'Standard User' }}
                </span>
              </dd>
            </div>
            <div class="py-4 sm:grid sm:grid-cols-3 sm:gap-4">
              <dt class="text-sm font-medium text-gray-500">Authentication method</dt>
              <dd class="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
                {{ formatAuthProvider(authStore.user?.auth_provider) }}
              </dd>
            </div>
            <div class="py-4 sm:grid sm:grid-cols-3 sm:gap-4">
              <dt class="text-sm font-medium text-gray-500">Email verified</dt>
              <dd class="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
                <span v-if="authStore.user?.is_verified" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  <CheckCircleIcon class="w-3 h-3 mr-1" />
                  Verified
                </span>
                <span v-else class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                  <ExclamationTriangleIcon class="w-3 h-3 mr-1" />
                  Unverified
                </span>
              </dd>
            </div>
            <div class="py-4 sm:grid sm:grid-cols-3 sm:gap-4">
              <dt class="text-sm font-medium text-gray-500">Member since</dt>
              <dd class="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
                {{ formatDate(authStore.user?.created_at) }}
              </dd>
            </div>
            <div class="py-4 sm:grid sm:grid-cols-3 sm:gap-4">
              <dt class="text-sm font-medium text-gray-500">Last updated</dt>
              <dd class="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
                {{ formatDate(authStore.user?.updated_at) || 'Never' }}
              </dd>
            </div>
          </dl>
        </div>
      </div>

      <!-- Danger Zone -->
      <div class="bg-white shadow rounded-lg">
        <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
          <h3 class="text-lg leading-6 font-medium text-red-900">Danger Zone</h3>
          <p class="mt-1 max-w-2xl text-sm text-red-600">
            Irreversible and destructive actions.
          </p>
        </div>
        <div class="px-4 py-5 sm:p-6">
          <div class="rounded-md bg-red-50 p-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <ExclamationTriangleIcon class="h-5 w-5 text-red-400" />
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-red-800">
                  Account Deletion
                </h3>
                <div class="mt-2 text-sm text-red-700">
                  <p>
                    Once you delete your account, there is no going back. Please be certain.
                    This feature is not yet available - contact support if you need to delete your account.
                  </p>
                </div>
                <div class="mt-4">
                  <button
                    disabled
                    class="bg-red-600 text-white px-4 py-2 text-sm font-medium rounded-md opacity-50 cursor-not-allowed"
                  >
                    Delete Account (Coming Soon)
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '@/store/auth'
import { usersAPI } from '@/api/users'
import { CheckCircleIcon, ExclamationTriangleIcon } from '@heroicons/vue/24/outline'

const authStore = useAuthStore()

const profileForm = reactive({
  first_name: '',
  last_name: '',
})

const errors = reactive({
  first_name: '',
  last_name: '',
})

const profileSuccess = ref(false)
const profileError = ref('')
const isUpdatingProfile = ref(false)

const initializeForm = () => {
  if (authStore.user) {
    profileForm.first_name = authStore.user.first_name || ''
    profileForm.last_name = authStore.user.last_name || ''
  }
}

const validateProfileForm = () => {
  errors.first_name = ''
  errors.last_name = ''
  
  // Optional validation - names are not required but should be reasonable length if provided
  if (profileForm.first_name && profileForm.first_name.length > 50) {
    errors.first_name = 'First name must be less than 50 characters'
  }
  
  if (profileForm.last_name && profileForm.last_name.length > 50) {
    errors.last_name = 'Last name must be less than 50 characters'
  }
  
  return !Object.values(errors).some(Boolean)
}

const handleUpdateProfile = async () => {
  if (!validateProfileForm()) return
  
  try {
    isUpdatingProfile.value = true
    profileError.value = ''
    profileSuccess.value = false
    
    const updateData = {
      first_name: profileForm.first_name || undefined,
      last_name: profileForm.last_name || undefined,
    }
    
    const updatedUser = await usersAPI.updateProfile(updateData)
    
    // Update the auth store with new user data
    authStore.updateUser(updatedUser)
    
    profileSuccess.value = true
    
    // Hide success message after 3 seconds
    setTimeout(() => {
      profileSuccess.value = false
    }, 3000)
    
  } catch (err: any) {
    console.error('Profile update error:', err)
    profileError.value = err.response?.data?.detail || 'Failed to update profile. Please try again.'
  } finally {
    isUpdatingProfile.value = false
  }
}

const formatAuthProvider = (provider: string | undefined) => {
  if (!provider) return 'Unknown'
  
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

const formatDate = (dateString: string | undefined) => {
  if (!dateString) return null
  
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  initializeForm()
})
</script>