<template>
  <footer class="app-footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-section">
          <h3>个人博客系统</h3>
          <p>基于 Vue 3 + Flask 构建的现代化博客平台</p>
        </div>
        
        <div class="footer-section">
          <h4>快速链接</h4>
          <ul>
            <li><router-link to="/">首页</router-link></li>
            <li><router-link to="/articles">文章列表</router-link></li>
            <li v-if="!authStore.isAuthenticated"><router-link to="/login">登录</router-link></li>
            <li v-if="!authStore.isAuthenticated"><router-link to="/register">注册</router-link></li>
          </ul>
        </div>
        
        <div class="footer-section">
          <h4>技术栈</h4>
          <ul>
            <li>Vue 3 + TypeScript</li>
            <li>Element Plus</li>
            <li>Flask + SQLAlchemy</li>
            <li>JWT 认证</li>
          </ul>
        </div>
        
        <div class="footer-section">
          <h4>联系方式</h4>
          <p>这是一个学习项目</p>
          <p>Python 学习指南 - Stage 6</p>
        </div>
      </div>
      
      <div class="footer-bottom">
        <p>&copy; 2024 个人博客系统. 学习项目，仅供参考.</p>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>

<style scoped>
.app-footer {
  background: #2c3e50;
  color: #ecf0f1;
  margin-top: auto;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 40px;
  padding: 40px 0;
}

.footer-section h3 {
  color: #3498db;
  margin-bottom: 16px;
  font-size: 20px;
}

.footer-section h4 {
  color: #ecf0f1;
  margin-bottom: 12px;
  font-size: 16px;
}

.footer-section p {
  line-height: 1.6;
  color: #bdc3c7;
}

.footer-section ul {
  list-style: none;
  padding: 0;
}

.footer-section ul li {
  margin-bottom: 8px;
}

.footer-section ul li a {
  color: #bdc3c7;
  text-decoration: none;
  transition: color 0.3s;
}

.footer-section ul li a:hover {
  color: #3498db;
}

.footer-bottom {
  border-top: 1px solid #34495e;
  padding: 20px 0;
  text-align: center;
}

.footer-bottom p {
  color: #95a5a6;
  margin: 0;
}

@media (max-width: 768px) {
  .footer-content {
    grid-template-columns: 1fr;
    gap: 24px;
    padding: 24px 0;
  }
  
  .footer-section {
    text-align: center;
  }
}
</style>
