<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-card">
        <div class="auth-header">
          <h1>注册</h1>
          <p>创建您的账户，开始写作之旅</p>
        </div>

        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          label-width="0"
          size="large"
          @submit.prevent="handleSubmit"
        >
          <el-form-item prop="username">
            <el-input
              v-model="form.username"
              placeholder="用户名"
              prefix-icon="User"
              clearable
              @blur="checkUsername"
            />
          </el-form-item>

          <el-form-item prop="email">
            <el-input
              v-model="form.email"
              type="email"
              placeholder="邮箱地址"
              prefix-icon="Message"
              clearable
              @blur="checkEmail"
            />
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="密码"
              prefix-icon="Lock"
              show-password
              clearable
            />
          </el-form-item>

          <el-form-item prop="confirmPassword">
            <el-input
              v-model="form.confirmPassword"
              type="password"
              placeholder="确认密码"
              prefix-icon="Lock"
              show-password
              clearable
              @keyup.enter="handleSubmit"
            />
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              :loading="loading"
              style="width: 100%"
              @click="handleSubmit"
            >
              {{ loading ? '注册中...' : '注册' }}
            </el-button>
          </el-form-item>
        </el-form>

        <div class="auth-footer">
          <p>
            已有账户？
            <router-link to="/login" class="auth-link">
              立即登录
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { AuthAPI } from '@/api/auth'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'

const router = useRouter()
const authStore = useAuthStore()

const formRef = ref<FormInstance>()
const loading = ref(false)

const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

// 自定义验证规则
const validateUsername = async (rule: any, value: string, callback: any) => {
  if (!value) {
    callback(new Error('请输入用户名'))
    return
  }
  if (value.length < 3 || value.length > 20) {
    callback(new Error('用户名长度在 3 到 20 个字符'))
    return
  }
  if (!/^[a-zA-Z0-9_]+$/.test(value)) {
    callback(new Error('用户名只能包含字母、数字和下划线'))
    return
  }
  callback()
}

const validateEmail = (rule: any, value: string, callback: any) => {
  if (!value) {
    callback(new Error('请输入邮箱地址'))
    return
  }
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(value)) {
    callback(new Error('请输入有效的邮箱地址'))
    return
  }
  callback()
}

const validatePassword = (rule: any, value: string, callback: any) => {
  if (!value) {
    callback(new Error('请输入密码'))
    return
  }
  if (value.length < 6) {
    callback(new Error('密码长度不能少于 6 个字符'))
    return
  }
  callback()
}

const validateConfirmPassword = (rule: any, value: string, callback: any) => {
  if (!value) {
    callback(new Error('请确认密码'))
    return
  }
  if (value !== form.password) {
    callback(new Error('两次输入的密码不一致'))
    return
  }
  callback()
}

const rules: FormRules = {
  username: [{ validator: validateUsername, trigger: 'blur' }],
  email: [{ validator: validateEmail, trigger: 'blur' }],
  password: [{ validator: validatePassword, trigger: 'blur' }],
  confirmPassword: [{ validator: validateConfirmPassword, trigger: 'blur' }]
}

// 检查用户名是否可用
const checkUsername = async () => {
  if (form.username && form.username.length >= 3) {
    try {
      const result = await AuthAPI.checkUsername(form.username)
      if (!result.available) {
        ElMessage.warning('用户名已被使用')
      }
    } catch (error) {
      // 忽略检查错误
    }
  }
}

// 检查邮箱是否可用
const checkEmail = async () => {
  if (form.email && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    try {
      const result = await AuthAPI.checkEmail(form.email)
      if (!result.available) {
        ElMessage.warning('邮箱已被使用')
      }
    } catch (error) {
      // 忽略检查错误
    }
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    loading.value = true

    await authStore.register({
      username: form.username,
      email: form.email,
      password: form.password,
      confirm_password: form.confirmPassword
    })

    ElMessage.success('注册成功，欢迎加入！')
    router.push('/')
  } catch (error: any) {
    if (error.response?.data?.error?.message) {
      ElMessage.error(error.response.data.error.message)
    } else if (typeof error === 'string') {
      ElMessage.error(error)
    } else {
      ElMessage.error('注册失败，请稍后重试')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.auth-container {
  width: 100%;
  max-width: 400px;
}

.auth-card {
  background: white;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.auth-header {
  text-align: center;
  margin-bottom: 32px;
}

.auth-header h1 {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 8px;
}

.auth-header p {
  color: #606266;
  font-size: 14px;
}

.auth-footer {
  text-align: center;
  margin-top: 24px;
}

.auth-footer p {
  color: #606266;
  font-size: 14px;
}

.auth-link {
  color: #409eff;
  text-decoration: none;
  font-weight: 500;
}

.auth-link:hover {
  text-decoration: underline;
}

@media (max-width: 480px) {
  .auth-card {
    padding: 24px;
  }
  
  .auth-header h1 {
    font-size: 24px;
  }
}
</style>
