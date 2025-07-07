/**
 * 用户认证状态管理
 */
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { AuthAPI } from '@/api/auth'
import type { User, LoginRequest, RegisterRequest } from '@/api'

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const user = ref<User | null>(null)
  const accessToken = ref<string | null>(localStorage.getItem('access_token'))
  const refreshToken = ref<string | null>(localStorage.getItem('refresh_token'))
  const loading = ref(false)

  // 计算属性
  const isAuthenticated = computed(() => !!accessToken.value && !!user.value)
  const isAdmin = computed(() => user.value?.username === 'admin')

  // 初始化用户信息
  const initUser = async () => {
    if (accessToken.value && !user.value) {
      try {
        const userData = await AuthAPI.getCurrentUser()
        user.value = userData
      } catch (error) {
        // token可能已过期，清除本地存储
        logout()
      }
    }
  }

  // 登录
  const login = async (credentials: LoginRequest) => {
    loading.value = true
    try {
      const response = await AuthAPI.login(credentials)

      // 保存token和用户信息
      accessToken.value = response.tokens.access_token
      refreshToken.value = response.tokens.refresh_token
      user.value = response.user

      // 保存到localStorage
      localStorage.setItem('access_token', response.tokens.access_token)
      localStorage.setItem('refresh_token', response.tokens.refresh_token)
      localStorage.setItem('user_info', JSON.stringify(response.user))

      return response
    } finally {
      loading.value = false
    }
  }

  // 注册
  const register = async (data: RegisterRequest) => {
    loading.value = true
    try {
      const response = await AuthAPI.register(data)

      // 注册成功后自动登录
      accessToken.value = response.tokens.access_token
      refreshToken.value = response.tokens.refresh_token
      user.value = response.user

      // 保存到localStorage
      localStorage.setItem('access_token', response.tokens.access_token)
      localStorage.setItem('refresh_token', response.tokens.refresh_token)
      localStorage.setItem('user_info', JSON.stringify(response.user))

      return response
    } finally {
      loading.value = false
    }
  }

  // 登出
  const logout = async () => {
    try {
      await AuthAPI.logout()
    } finally {
      // 清除状态
      user.value = null
      accessToken.value = null
      refreshToken.value = null

      // 清除localStorage
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user_info')
    }
  }

  // 刷新token
  const refreshAccessToken = async () => {
    try {
      const response = await AuthAPI.refreshToken()
      accessToken.value = response.access_token
      localStorage.setItem('access_token', response.access_token)
      return response
    } catch (error) {
      // 刷新失败，登出用户
      logout()
      throw error
    }
  }

  return {
    // 状态
    user,
    accessToken,
    refreshToken,
    loading,

    // 计算属性
    isAuthenticated,
    isAdmin,

    // 方法
    initUser,
    login,
    register,
    logout,
    refreshAccessToken
  }
})
