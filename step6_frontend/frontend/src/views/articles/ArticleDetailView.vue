<template>
  <div class="article-detail-page">
    <div v-loading="loading" class="container">
      <div v-if="article" class="article-detail">
        <!-- 文章头部 -->
        <div class="article-header">
          <h1 class="article-title">{{ article.title }}</h1>
          
          <div class="article-meta">
            <div class="author-info">
              <el-avatar :size="40">
                {{ article.author.username.charAt(0).toUpperCase() }}
              </el-avatar>
              <div class="author-details">
                <div class="author-name">{{ article.author.username }}</div>
                <div class="publish-info">
                  发布于 {{ formatDate(article.created_at) }}
                  <span v-if="article.updated_at !== article.created_at">
                    · 更新于 {{ formatDate(article.updated_at) }}
                  </span>
                </div>
              </div>
            </div>
            
            <div class="article-actions">
              <el-button 
                v-if="canEdit" 
                type="primary" 
                @click="editArticle"
              >
                <el-icon><Edit /></el-icon>
                编辑
              </el-button>
              
              <el-button 
                :type="isLiked ? 'danger' : 'default'"
                @click="toggleLike"
                :disabled="!authStore.isAuthenticated"
              >
                <el-icon><Star /></el-icon>
                {{ article.likes }}
              </el-button>
              
              <el-dropdown @command="handleCommand">
                <el-button>
                  <el-icon><MoreFilled /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="share">分享文章</el-dropdown-item>
                    <el-dropdown-item 
                      v-if="canEdit" 
                      command="delete" 
                      divided
                    >
                      删除文章
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>
          
          <!-- 文章标签 -->
          <div v-if="article.tags?.length" class="article-tags">
            <el-tag 
              v-for="tag in article.tags" 
              :key="tag.id"
              type="info"
            >
              {{ tag.name }}
            </el-tag>
          </div>
          
          <!-- 文章统计 -->
          <div class="article-stats">
            <span class="stat-item">
              <el-icon><View /></el-icon>
              {{ article.views }} 次阅读
            </span>
            <span class="stat-item">
              <el-icon><ChatDotRound /></el-icon>
              {{ article.comment_count }} 条评论
            </span>
          </div>
        </div>

        <!-- 文章封面 -->
        <div v-if="article.featured_image" class="article-image">
          <img :src="article.featured_image" :alt="article.title" />
        </div>

        <!-- 文章摘要 -->
        <div v-if="article.summary" class="article-summary">
          <p>{{ article.summary }}</p>
        </div>

        <!-- 文章内容 -->
        <div class="article-content">
          <div v-html="formattedContent"></div>
        </div>

        <!-- 文章底部操作 -->
        <div class="article-footer">
          <div class="like-section">
            <el-button 
              :type="isLiked ? 'danger' : 'default'"
              size="large"
              @click="toggleLike"
              :disabled="!authStore.isAuthenticated"
            >
              <el-icon><Star /></el-icon>
              {{ isLiked ? '已点赞' : '点赞' }} ({{ article.likes }})
            </el-button>
          </div>
          
          <div class="share-section">
            <span>分享到：</span>
            <el-button-group>
              <el-button @click="shareToWeibo">微博</el-button>
              <el-button @click="shareToWechat">微信</el-button>
              <el-button @click="copyLink">复制链接</el-button>
            </el-button-group>
          </div>
        </div>
      </div>

      <!-- 评论区域 -->
      <div v-if="article" class="comments-section">
        <h3>评论 ({{ article.comment_count }})</h3>
        
        <!-- 发表评论 -->
        <div v-if="authStore.isAuthenticated" class="comment-form">
          <el-input
            v-model="newComment"
            type="textarea"
            :rows="4"
            placeholder="写下你的评论..."
            maxlength="500"
            show-word-limit
          />
          <div class="comment-actions">
            <el-button 
              type="primary" 
              @click="submitComment"
              :loading="commentLoading"
              :disabled="!newComment.trim()"
            >
              发表评论
            </el-button>
          </div>
        </div>
        
        <div v-else class="login-prompt">
          <p>
            <router-link to="/login">登录</router-link> 
            后参与评论讨论
          </p>
        </div>

        <!-- 评论列表 -->
        <div class="comments-list">
          <div v-if="comments.length === 0" class="empty-comments">
            <el-empty description="暂无评论，来发表第一条评论吧！" />
          </div>
          
          <div v-else>
            <div 
              v-for="comment in comments" 
              :key="comment.id"
              class="comment-item"
            >
              <div class="comment-avatar">
                <el-avatar :size="36">
                  {{ comment.author.username.charAt(0).toUpperCase() }}
                </el-avatar>
              </div>
              
              <div class="comment-content">
                <div class="comment-header">
                  <span class="comment-author">{{ comment.author.username }}</span>
                  <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
                </div>
                
                <div class="comment-text">{{ comment.content }}</div>
                
                <div class="comment-actions">
                  <el-button 
                    text 
                    size="small"
                    @click="replyToComment(comment.id)"
                  >
                    回复
                  </el-button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useArticlesStore } from '@/stores/articles'
import { useAuthStore } from '@/stores/auth'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Edit, Star, MoreFilled, View, ChatDotRound } from '@element-plus/icons-vue'
import type { Article, Comment } from '@/api'

const route = useRoute()
const router = useRouter()
const articlesStore = useArticlesStore()
const authStore = useAuthStore()

// 响应式数据
const loading = ref(false)
const commentLoading = ref(false)
const newComment = ref('')
const comments = ref<Comment[]>([])
const isLiked = ref(false)

// 计算属性
const article = computed(() => articlesStore.currentArticle)
const canEdit = computed(() => {
  return authStore.isAuthenticated && 
         authStore.user?.id === article.value?.author.id
})

const formattedContent = computed(() => {
  if (!article.value?.content) return ''
  // 简单的 Markdown 转 HTML（实际项目中应使用专业的 Markdown 解析器）
  return article.value.content
    .replace(/\n/g, '<br>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
})

// 生命周期
onMounted(async () => {
  const articleId = Number(route.params.id)
  if (articleId) {
    await loadArticle(articleId)
    await loadComments(articleId)
  }
})

// 方法
const loadArticle = async (id: number) => {
  loading.value = true
  try {
    await articlesStore.fetchArticle(id)
    // 检查用户是否已点赞
    if (authStore.isAuthenticated) {
      // TODO: 实现检查点赞状态的API
    }
  } finally {
    loading.value = false
  }
}

const loadComments = async (articleId: number) => {
  try {
    // TODO: 实现评论加载
    comments.value = []
  } catch (error) {
    console.error('加载评论失败:', error)
  }
}

const editArticle = () => {
  router.push(`/articles/${article.value?.id}/edit`)
}

const toggleLike = async () => {
  if (!authStore.isAuthenticated) {
    ElMessage.warning('请先登录')
    return
  }
  
  try {
    if (article.value) {
      await articlesStore.toggleLike(article.value.id)
      isLiked.value = !isLiked.value
    }
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const submitComment = async () => {
  if (!newComment.value.trim()) return
  
  commentLoading.value = true
  try {
    // TODO: 实现评论提交
    ElMessage.success('评论发表成功')
    newComment.value = ''
    // 重新加载评论
    if (article.value) {
      await loadComments(article.value.id)
    }
  } catch (error) {
    ElMessage.error('评论发表失败')
  } finally {
    commentLoading.value = false
  }
}

const replyToComment = (commentId: number) => {
  // TODO: 实现回复评论
  console.log('回复评论:', commentId)
}

const handleCommand = async (command: string) => {
  switch (command) {
    case 'share':
      await copyLink()
      break
    case 'delete':
      await deleteArticle()
      break
  }
}

const shareToWeibo = () => {
  const url = encodeURIComponent(window.location.href)
  const title = encodeURIComponent(article.value?.title || '')
  window.open(`https://service.weibo.com/share/share.php?url=${url}&title=${title}`)
}

const shareToWechat = () => {
  ElMessage.info('请复制链接分享到微信')
  copyLink()
}

const copyLink = async () => {
  try {
    await navigator.clipboard.writeText(window.location.href)
    ElMessage.success('链接已复制到剪贴板')
  } catch (error) {
    ElMessage.error('复制失败')
  }
}

const deleteArticle = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这篇文章吗？此操作不可恢复。',
      '确认删除',
      {
        confirmButtonText: '删除',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    if (article.value) {
      await articlesStore.deleteArticle(article.value.id)
      ElMessage.success('文章已删除')
      router.push('/articles')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
.article-detail-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.article-detail {
  background: white;
  border-radius: 12px;
  padding: 40px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.article-header {
  margin-bottom: 32px;
}

.article-title {
  font-size: 32px;
  font-weight: 700;
  color: #303133;
  line-height: 1.3;
  margin-bottom: 24px;
}

.article-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.author-name {
  font-weight: 600;
  color: #303133;
}

.publish-info {
  font-size: 14px;
  color: #909399;
}

.article-actions {
  display: flex;
  gap: 8px;
}

.article-tags {
  margin-bottom: 16px;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.article-stats {
  display: flex;
  gap: 24px;
  font-size: 14px;
  color: #909399;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.article-image {
  margin-bottom: 32px;
  text-align: center;
}

.article-image img {
  max-width: 100%;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.article-summary {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 32px;
  border-left: 4px solid #409eff;
}

.article-content {
  font-size: 16px;
  line-height: 1.8;
  color: #303133;
  margin-bottom: 40px;
}

.article-footer {
  border-top: 1px solid #ebeef5;
  padding-top: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.share-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.comments-section {
  background: white;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.comments-section h3 {
  margin-bottom: 24px;
  color: #303133;
}

.comment-form {
  margin-bottom: 32px;
}

.comment-actions {
  margin-top: 12px;
  text-align: right;
}

.login-prompt {
  text-align: center;
  padding: 24px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 32px;
}

.login-prompt a {
  color: #409eff;
  text-decoration: none;
}

.comment-item {
  display: flex;
  gap: 12px;
  padding: 16px 0;
  border-bottom: 1px solid #f0f0f0;
}

.comment-item:last-child {
  border-bottom: none;
}

.comment-content {
  flex: 1;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.comment-author {
  font-weight: 600;
  color: #303133;
}

.comment-date {
  font-size: 12px;
  color: #909399;
}

.comment-text {
  color: #606266;
  line-height: 1.6;
  margin-bottom: 8px;
}

.comment-actions {
  display: flex;
  gap: 8px;
}

@media (max-width: 768px) {
  .article-detail {
    padding: 24px;
  }
  
  .article-title {
    font-size: 24px;
  }
  
  .article-meta {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .article-footer {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
}
</style>
