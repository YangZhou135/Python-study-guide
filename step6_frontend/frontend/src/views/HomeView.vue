<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useArticlesStore } from '@/stores/articles'
import { useAuthStore } from '@/stores/auth'
import type { Article } from '@/api'

const router = useRouter()
const articlesStore = useArticlesStore()
const authStore = useAuthStore()

const featuredArticles = ref<Article[]>([])
const loading = ref(false)

onMounted(async () => {
  await loadFeaturedArticles()
})

const loadFeaturedArticles = async () => {
  loading.value = true
  try {
    await articlesStore.fetchArticles({
      per_page: 6,
      is_published: true
    })
    featuredArticles.value = articlesStore.articles
  } finally {
    loading.value = false
  }
}

const goToArticle = (id: number) => {
  router.push(`/articles/${id}`)
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN')
}
</script>

<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="container">
        <div class="hero-content">
          <h1 class="hero-title">欢迎来到个人博客</h1>
          <p class="hero-subtitle">
            分享技术心得，记录学习历程，探索编程世界
          </p>
          <div class="hero-actions">
            <el-button
              type="primary"
              size="large"
              @click="router.push('/articles')"
            >
              浏览文章
            </el-button>
            <el-button
              v-if="authStore.isAuthenticated"
              size="large"
              @click="router.push('/articles/create')"
            >
              开始写作
            </el-button>
            <el-button
              v-else
              size="large"
              @click="router.push('/register')"
            >
              加入我们
            </el-button>
          </div>
        </div>
      </div>
    </section>

    <!-- Featured Articles -->
    <section class="featured-section">
      <div class="container">
        <h2 class="section-title">精选文章</h2>

        <div v-if="loading" class="loading-container">
          <el-loading-spinner />
        </div>

        <div v-else class="articles-grid">
          <div
            v-for="article in featuredArticles"
            :key="article.id"
            class="article-card"
            @click="goToArticle(article.id)"
          >
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

            <div class="article-content">
              <h3 class="article-title">{{ article.title }}</h3>
              <p class="article-summary">{{ article.summary }}</p>

              <div class="article-meta">
                <span class="author">{{ article.author.username }}</span>
                <span class="date">{{ formatDate(article.created_at) }}</span>
                <div class="stats">
                  <span><el-icon><View /></el-icon> {{ article.views }}</span>
                  <span><el-icon><Star /></el-icon> {{ article.likes }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="more-articles">
          <el-button @click="router.push('/articles')">
            查看更多文章
          </el-button>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-page {
  min-height: 100vh;
}

.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 80px 0;
  text-align: center;
}

.hero-title {
  font-size: 48px;
  font-weight: 700;
  margin-bottom: 16px;
}

.hero-subtitle {
  font-size: 20px;
  margin-bottom: 32px;
  opacity: 0.9;
}

.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.featured-section {
  padding: 60px 0;
  background: white;
}

.section-title {
  text-align: center;
  font-size: 32px;
  font-weight: 600;
  margin-bottom: 40px;
  color: #303133;
}

.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.article-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
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
  margin-bottom: 8px;
  color: #303133;
  line-height: 1.4;
}

.article-summary {
  color: #606266;
  line-height: 1.6;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  color: #909399;
}

.stats {
  display: flex;
  gap: 12px;
}

.stats span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.more-articles {
  text-align: center;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 32px;
  }

  .hero-subtitle {
    font-size: 16px;
  }

  .articles-grid {
    grid-template-columns: 1fr;
  }
}
</style>
