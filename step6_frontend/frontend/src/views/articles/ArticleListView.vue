<template>
  <div class="article-list-page">
    <div class="container">
      <!-- 页面头部 -->
      <div class="page-header">
        <h1 class="page-title">文章列表</h1>
        <div class="header-actions">
          <el-button 
            v-if="authStore.isAuthenticated"
            type="primary" 
            @click="$router.push('/articles/create')"
          >
            <el-icon><Edit /></el-icon>
            写文章
          </el-button>
        </div>
      </div>

      <!-- 搜索和筛选 -->
      <div class="search-section">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-input
              v-model="searchQuery"
              placeholder="搜索文章标题或内容..."
              clearable
              @keyup.enter="handleSearch"
            >
              <template #append>
                <el-button @click="handleSearch">
                  <el-icon><Search /></el-icon>
                </el-button>
              </template>
            </el-input>
          </el-col>
          <el-col :span="6">
            <el-select v-model="filterTag" placeholder="选择标签" clearable @change="handleFilter">
              <el-option label="全部" value="" />
              <el-option label="技术" value="技术" />
              <el-option label="生活" value="生活" />
              <el-option label="学习" value="学习" />
            </el-select>
          </el-col>
          <el-col :span="6">
            <el-select v-model="sortBy" @change="handleFilter">
              <el-option label="最新发布" value="created_at" />
              <el-option label="最多浏览" value="views" />
              <el-option label="最多点赞" value="likes" />
            </el-select>
          </el-col>
        </el-row>
      </div>

      <!-- 文章列表 -->
      <div v-loading="loading" class="articles-section">
        <div v-if="articles.length === 0 && !loading" class="empty-state">
          <el-empty description="暂无文章" />
        </div>
        
        <div v-else class="articles-grid">
          <div 
            v-for="article in articles" 
            :key="article.id"
            class="article-card"
            @click="goToArticle(article.id)"
          >
            <!-- 文章封面 -->
            <div class="article-image">
              <img 
                v-if="article.featured_image"
                :src="article.featured_image" 
                :alt="article.title"
              />
              <div v-else class="placeholder-image">
                <el-icon size="48"><Document /></el-icon>
              </div>
            </div>
            
            <!-- 文章内容 -->
            <div class="article-content">
              <h3 class="article-title">{{ article.title }}</h3>
              <p class="article-summary">{{ article.summary }}</p>
              
              <!-- 标签 -->
              <div class="article-tags">
                <el-tag 
                  v-for="tag in article.tags" 
                  :key="tag.id"
                  size="small"
                  type="info"
                >
                  {{ tag.name }}
                </el-tag>
              </div>
              
              <!-- 文章元信息 -->
              <div class="article-meta">
                <div class="author-info">
                  <el-avatar :size="24">
                    {{ article.author.username.charAt(0).toUpperCase() }}
                  </el-avatar>
                  <span class="author-name">{{ article.author.username }}</span>
                </div>
                
                <div class="article-stats">
                  <span class="stat-item">
                    <el-icon><View /></el-icon>
                    {{ article.views }}
                  </span>
                  <span class="stat-item">
                    <el-icon><Star /></el-icon>
                    {{ article.likes }}
                  </span>
                  <span class="stat-item">
                    <el-icon><ChatDotRound /></el-icon>
                    {{ article.comment_count }}
                  </span>
                </div>
                
                <div class="publish-date">
                  {{ formatDate(article.created_at) }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 分页 -->
      <div v-if="pagination.total > 0" class="pagination-section">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="pagination.total"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useArticlesStore } from '@/stores/articles'
import { useAuthStore } from '@/stores/auth'
import { Edit, Search, Document, View, Star, ChatDotRound } from '@element-plus/icons-vue'

const router = useRouter()
const articlesStore = useArticlesStore()
const authStore = useAuthStore()

// 响应式数据
const searchQuery = ref('')
const filterTag = ref('')
const sortBy = ref('created_at')
const currentPage = ref(1)
const pageSize = ref(10)

// 计算属性
const articles = computed(() => articlesStore.articles)
const pagination = computed(() => articlesStore.pagination)
const loading = computed(() => articlesStore.loading)

// 生命周期
onMounted(() => {
  loadArticles()
})

// 方法
const loadArticles = async () => {
  const params = {
    page: currentPage.value,
    per_page: pageSize.value,
    is_published: true
  }
  
  if (searchQuery.value) {
    params.search = searchQuery.value
  }
  
  if (filterTag.value) {
    params.tag = filterTag.value
  }
  
  await articlesStore.fetchArticles(params)
}

const handleSearch = () => {
  currentPage.value = 1
  loadArticles()
}

const handleFilter = () => {
  currentPage.value = 1
  loadArticles()
}

const handlePageChange = (page: number) => {
  currentPage.value = page
  loadArticles()
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
  loadArticles()
}

const goToArticle = (id: number) => {
  router.push(`/articles/${id}`)
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN')
}
</script>

<style scoped>
.article-list-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 24px 0;
  border-bottom: 1px solid #ebeef5;
}

.search-section {
  margin-bottom: 24px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.articles-section {
  margin-bottom: 24px;
}

.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
}

.article-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
}

.article-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.article-image {
  height: 200px;
  overflow: hidden;
}

.article-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.placeholder-image {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
  color: #909399;
}

.article-content {
  padding: 20px;
}

.article-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 8px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-summary {
  color: #606266;
  line-height: 1.6;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-tags {
  margin-bottom: 16px;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.article-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  color: #909399;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.author-name {
  font-weight: 500;
}

.article-stats {
  display: flex;
  gap: 12px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.pagination-section {
  display: flex;
  justify-content: center;
  padding: 24px 0;
}

.empty-state {
  text-align: center;
  padding: 60px 0;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .articles-grid {
    grid-template-columns: 1fr;
  }
  
  .article-meta {
    flex-direction: column;
    gap: 8px;
    align-items: flex-start;
  }
}
</style>
