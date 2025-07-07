import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/auth/LoginView.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/auth/RegisterView.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/articles',
      name: 'articles',
      component: () => import('../views/articles/ArticleListView.vue'),
    },
    {
      path: '/articles/create',
      name: 'article-create',
      component: () => import('../views/articles/ArticleCreateView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/articles/:id',
      name: 'article-detail',
      component: () => import('../views/articles/ArticleDetailView.vue'),
    },
    {
      path: '/articles/:id/edit',
      name: 'article-edit',
      component: () => import('../views/articles/ArticleEditView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/user/ProfileView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/user/DashboardView.vue'),
      meta: { requiresAuth: true }
    }
  ],
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // 初始化用户信息
  if (authStore.accessToken && !authStore.user) {
    await authStore.initUser()
  }

  // 检查需要认证的路由
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
    return
  }

  // 检查需要游客身份的路由（如登录、注册页）
  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next({ name: 'home' })
    return
  }

  next()
})

export default router
