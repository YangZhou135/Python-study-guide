/**
 * API服务层 - Stage 6 前后端集成
 * 统一管理所有API请求
 */

import axios, { type AxiosInstance, type AxiosResponse } from 'axios'
import { ElMessage } from 'element-plus'

// API配置
const API_BASE_URL = 'http://127.0.0.1:5000/api/v1'

// 创建axios实例
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器 - 添加认证token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 统一处理错误
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response
  },
  (error) => {
    if (error.response) {
      const { status, data } = error.response

      // 处理认证错误
      if (status === 401) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user_info')
        ElMessage.error('登录已过期，请重新登录')
        // 可以在这里跳转到登录页
        window.location.href = '/login'
        return Promise.reject(error)
      }

      // 显示错误消息
      const message = data?.error?.message || data?.message || '请求失败'
      ElMessage.error(message)
    } else {
      ElMessage.error('网络错误，请检查网络连接')
    }

    return Promise.reject(error)
  }
)

// API响应类型定义
export interface ApiResponse<T = any> {
  success: boolean
  code: string
  message: string
  data?: T
  timestamp: string
}

export interface PaginationInfo {
  page: number
  pages: number
  per_page: number
  total: number
  has_next: boolean
  has_prev: boolean
}

export interface PaginatedResponse<T = any> extends ApiResponse<T> {
  pagination: PaginationInfo
}

// 用户相关类型
export interface User {
  id: number
  username: string
  email: string
  display_name?: string
  bio?: string
  website?: string
  location?: string
  avatar?: string
  is_active: boolean
  created_at: string
  last_login?: string
  login_count: number
  statistics?: {
    articles_count: number
    comments_count: number
    draft_count: number
    total_likes: number
    total_views: number
  }
}

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
}

export interface AuthResponse {
  user: User
  tokens: {
    access_token: string
    refresh_token: string
    expires_in: number
    token_type: string
  }
}

// 文章相关类型
export interface Article {
  id: number
  title: string
  content: string
  summary: string
  slug: string
  is_published: boolean
  allow_comments: boolean
  featured_image?: string
  views: number
  likes: number
  comment_count: number
  created_at: string
  updated_at: string
  author: {
    id: number
    username: string
    avatar?: string
  }
  tags: Array<{
    id: number
    name: string
  }>
}

export interface CreateArticleRequest {
  title: string
  content: string
  summary?: string
  is_published?: boolean
  allow_comments?: boolean
  featured_image?: string
  tags?: string[]
}

// 评论相关类型
export interface Comment {
  id: number
  content: string
  created_at: string
  parent_id?: number
  replies_count?: number
  author: {
    id: number
    username: string
  }
  article: {
    id: number
    title: string
  }
}

export interface CreateCommentRequest {
  content: string
  article_id: number
  parent_id?: number
}

// 文件上传类型
export interface UploadResponse {
  file: {
    filename: string
    original_filename: string
    url: string
    size: number
    mime_type: string
    uploaded_at: string
    uploaded_by: string
    thumbnail_url?: string
  }
}

export default apiClient
