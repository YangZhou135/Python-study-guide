/**
 * 文章API服务
 */

import apiClient, { 
  type ApiResponse, 
  type PaginatedResponse,
  type Article, 
  type CreateArticleRequest 
} from './index'

export interface ArticleListParams {
  page?: number
  per_page?: number
  search?: string
  tag?: string
  author_id?: number
  is_published?: boolean
}

export class ArticlesAPI {
  /**
   * 获取文章列表
   */
  static async getArticles(params: ArticleListParams = {}): Promise<{
    articles: Article[]
    pagination: any
  }> {
    const response = await apiClient.get<PaginatedResponse<Article[]>>('/articles', { params })
    return {
      articles: response.data.data!,
      pagination: response.data.pagination
    }
  }

  /**
   * 获取单篇文章
   */
  static async getArticle(id: number): Promise<Article> {
    const response = await apiClient.get<ApiResponse<{ article: Article }>>(`/articles/${id}`)
    return response.data.data!.article
  }

  /**
   * 创建文章
   */
  static async createArticle(data: CreateArticleRequest): Promise<Article> {
    const response = await apiClient.post<ApiResponse<{ article: Article }>>('/articles', data)
    return response.data.data!.article
  }

  /**
   * 更新文章
   */
  static async updateArticle(id: number, data: Partial<CreateArticleRequest>): Promise<Article> {
    const response = await apiClient.put<ApiResponse<{ article: Article }>>(`/articles/${id}`, data)
    return response.data.data!.article
  }

  /**
   * 删除文章
   */
  static async deleteArticle(id: number): Promise<void> {
    await apiClient.delete(`/articles/${id}`)
  }

  /**
   * 点赞文章
   */
  static async likeArticle(id: number): Promise<{ liked: boolean; likes_count: number }> {
    const response = await apiClient.post<ApiResponse<{ liked: boolean; likes_count: number }>>(
      `/articles/${id}/like`
    )
    return response.data.data!
  }

  /**
   * 搜索文章
   */
  static async searchArticles(params: {
    q: string
    page?: number
    per_page?: number
  }): Promise<{
    articles: Article[]
    pagination: any
  }> {
    const response = await apiClient.get<PaginatedResponse<Article[]>>('/articles/search', { params })
    return {
      articles: response.data.data!,
      pagination: response.data.pagination
    }
  }
}

export default ArticlesAPI
