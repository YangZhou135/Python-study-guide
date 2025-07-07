<template>
  <header class="app-header">
    <div class="container">
      <div class="header-content">
        <!-- Logo -->
        <div class="logo">
          <router-link to="/" class="logo-link">
            <h1>个人博客</h1>
          </router-link>
        </div>

        <!-- 导航菜单 -->
        <nav class="nav-menu">
          <el-menu
            mode="horizontal"
            :default-active="activeIndex"
            class="header-menu"
            @select="handleSelect"
          >
            <el-menu-item index="/">首页</el-menu-item>
            <el-menu-item index="/articles">文章</el-menu-item>
            
            <template v-if="authStore.isAuthenticated">
              <el-menu-item index="/articles/create">写文章</el-menu-item>
              <el-menu-item index="/dashboard">控制台</el-menu-item>
            </template>
          </el-menu>
        </nav>

        <!-- 用户操作区 -->
        <div class="user-actions">
          <template v-if="authStore.isAuthenticated">
            <!-- 搜索框 -->
            <el-input
              v-model="searchQuery"
              placeholder="搜索文章..."
              class="search-input"
              @keyup.enter="handleSearch"
            >
              <template #suffix>
                <el-icon class="search-icon" @click="handleSearch">
                  <Search />
                </el-icon>
              </template>
            </el-input>

            <!-- 用户菜单 -->
            <el-dropdown @command="handleUserCommand">
              <span class="user-dropdown">
                <el-avatar :size="32">
                  {{ authStore.user?.username?.charAt(0).toUpperCase() }}
                </el-avatar>
                <span class="username">{{ authStore.user?.username }}</span>
                <el-icon><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">个人资料</el-dropdown-item>
                  <el-dropdown-item command="dashboard">控制台</el-dropdown-item>
                  <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>

          <template v-else>
            <el-button type="primary" @click="$router.push('/login')">
              登录
            </el-button>
            <el-button @click="$router.push('/register')">
              注册
            </el-button>
          </template>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'
import { Search, ArrowDown } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const searchQuery = ref('')

// 当前激活的菜单项
const activeIndex = computed(() => route.path)

// 处理菜单选择
const handleSelect = (index: string) => {
  router.push(index)
}

// 处理搜索
const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({
      name: 'articles',
      query: { search: searchQuery.value.trim() }
    })
  }
}

// 处理用户菜单命令
const handleUserCommand = async (command: string) => {
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'dashboard':
      router.push('/dashboard')
      break
    case 'logout':
      try {
        await authStore.logout()
        ElMessage.success('已退出登录')
        router.push('/')
      } catch (error) {
        ElMessage.error('退出登录失败')
      }
      break
  }
}
</script>

<style scoped>
.app-header {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
}

.logo-link {
  text-decoration: none;
  color: #409eff;
}

.logo h1 {
  font-size: 24px;
  font-weight: 600;
  margin: 0;
}

.nav-menu {
  flex: 1;
  margin: 0 40px;
}

.header-menu {
  border-bottom: none;
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.search-input {
  width: 200px;
}

.search-icon {
  cursor: pointer;
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 8px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.user-dropdown:hover {
  background-color: #f5f7fa;
}

.username {
  font-size: 14px;
  color: #606266;
}

@media (max-width: 768px) {
  .header-content {
    flex-wrap: wrap;
    height: auto;
    padding: 12px 0;
  }
  
  .nav-menu {
    order: 3;
    width: 100%;
    margin: 12px 0 0 0;
  }
  
  .search-input {
    width: 150px;
  }
}
</style>
