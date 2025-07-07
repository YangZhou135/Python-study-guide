/**
 * 认证API服务
 */

import apiClient, {
  type ApiResponse,
  type LoginRequest,
  type RegisterRequest,
  type AuthResponse,
  type User
} from './index'

export class AuthAPI {
  /**
   * 用户登录
   */
  static async login(data: LoginRequest): Promise<AuthResponse> {
    const response = await apiClient.post<ApiResponse<AuthResponse>>('/auth/login', data)
    return response.data.data!
  }

  /**
   * 用户注册
   */
  static async register(data: RegisterRequest): Promise<AuthResponse> {
    const response = await apiClient.post<ApiResponse<AuthResponse>>('/auth/register', data)
    return response.data.data!
  }

  /**
   * 获取当前用户信息
   */
  static async getCurrentUser(): Promise<User> {
    const response = await apiClient.get<ApiResponse<{ user: User }>>('/auth/me')
    return response.data.data!.user
  }

  /**
   * 刷新token
   */
  static async refreshToken(): Promise<{ access_token: string; expires_in: number }> {
    const refreshToken = localStorage.getItem('refresh_token')
    const response = await apiClient.post<ApiResponse<{ access_token: string; expires_in: number }>>(
      '/auth/refresh',
      { refresh_token: refreshToken }
    )
    return response.data.data!
  }

  /**
   * 用户登出
   */
  static async logout(): Promise<void> {
    try {
      await apiClient.post('/auth/logout')
    } finally {
      // 无论请求是否成功，都清除本地存储
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user_info')
    }
  }

  /**
   * 修改密码
   */
  static async changePassword(data: {
    current_password: string
    new_password: string
  }): Promise<void> {
    await apiClient.post<ApiResponse>('/auth/change-password', data)
  }

  /**
   * 检查用户名是否可用
   */
  static async checkUsername(username: string): Promise<{ available: boolean }> {
    const response = await apiClient.post<ApiResponse<{ available: boolean }>>(
      '/auth/check-username',
      { username }
    )
    return response.data.data!
  }

  /**
   * 检查邮箱是否可用
   */
  static async checkEmail(email: string): Promise<{ available: boolean }> {
    const response = await apiClient.post<ApiResponse<{ available: boolean }>>(
      '/auth/check-email',
      { email }
    )
    return response.data.data!
  }

  /**
   * 更新用户资料
   */
  static async updateProfile(data: {
    email?: string
    display_name?: string
    bio?: string
    website?: string
    location?: string
    avatar?: string
  }): Promise<User> {
    const response = await apiClient.put<ApiResponse<{ user: User }>>('/auth/profile', data)
    return response.data.data!.user
  }
}

export default AuthAPI
