/**
 * 文件上传API服务
 */

import apiClient, { type ApiResponse, type UploadResponse } from './index'

export class UploadAPI {
  /**
   * 上传图片
   */
  static async uploadImage(file: File): Promise<UploadResponse['file']> {
    const formData = new FormData()
    formData.append('file', file)

    const response = await apiClient.post<ApiResponse<UploadResponse>>(
      '/upload/image',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    )
    return response.data.data!.file
  }

  /**
   * 上传文件
   */
  static async uploadFile(file: File): Promise<UploadResponse['file']> {
    const formData = new FormData()
    formData.append('file', file)

    const response = await apiClient.post<ApiResponse<UploadResponse>>(
      '/upload/file',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    )
    return response.data.data!.file
  }

  /**
   * 获取文件URL
   */
  static getFileUrl(path: string): string {
    if (path.startsWith('http')) {
      return path
    }
    return `http://localhost:5000${path}`
  }
}

export default UploadAPI
