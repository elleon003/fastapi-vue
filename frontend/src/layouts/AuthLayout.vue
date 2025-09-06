<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <RouterLink to="/" class="flex justify-center">
        <h1 class="text-3xl font-bold text-primary-600">{{ APP_NAME }}</h1>
      </RouterLink>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
        <RouterView />
      </div>
    </div>

    <div class="mt-8 text-center">
      <RouterLink to="/" class="text-sm text-gray-500 hover:text-gray-700">
        ← Back to home
      </RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { APP_NAME } from '@/constants'
</script>