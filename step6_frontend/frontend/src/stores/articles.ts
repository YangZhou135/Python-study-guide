/**
 * 文章状态管理
 */
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { ArticlesAPI } from '@/api/articles'
import type { Article, CreateArticleRequest } from '@/api'

export const useArticlesStore = defineStore('articles', () => {
  // 状态
  const articles = ref<Article[]>([])
  const currentArticle = ref<Article | null>(null)
  const loading = ref(false)
  const pagination = ref({
    page: 1,
    pages: 1,
    per_page: 10,
    total: 0,
    has_next: false,
    has_prev: false
  })

  // 计算属性
  const publishedArticles = computed(() => 
    articles.value.filter(article => article.is_published)
  )
  
  const draftArticles = computed(() => 
    articles.value.filter(article => !article.is_published)
  )

  // 获取文章列表
  const fetchArticles = async (params: any = {}) => {
    loading.value = true
    try {
      const response = await ArticlesAPI.getArticles(params)
      articles.value = response.articles
      pagination.value = response.pagination
    } finally {
      loading.value = false
    }
  }

  // 获取单篇文章
  const fetchArticle = async (id: number) => {
    loading.value = true
    try {
      const article = await ArticlesAPI.getArticle(id)
      currentArticle.value = article
      return article
    } finally {
      loading.value = false
    }
  }

  // 创建文章
  const createArticle = async (data: CreateArticleRequest) => {
    loading.value = true
    try {
      const article = await ArticlesAPI.createArticle(data)
      articles.value.unshift(article)
      return article
    } finally {
      loading.value = false
    }
  }

  // 更新文章
  const updateArticle = async (id: number, data: Partial<CreateArticleRequest>) => {
    loading.value = true
    try {
      const article = await ArticlesAPI.updateArticle(id, data)
      
      // 更新列表中的文章
      const index = articles.value.findIndex(a => a.id === id)
      if (index !== -1) {
        articles.value[index] = article
      }
      
      // 更新当前文章
      if (currentArticle.value?.id === id) {
        currentArticle.value = article
      }
      
      return article
    } finally {
      loading.value = false
    }
  }

  // 删除文章
  const deleteArticle = async (id: number) => {
    loading.value = true
    try {
      await ArticlesAPI.deleteArticle(id)
      
      // 从列表中移除
      const index = articles.value.findIndex(a => a.id === id)
      if (index !== -1) {
        articles.value.splice(index, 1)
      }
      
      // 清除当前文章
      if (currentArticle.value?.id === id) {
        currentArticle.value = null
      }
    } finally {
      loading.value = false
    }
  }

  // 点赞文章
  const likeArticle = async (id: number) => {
    try {
      const response = await ArticlesAPI.likeArticle(id)
      
      // 更新列表中的文章
      const index = articles.value.findIndex(a => a.id === id)
      if (index !== -1) {
        articles.value[index].likes = response.likes_count
      }
      
      // 更新当前文章
      if (currentArticle.value?.id === id) {
        currentArticle.value.likes = response.likes_count
      }
      
      return response
    } catch (error) {
      throw error
    }
  }

  // 搜索文章
  const searchArticles = async (query: string, params: any = {}) => {
    loading.value = true
    try {
      const response = await ArticlesAPI.searchArticles({ q: query, ...params })
      articles.value = response.articles
      pagination.value = response.pagination
      return response
    } finally {
      loading.value = false
    }
  }

  // 清除当前文章
  const clearCurrentArticle = () => {
    currentArticle.value = null
  }

  return {
    // 状态
    articles,
    currentArticle,
    loading,
    pagination,
    
    // 计算属性
    publishedArticles,
    draftArticles,
    
    // 方法
    fetchArticles,
    fetchArticle,
    createArticle,
    updateArticle,
    deleteArticle,
    likeArticle,
    searchArticles,
    clearCurrentArticle
  }
})
