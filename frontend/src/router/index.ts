import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { USER_ROLES } from '@/constants'

// Layouts
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'
import DashboardLayout from '@/layouts/DashboardLayout.vue'

// Views
import Home from '@/views/Home.vue'
import Login from '@/views/auth/Login.vue'
import Register from '@/views/auth/Register.vue'
import MagicLink from '@/views/auth/MagicLink.vue'
import AuthCallback from '@/views/auth/AuthCallback.vue'
import AuthError from '@/views/auth/AuthError.vue'
import Dashboard from '@/views/dashboard/Dashboard.vue'
import UserSettings from '@/views/dashboard/UserSettings.vue'
import AdminDashboard from '@/views/admin/AdminDashboard.vue'
import UserManagement from '@/views/admin/UserManagement.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: DefaultLayout,
      children: [
        {
          path: '',
          name: 'home',
          component: Home,
        },
      ],
    },
    {
      path: '/auth',
      component: AuthLayout,
      children: [
        {
          path: 'login',
          name: 'login',
          component: Login,
          meta: { guest: true },
        },
        {
          path: 'register',
          name: 'register',
          component: Register,
          meta: { guest: true },
        },
        {
          path: 'magic-link',
          name: 'magic-link',
          component: MagicLink,
          meta: { guest: true },
        },
        {
          path: 'callback',
          name: 'auth-callback',
          component: AuthCallback,
        },
        {
          path: 'error',
          name: 'auth-error',
          component: AuthError,
        },
      ],
    },
    {
      path: '/dashboard',
      component: DashboardLayout,
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'dashboard',
          component: Dashboard,
        },
        {
          path: 'settings',
          name: 'user-settings',
          component: UserSettings,
        },
      ],
    },
    {
      path: '/admin',
      component: DashboardLayout,
      meta: { requiresAuth: true, requiresAdmin: true },
      children: [
        {
          path: '',
          name: 'admin-dashboard',
          component: AdminDashboard,
        },
        {
          path: 'users',
          name: 'user-management',
          component: UserManagement,
        },
      ],
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/views/NotFound.vue'),
    },
  ],
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Initialize auth store if not already done
  if (!authStore.user && localStorage.getItem('access_token')) {
    authStore.initFromStorage()
  }

  // Check if route requires authentication
  if (to.meta.requiresAuth) {
    if (!authStore.isAuthenticated) {
      next({ name: 'login', query: { redirect: to.fullPath } })
      return
    }

    // Check admin requirements
    if (to.meta.requiresAdmin && !authStore.isAdmin) {
      next({ name: 'dashboard' })
      return
    }
  }

  // Redirect authenticated users away from guest-only pages
  if (to.meta.guest && authStore.isAuthenticated) {
    if (authStore.isAdmin) {
      next({ name: 'admin-dashboard' })
    } else {
      next({ name: 'dashboard' })
    }
    return
  }

  next()
})

export default router