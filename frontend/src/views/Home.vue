<template>
  <div>
    <!-- Hero Section -->
    <div class="relative bg-gradient-to-r from-primary-600 to-primary-700 overflow-hidden">
      <div class="max-w-7xl mx-auto">
        <div class="relative z-10 pb-8 sm:pb-16 md:pb-20 lg:max-w-2xl lg:w-full lg:pb-28 xl:pb-32">
          <main class="mt-10 mx-auto max-w-7xl px-4 sm:mt-12 sm:px-6 md:mt-16 lg:mt-20 lg:px-8 xl:mt-28">
            <div class="sm:text-center lg:text-left">
              <h1 class="text-4xl tracking-tight font-extrabold text-white sm:text-5xl md:text-6xl">
                <span class="block xl:inline">Welcome to</span>
                <span class="block text-primary-200 xl:inline">{{ APP_NAME }}</span>
              </h1>
              <p class="mt-3 text-base text-primary-100 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0">
                A modern full-stack starter template built with FastAPI and Vue.js. Features comprehensive authentication, user management, and role-based permissions out of the box.
              </p>
              <div class="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start">
                <div class="rounded-md shadow">
                  <RouterLink
                    v-if="!authStore.isAuthenticated"
                    to="/auth/register"
                    class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-primary-700 bg-white hover:bg-gray-50 md:py-4 md:text-lg md:px-10"
                  >
                    Get started
                  </RouterLink>
                  <RouterLink
                    v-else
                    :to="authStore.isAdmin ? '/admin' : '/dashboard'"
                    class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-primary-700 bg-white hover:bg-gray-50 md:py-4 md:text-lg md:px-10"
                  >
                    Go to Dashboard
                  </RouterLink>
                </div>
                <div class="mt-3 sm:mt-0 sm:ml-3">
                  <a
                    href="#features"
                    class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-500 hover:bg-primary-600 md:py-4 md:text-lg md:px-10"
                  >
                    Learn more
                  </a>
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
      <div class="lg:absolute lg:inset-y-0 lg:right-0 lg:w-1/2">
        <div class="h-56 w-full bg-primary-800 sm:h-72 md:h-96 lg:w-full lg:h-full flex items-center justify-center">
          <div class="text-primary-200 text-8xl font-light">🚀</div>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div id="features" class="py-12 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="lg:text-center">
          <h2 class="text-base text-primary-600 font-semibold tracking-wide uppercase">Features</h2>
          <p class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
            Everything you need to get started
          </p>
          <p class="mt-4 max-w-2xl text-xl text-gray-500 lg:mx-auto">
            Built with modern technologies and best practices for scalable web applications.
          </p>
        </div>

        <div class="mt-10">
          <div class="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10">
            <div class="relative">
              <dt>
                <div class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white">
                  <ShieldCheckIcon class="h-6 w-6" />
                </div>
                <p class="ml-16 text-lg leading-6 font-medium text-gray-900">Multiple Authentication Methods</p>
              </dt>
              <dd class="mt-2 ml-16 text-base text-gray-500">
                Support for email/password, Google OAuth, LinkedIn OAuth, and magic link authentication.
              </dd>
            </div>

            <div class="relative">
              <dt>
                <div class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white">
                  <UsersIcon class="h-6 w-6" />
                </div>
                <p class="ml-16 text-lg leading-6 font-medium text-gray-900">Role-Based Access Control</p>
              </dt>
              <dd class="mt-2 ml-16 text-base text-gray-500">
                Built-in user roles (admin/user) with appropriate permissions and route guards.
              </dd>
            </div>

            <div class="relative">
              <dt>
                <div class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white">
                  <CogIcon class="h-6 w-6" />
                </div>
                <p class="ml-16 text-lg leading-6 font-medium text-gray-900">Modern Tech Stack</p>
              </dt>
              <dd class="mt-2 ml-16 text-base text-gray-500">
                FastAPI backend with SQLAlchemy, Vue.js 3 with Composition API, TypeScript, and Tailwind CSS.
              </dd>
            </div>

            <div class="relative">
              <dt>
                <div class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white">
                  <ChartBarIcon class="h-6 w-6" />
                </div>
                <p class="ml-16 text-lg leading-6 font-medium text-gray-900">Admin Dashboard</p>
              </dt>
              <dd class="mt-2 ml-16 text-base text-gray-500">
                Comprehensive admin interface for user management and system oversight.
              </dd>
            </div>

            <div class="relative">
              <dt>
                <div class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white">
                  <ServerIcon class="h-6 w-6" />
                </div>
                <p class="ml-16 text-lg leading-6 font-medium text-gray-900">Database Flexibility</p>
              </dt>
              <dd class="mt-2 ml-16 text-base text-gray-500">
                SQLite for development, PostgreSQL for production, with Alembic migrations.
              </dd>
            </div>

            <div class="relative">
              <dt>
                <div class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white">
                  <DocumentTextIcon class="h-6 w-6" />
                </div>
                <p class="ml-16 text-lg leading-6 font-medium text-gray-900">Auto-Generated API Docs</p>
              </dt>
              <dd class="mt-2 ml-16 text-base text-gray-500">
                Interactive API documentation with Swagger UI and ReDoc out of the box.
              </dd>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Authentication Methods Section -->
    <div class="bg-gray-50 py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="lg:text-center">
          <h2 class="text-base text-primary-600 font-semibold tracking-wide uppercase">Authentication</h2>
          <p class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
            Multiple ways to sign in
          </p>
        </div>

        <div class="mt-10 grid gap-8 md:grid-cols-2 lg:grid-cols-4">
          <div class="bg-white p-6 rounded-lg shadow-sm text-center">
            <div class="text-primary-600 text-3xl mb-4">📧</div>
            <h3 class="font-medium text-gray-900">Email & Password</h3>
            <p class="text-sm text-gray-500 mt-2">Traditional authentication with secure password hashing</p>
          </div>

          <div class="bg-white p-6 rounded-lg shadow-sm text-center">
            <div class="text-primary-600 text-3xl mb-4">🔗</div>
            <h3 class="font-medium text-gray-900">Google OAuth</h3>
            <p class="text-sm text-gray-500 mt-2">Sign in with your Google account</p>
          </div>

          <div class="bg-white p-6 rounded-lg shadow-sm text-center">
            <div class="text-primary-600 text-3xl mb-4">💼</div>
            <h3 class="font-medium text-gray-900">LinkedIn OAuth</h3>
            <p class="text-sm text-gray-500 mt-2">Professional authentication via LinkedIn</p>
          </div>

          <div class="bg-white p-6 rounded-lg shadow-sm text-center">
            <div class="text-primary-600 text-3xl mb-4">✨</div>
            <h3 class="font-medium text-gray-900">Magic Links</h3>
            <p class="text-sm text-gray-500 mt-2">Passwordless authentication via email</p>
          </div>
        </div>
      </div>
    </div>

    <!-- CTA Section -->
    <div class="bg-primary-600">
      <div class="max-w-2xl mx-auto text-center py-16 px-4 sm:py-20 sm:px-6 lg:px-8">
        <h2 class="text-3xl font-extrabold text-white sm:text-4xl">
          <span class="block">Ready to get started?</span>
          <span class="block">Create your account today.</span>
        </h2>
        <p class="mt-4 text-lg leading-6 text-primary-200">
          Join thousands of developers building modern web applications.
        </p>
        <div class="mt-8 flex justify-center space-x-4">
          <RouterLink
            v-if="!authStore.isAuthenticated"
            to="/auth/register"
            class="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-primary-600 bg-white hover:bg-primary-50"
          >
            Sign up free
          </RouterLink>
          <RouterLink
            v-if="!authStore.isAuthenticated"
            to="/auth/login"
            class="inline-flex items-center justify-center px-5 py-3 border border-white text-base font-medium rounded-md text-white hover:bg-primary-700"
          >
            Sign in
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { APP_NAME } from '@/constants'
import {
  ShieldCheckIcon,
  UsersIcon,
  CogIcon,
  ChartBarIcon,
  ServerIcon,
  DocumentTextIcon,
} from '@heroicons/vue/24/outline'

const authStore = useAuthStore()
</script>