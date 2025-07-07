<template>
  <div class="dashboard-page">
    <div class="container">
      <div class="dashboard-header">
        <h1>控制台</h1>
        <p>欢迎回来，{{ authStore.user?.username }}！</p>
      </div>

      <!-- 统计卡片 -->
      <div class="stats-section">
        <el-row :gutter="24">
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon">
                <el-icon size="32" color="#409eff"><Document /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ stats.article_count }}</div>
                <div class="stat-label">我的文章</div>
              </div>
            </div>
          </el-col>
          
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon">
                <el-icon size="32" color="#67c23a"><View /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ stats.total_views }}</div>
                <div class="stat-label">总阅读量</div>
              </div>
            </div>
          </el-col>
          
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon">
                <el-icon size="32" color="#e6a23c"><Star /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ stats.total_likes }}</div>
                <div class="stat-label">获得点赞</div>
              </div>
            </div>
          </el-col>
          
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon">
                <el-icon size="32" color="#f56c6c"><ChatDotRound /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ stats.comment_count }}</div>
                <div class="stat-label">收到评论</div>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>

      <el-row :gutter="24">
        <!-- 左侧：我的文章 -->
        <el-col :span="16">
          <div class="dashboard-card">
            <div class="card-header">
              <h2>我的文章</h2>
              <div class="card-actions">
                <el-button type="primary" @click="$router.push('/articles/create')">
                  <el-icon><Edit /></el-icon>
                  写文章
                </el-button>
              </div>
            </div>

            <div class="article-tabs">
              <el-tabs v-model="activeTab" @tab-change="handleTabChange">
                <el-tab-pane label="全部" name="all" />
                <el-tab-pane label="已发布" name="published" />
                <el-tab-pane label="草稿" name="draft" />
              </el-tabs>
            </div>

            <div v-loading="articlesLoading" class="articles-list">
              <div v-if="myArticles.length === 0" class="empty-state">
                <el-empty description="暂无文章" />
                <el-button type="primary" @click="$router.push('/articles/create')">
                  开始写作
                </el-button>
              </div>
              
              <div v-else class="article-items">
                <div 
                  v-for="article in myArticles" 
                  :key="article.id"
                  class="article-item"
                >
                  <div class="article-info">
                    <h3 class="article-title" @click="goToArticle(article.id)">
                      {{ article.title }}
                    </h3>
                    <p class="article-summary">{{ article.summary }}</p>
                    
                    <div class="article-meta">
                      <el-tag 
                        :type="article.is_published ? 'success' : 'info'"
                        size="small"
                      >
                        {{ article.is_published ? '已发布' : '草稿' }}
                      </el-tag>
                      
                      <span class="meta-item">
                        <el-icon><View /></el-icon>
                        {{ article.views }}
                      </span>
                      
                      <span class="meta-item">
                        <el-icon><Star /></el-icon>
                        {{ article.likes }}
                      </span>
                      
                      <span class="meta-item">
                        <el-icon><ChatDotRound /></el-icon>
                        {{ article.comment_count }}
                      </span>
                      
                      <span class="meta-date">
                        {{ formatDate(article.created_at) }}
                      </span>
                    </div>
                  </div>
                  
                  <div class="article-actions">
                    <el-button 
                      size="small" 
                      @click="editArticle(article.id)"
                    >
                      编辑
                    </el-button>
                    
                    <el-dropdown @command="(command) => handleArticleAction(command, article)">
                      <el-button size="small">
                        更多
                        <el-icon><ArrowDown /></el-icon>
                      </el-button>
                      <template #dropdown>
                        <el-dropdown-menu>
                          <el-dropdown-item 
                            :command="`${article.is_published ? 'unpublish' : 'publish'}`"
                          >
                            {{ article.is_published ? '取消发布' : '发布' }}
                          </el-dropdown-item>
                          <el-dropdown-item command="duplicate">
                            复制文章
                          </el-dropdown-item>
                          <el-dropdown-item command="delete" divided>
                            删除文章
                          </el-dropdown-item>
                        </el-dropdown-menu>
                      </template>
                    </el-dropdown>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-col>

        <!-- 右侧：快捷操作和最新动态 -->
        <el-col :span="8">
          <!-- 快捷操作 -->
          <div class="dashboard-card">
            <h2>快捷操作</h2>
            
            <div class="quick-actions">
              <el-button 
                type="primary" 
                size="large" 
                style="width: 100%; margin-bottom: 12px;"
                @click="$router.push('/articles/create')"
              >
                <el-icon><Edit /></el-icon>
                写新文章
              </el-button>
              
              <el-button 
                size="large" 
                style="width: 100%; margin-bottom: 12px;"
                @click="$router.push('/profile')"
              >
                <el-icon><User /></el-icon>
                编辑资料
              </el-button>
              
              <el-button 
                size="large" 
                style="width: 100%;"
                @click="$router.push('/articles')"
              >
                <el-icon><Reading /></el-icon>
                浏览文章
              </el-button>
            </div>
          </div>

          <!-- 最新评论 -->
          <div class="dashboard-card">
            <h2>最新评论</h2>
            
            <div v-if="recentComments.length === 0" class="empty-state">
              <el-empty description="暂无评论" :image-size="80" />
            </div>
            
            <div v-else class="comments-list">
              <div 
                v-for="comment in recentComments" 
                :key="comment.id"
                class="comment-item"
              >
                <div class="comment-header">
                  <span class="commenter">{{ comment.author.username }}</span>
                  <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
                </div>
                
                <div class="comment-content">{{ comment.content }}</div>
                
                <div class="comment-article">
                  评论于：
                  <a @click="goToArticle(comment.article.id)">
                    {{ comment.article.title }}
                  </a>
                </div>
              </div>
            </div>
          </div>

          <!-- 数据趋势 -->
          <div class="dashboard-card">
            <h2>本月数据</h2>
            
            <div class="trend-stats">
              <div class="trend-item">
                <div class="trend-label">新增文章</div>
                <div class="trend-value">
                  {{ monthlyStats.new_articles }}
                  <span class="trend-change positive">+{{ monthlyStats.articles_change }}%</span>
                </div>
              </div>
              
              <div class="trend-item">
                <div class="trend-label">新增阅读</div>
                <div class="trend-value">
                  {{ monthlyStats.new_views }}
                  <span class="trend-change positive">+{{ monthlyStats.views_change }}%</span>
                </div>
              </div>
              
              <div class="trend-item">
                <div class="trend-label">新增点赞</div>
                <div class="trend-value">
                  {{ monthlyStats.new_likes }}
                  <span class="trend-change positive">+{{ monthlyStats.likes_change }}%</span>
                </div>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useArticlesStore } from '@/stores/articles'
import { useAuthStore } from '@/stores/auth'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Document, View, Star, ChatDotRound, Edit, User, Reading, ArrowDown 
} from '@element-plus/icons-vue'
import type { Article, Comment } from '@/api'

const router = useRouter()
const articlesStore = useArticlesStore()
const authStore = useAuthStore()

// 响应式数据
const activeTab = ref('all')
const articlesLoading = ref(false)

// 统计数据
const stats = ref({
  article_count: 0,
  total_views: 0,
  total_likes: 0,
  comment_count: 0
})

// 月度统计
const monthlyStats = ref({
  new_articles: 3,
  articles_change: 25,
  new_views: 156,
  views_change: 18,
  new_likes: 23,
  likes_change: 12
})

// 我的文章
const myArticles = ref<Article[]>([])

// 最新评论
const recentComments = ref<Comment[]>([])

// 计算属性
const filteredArticles = computed(() => {
  switch (activeTab.value) {
    case 'published':
      return myArticles.value.filter(article => article.is_published)
    case 'draft':
      return myArticles.value.filter(article => !article.is_published)
    default:
      return myArticles.value
  }
})

// 生命周期
onMounted(() => {
  loadDashboardData()
})

// 方法
const loadDashboardData = async () => {
  await Promise.all([
    loadMyArticles(),
    loadStats(),
    loadRecentComments()
  ])
}

const loadMyArticles = async () => {
  articlesLoading.value = true
  try {
    // TODO: 实现加载用户文章的API
    myArticles.value = []
  } catch (error) {
    ElMessage.error('加载文章失败')
  } finally {
    articlesLoading.value = false
  }
}

const loadStats = async () => {
  try {
    // TODO: 实现加载用户统计的API
    stats.value = {
      article_count: 12,
      total_views: 1580,
      total_likes: 89,
      comment_count: 45
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

const loadRecentComments = async () => {
  try {
    // TODO: 实现加载最新评论的API
    recentComments.value = []
  } catch (error) {
    console.error('加载评论失败:', error)
  }
}

const handleTabChange = (tabName: string) => {
  activeTab.value = tabName
}

const goToArticle = (id: number) => {
  router.push(`/articles/${id}`)
}

const editArticle = (id: number) => {
  router.push(`/articles/${id}/edit`)
}

const handleArticleAction = async (command: string, article: Article) => {
  const [action, articleId] = command.includes('_') ? 
    command.split('_') : [command, article.id]

  switch (action) {
    case 'publish':
    case 'unpublish':
      await togglePublishStatus(article)
      break
    case 'duplicate':
      await duplicateArticle(article)
      break
    case 'delete':
      await deleteArticle(article)
      break
  }
}

const togglePublishStatus = async (article: Article) => {
  try {
    const newStatus = !article.is_published
    await articlesStore.updateArticle(article.id, { 
      is_published: newStatus 
    })
    
    article.is_published = newStatus
    ElMessage.success(newStatus ? '文章已发布' : '文章已取消发布')
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const duplicateArticle = async (article: Article) => {
  try {
    const duplicateData = {
      title: `${article.title} - 副本`,
      content: article.content,
      summary: article.summary,
      is_published: false
    }
    
    await articlesStore.createArticle(duplicateData)
    ElMessage.success('文章已复制')
    await loadMyArticles()
  } catch (error) {
    ElMessage.error('复制失败')
  }
}

const deleteArticle = async (article: Article) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除文章"${article.title}"吗？此操作不可恢复。`,
      '确认删除',
      {
        confirmButtonText: '删除',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await articlesStore.deleteArticle(article.id)
    ElMessage.success('文章已删除')
    await loadMyArticles()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN', {
    month: 'short',
    day: 'numeric'
  })
}
</script>

<style scoped>
.dashboard-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 32px;
  padding: 32px 0;
}

.dashboard-header h1 {
  font-size: 32px;
  color: #303133;
  margin-bottom: 8px;
}

.dashboard-header p {
  color: #606266;
  font-size: 16px;
}

.stats-section {
  margin-bottom: 32px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 28px;
  font-weight: 700;
  color: #303133;
  margin-bottom: 4px;
}

.stat-label {
  color: #909399;
  font-size: 14px;
}

.dashboard-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.dashboard-card h2 {
  color: #303133;
  margin-bottom: 20px;
  font-size: 18px;
  font-weight: 600;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-header h2 {
  margin: 0;
}

.article-tabs {
  margin-bottom: 20px;
}

.articles-list {
  min-height: 200px;
}

.empty-state {
  text-align: center;
  padding: 40px 0;
}

.article-items {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.article-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 16px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  transition: border-color 0.3s;
}

.article-item:hover {
  border-color: #c6e2ff;
}

.article-info {
  flex: 1;
}

.article-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 8px;
  cursor: pointer;
  line-height: 1.4;
}

.article-title:hover {
  color: #409eff;
}

.article-summary {
  color: #606266;
  font-size: 14px;
  margin-bottom: 12px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 12px;
  color: #909399;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.meta-date {
  margin-left: auto;
}

.article-actions {
  display: flex;
  gap: 8px;
  margin-left: 16px;
}

.quick-actions {
  display: flex;
  flex-direction: column;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.comment-item {
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.commenter {
  font-weight: 500;
  color: #303133;
  font-size: 14px;
}

.comment-date {
  font-size: 12px;
  color: #909399;
}

.comment-content {
  color: #606266;
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 8px;
}

.comment-article {
  font-size: 12px;
  color: #909399;
}

.comment-article a {
  color: #409eff;
  cursor: pointer;
  text-decoration: none;
}

.comment-article a:hover {
  text-decoration: underline;
}

.trend-stats {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.trend-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.trend-item:last-child {
  border-bottom: none;
}

.trend-label {
  color: #606266;
  font-size: 14px;
}

.trend-value {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #303133;
}

.trend-change {
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 4px;
}

.trend-change.positive {
  background: #f0f9ff;
  color: #67c23a;
}

@media (max-width: 768px) {
  .stats-section :deep(.el-col) {
    width: 50% !important;
    margin-bottom: 16px;
  }
  
  .dashboard-card {
    padding: 16px;
  }
  
  .article-item {
    flex-direction: column;
    gap: 12px;
  }
  
  .article-actions {
    margin-left: 0;
    align-self: stretch;
  }
}
</style>
