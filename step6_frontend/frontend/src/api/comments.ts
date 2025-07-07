/**
 * 评论API服务
 */

import apiClient, { 
  type ApiResponse, 
  type PaginatedResponse,
  type Comment, 
  type CreateCommentRequest 
} from './index'

export interface CommentListParams {
  article_id?: number
  page?: number
  per_page?: number
  parent_id?: number
}

export class CommentsAPI {
  /**
   * 获取评论列表
   */
  static async getComments(params: CommentListParams = {}): Promise<{
    comments: Comment[]
    pagination: any
  }> {
    const response = await apiClient.get<PaginatedResponse<Comment[]>>('/comments', { params })
    return {
      comments: response.data.data!,
      pagination: response.data.pagination
    }
  }

  /**
   * 获取单条评论
   */
  static async getComment(id: number): Promise<Comment> {
    const response = await apiClient.get<ApiResponse<{ comment: Comment }>>(`/comments/${id}`)
    return response.data.data!.comment
  }

  /**
   * 创建评论
   */
  static async createComment(data: CreateCommentRequest): Promise<Comment> {
    const response = await apiClient.post<ApiResponse<{ comment: Comment }>>('/comments', data)
    return response.data.data!.comment
  }

  /**
   * 更新评论
   */
  static async updateComment(id: number, data: { content: string }): Promise<Comment> {
    const response = await apiClient.put<ApiResponse<{ comment: Comment }>>(`/comments/${id}`, data)
    return response.data.data!.comment
  }

  /**
   * 删除评论
   */
  static async deleteComment(id: number): Promise<void> {
    await apiClient.delete(`/comments/${id}`)
  }
}

export default CommentsAPI
