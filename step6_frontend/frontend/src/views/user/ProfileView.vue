<template>
  <div class="profile-page">
    <div class="container">
      <div class="profile-header">
        <h1>个人资料</h1>
        <p>管理您的账户信息和偏好设置</p>
      </div>

      <div class="profile-content">
        <el-row :gutter="24">
          <!-- 左侧：个人信息 -->
          <el-col :span="16">
            <div class="profile-card">
              <h2>基本信息</h2>
              
              <el-form
                ref="profileFormRef"
                :model="profileForm"
                :rules="profileRules"
                label-width="100px"
                size="large"
              >
                <el-form-item label="用户名" prop="username">
                  <el-input
                    v-model="profileForm.username"
                    placeholder="请输入用户名"
                    disabled
                  />
                  <div class="form-tip">用户名创建后不可修改</div>
                </el-form-item>

                <el-form-item label="邮箱地址" prop="email">
                  <el-input
                    v-model="profileForm.email"
                    type="email"
                    placeholder="请输入邮箱地址"
                  />
                </el-form-item>

                <el-form-item label="昵称" prop="display_name">
                  <el-input
                    v-model="profileForm.display_name"
                    placeholder="请输入昵称（可选）"
                    maxlength="50"
                    show-word-limit
                  />
                </el-form-item>

                <el-form-item label="个人简介">
                  <el-input
                    v-model="profileForm.bio"
                    type="textarea"
                    :rows="4"
                    placeholder="介绍一下自己吧..."
                    maxlength="200"
                    show-word-limit
                  />
                </el-form-item>

                <el-form-item label="个人网站">
                  <el-input
                    v-model="profileForm.website"
                    placeholder="https://example.com"
                  />
                </el-form-item>

                <el-form-item label="所在地">
                  <el-input
                    v-model="profileForm.location"
                    placeholder="请输入所在地"
                  />
                </el-form-item>

                <el-form-item>
                  <el-button 
                    type="primary" 
                    @click="updateProfile"
                    :loading="profileLoading"
                  >
                    保存更改
                  </el-button>
                  <el-button @click="resetProfile">重置</el-button>
                </el-form-item>
              </el-form>
            </div>

            <!-- 密码修改 -->
            <div class="profile-card">
              <h2>修改密码</h2>
              
              <el-form
                ref="passwordFormRef"
                :model="passwordForm"
                :rules="passwordRules"
                label-width="100px"
                size="large"
              >
                <el-form-item label="当前密码" prop="current_password">
                  <el-input
                    v-model="passwordForm.current_password"
                    type="password"
                    placeholder="请输入当前密码"
                    show-password
                  />
                </el-form-item>

                <el-form-item label="新密码" prop="new_password">
                  <el-input
                    v-model="passwordForm.new_password"
                    type="password"
                    placeholder="请输入新密码"
                    show-password
                  />
                </el-form-item>

                <el-form-item label="确认密码" prop="confirm_password">
                  <el-input
                    v-model="passwordForm.confirm_password"
                    type="password"
                    placeholder="请再次输入新密码"
                    show-password
                  />
                </el-form-item>

                <el-form-item>
                  <el-button 
                    type="primary" 
                    @click="changePassword"
                    :loading="passwordLoading"
                  >
                    修改密码
                  </el-button>
                  <el-button @click="resetPasswordForm">重置</el-button>
                </el-form-item>
              </el-form>
            </div>
          </el-col>

          <!-- 右侧：头像和统计 -->
          <el-col :span="8">
            <!-- 头像上传 -->
            <div class="profile-card">
              <h2>头像</h2>
              
              <div class="avatar-section">
                <div class="avatar-display">
                  <el-avatar 
                    :size="120" 
                    :src="profileForm.avatar"
                    class="user-avatar"
                  >
                    {{ profileForm.username?.charAt(0).toUpperCase() }}
                  </el-avatar>
                </div>
                
                <div class="avatar-actions">
                  <el-upload
                    :action="uploadUrl"
                    :headers="uploadHeaders"
                    :show-file-list="false"
                    :on-success="handleAvatarSuccess"
                    :on-error="handleAvatarError"
                    :before-upload="beforeAvatarUpload"
                    accept="image/*"
                  >
                    <el-button type="primary">上传头像</el-button>
                  </el-upload>
                  
                  <el-button 
                    v-if="profileForm.avatar" 
                    @click="removeAvatar"
                    type="danger"
                    plain
                  >
                    删除头像
                  </el-button>
                </div>
                
                <div class="avatar-tips">
                  <p>支持 JPG、PNG 格式</p>
                  <p>建议尺寸：200x200px</p>
                  <p>文件大小不超过 1MB</p>
                </div>
              </div>
            </div>

            <!-- 账户统计 -->
            <div class="profile-card">
              <h2>账户统计</h2>
              
              <div class="stats-grid">
                <div class="stat-item">
                  <div class="stat-number">{{ userStats.article_count }}</div>
                  <div class="stat-label">发表文章</div>
                </div>
                
                <div class="stat-item">
                  <div class="stat-number">{{ userStats.total_views }}</div>
                  <div class="stat-label">总阅读量</div>
                </div>
                
                <div class="stat-item">
                  <div class="stat-number">{{ userStats.total_likes }}</div>
                  <div class="stat-label">获得点赞</div>
                </div>
                
                <div class="stat-item">
                  <div class="stat-number">{{ userStats.comment_count }}</div>
                  <div class="stat-label">发表评论</div>
                </div>
              </div>
            </div>

            <!-- 账户信息 -->
            <div class="profile-card">
              <h2>账户信息</h2>
              
              <div class="account-info">
                <div class="info-item">
                  <span class="info-label">注册时间：</span>
                  <span class="info-value">{{ formatDate(userInfo.created_at) }}</span>
                </div>
                
                <div class="info-item">
                  <span class="info-label">最后登录：</span>
                  <span class="info-value">{{ formatDate(userInfo.last_login) }}</span>
                </div>
                
                <div class="info-item">
                  <span class="info-label">账户状态：</span>
                  <el-tag :type="userInfo.is_active ? 'success' : 'danger'">
                    {{ userInfo.is_active ? '正常' : '已禁用' }}
                  </el-tag>
                </div>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { AuthAPI } from '@/api/auth'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'

const authStore = useAuthStore()

// 表单引用
const profileFormRef = ref<FormInstance>()
const passwordFormRef = ref<FormInstance>()

// 加载状态
const profileLoading = ref(false)
const passwordLoading = ref(false)

// 用户信息
const userInfo = computed(() => authStore.user || {})
const userStats = ref({
  article_count: 0,
  total_views: 0,
  total_likes: 0,
  comment_count: 0
})

// 个人资料表单
const profileForm = reactive({
  username: '',
  email: '',
  display_name: '',
  bio: '',
  website: '',
  location: '',
  avatar: ''
})

// 密码修改表单
const passwordForm = reactive({
  current_password: '',
  new_password: '',
  confirm_password: ''
})

// 上传配置
const uploadUrl = computed(() => `${import.meta.env.VITE_API_BASE_URL}/api/upload/avatar`)
const uploadHeaders = computed(() => ({
  'Authorization': `Bearer ${authStore.accessToken}`
}))

// 表单验证规则
const profileRules: FormRules = {
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ]
}

const passwordRules: FormRules = {
  current_password: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于 6 个字符', trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.new_password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 生命周期
onMounted(() => {
  loadUserProfile()
  loadUserStats()
})

// 方法
const loadUserProfile = () => {
  const user = authStore.user
  if (user) {
    Object.assign(profileForm, {
      username: user.username,
      email: user.email,
      display_name: user.display_name || '',
      bio: user.bio || '',
      website: user.website || '',
      location: user.location || '',
      avatar: user.avatar || ''
    })
  }
}

const loadUserStats = async () => {
  try {
    // TODO: 实现用户统计数据加载
    userStats.value = {
      article_count: 12,
      total_views: 1580,
      total_likes: 89,
      comment_count: 45
    }
  } catch (error) {
    console.error('加载用户统计失败:', error)
  }
}

const updateProfile = async () => {
  if (!profileFormRef.value) return

  try {
    await profileFormRef.value.validate()
    profileLoading.value = true

    const updateData = {
      email: profileForm.email,
      display_name: profileForm.display_name,
      bio: profileForm.bio,
      website: profileForm.website,
      location: profileForm.location,
      avatar: profileForm.avatar
    }

    await AuthAPI.updateProfile(updateData)
    await authStore.fetchUserInfo()
    
    ElMessage.success('个人资料更新成功')
  } catch (error: any) {
    if (error.response?.data?.error?.message) {
      ElMessage.error(error.response.data.error.message)
    } else {
      ElMessage.error('更新个人资料失败')
    }
  } finally {
    profileLoading.value = false
  }
}

const resetProfile = () => {
  loadUserProfile()
}

const changePassword = async () => {
  if (!passwordFormRef.value) return

  try {
    await passwordFormRef.value.validate()
    passwordLoading.value = true

    await AuthAPI.changePassword({
      current_password: passwordForm.current_password,
      new_password: passwordForm.new_password
    })

    ElMessage.success('密码修改成功')
    resetPasswordForm()
  } catch (error: any) {
    if (error.response?.data?.error?.message) {
      ElMessage.error(error.response.data.error.message)
    } else {
      ElMessage.error('密码修改失败')
    }
  } finally {
    passwordLoading.value = false
  }
}

const resetPasswordForm = () => {
  Object.assign(passwordForm, {
    current_password: '',
    new_password: '',
    confirm_password: ''
  })
  passwordFormRef.value?.clearValidate()
}

const beforeAvatarUpload = (file: File) => {
  const isImage = file.type.startsWith('image/')
  const isLt1M = file.size / 1024 / 1024 < 1

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt1M) {
    ElMessage.error('图片大小不能超过 1MB!')
    return false
  }
  return true
}

const handleAvatarSuccess = (response: any) => {
  if (response.success) {
    profileForm.avatar = response.data.url
    ElMessage.success('头像上传成功')
  } else {
    ElMessage.error('头像上传失败')
  }
}

const handleAvatarError = () => {
  ElMessage.error('头像上传失败，请重试')
}

const removeAvatar = () => {
  profileForm.avatar = ''
}

const formatDate = (dateString: string) => {
  if (!dateString) return '未知'
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.profile-header {
  text-align: center;
  margin-bottom: 32px;
  padding: 32px 0;
}

.profile-header h1 {
  font-size: 32px;
  color: #303133;
  margin-bottom: 8px;
}

.profile-header p {
  color: #606266;
  font-size: 16px;
}

.profile-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.profile-card h2 {
  color: #303133;
  margin-bottom: 20px;
  font-size: 18px;
  font-weight: 600;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.avatar-section {
  text-align: center;
}

.avatar-display {
  margin-bottom: 16px;
}

.user-avatar {
  border: 3px solid #f0f0f0;
}

.avatar-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.avatar-tips {
  font-size: 12px;
  color: #909399;
}

.avatar-tips p {
  margin: 2px 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.stat-item {
  text-align: center;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.stat-number {
  font-size: 24px;
  font-weight: 600;
  color: #409eff;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: #909399;
}

.account-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  color: #606266;
  font-size: 14px;
}

.info-value {
  color: #303133;
  font-size: 14px;
  font-weight: 500;
}

@media (max-width: 768px) {
  .profile-content :deep(.el-col) {
    width: 100% !important;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .profile-card {
    padding: 16px;
  }
}
</style>
