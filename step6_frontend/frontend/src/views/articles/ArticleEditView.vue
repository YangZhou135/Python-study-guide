<template>
  <div class="article-edit-page">
    <div class="container">
      <div class="page-header">
        <h1>编辑文章</h1>
        <div class="header-actions">
          <el-button @click="goBack">取消</el-button>
          <el-button @click="saveDraft" :loading="draftLoading">
            保存草稿
          </el-button>
          <el-button type="primary" @click="updateArticle" :loading="updateLoading">
            更新文章
          </el-button>
        </div>
      </div>

      <div v-loading="loading" class="article-form">
        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          label-width="100px"
          size="large"
        >
          <!-- 文章标题 -->
          <el-form-item label="文章标题" prop="title">
            <el-input
              v-model="form.title"
              placeholder="请输入文章标题"
              maxlength="100"
              show-word-limit
              clearable
            />
          </el-form-item>

          <!-- 文章摘要 -->
          <el-form-item label="文章摘要" prop="summary">
            <el-input
              v-model="form.summary"
              type="textarea"
              :rows="3"
              placeholder="请输入文章摘要（可选）"
              maxlength="200"
              show-word-limit
            />
          </el-form-item>

          <!-- 封面图片 -->
          <el-form-item label="封面图片">
            <div class="image-upload">
              <el-upload
                class="cover-uploader"
                :action="uploadUrl"
                :headers="uploadHeaders"
                :show-file-list="false"
                :on-success="handleImageSuccess"
                :on-error="handleImageError"
                :before-upload="beforeImageUpload"
                accept="image/*"
              >
                <img v-if="form.featured_image" :src="form.featured_image" class="cover-image" />
                <div v-else class="upload-placeholder">
                  <el-icon class="upload-icon"><Plus /></el-icon>
                  <div class="upload-text">点击上传封面</div>
                </div>
              </el-upload>
              <div class="upload-tips">
                <p>建议尺寸：16:9，支持 JPG、PNG 格式，文件大小不超过 2MB</p>
                <el-button v-if="form.featured_image" text type="danger" @click="removeCover">
                  删除封面
                </el-button>
              </div>
            </div>
          </el-form-item>

          <!-- 文章标签 -->
          <el-form-item label="文章标签">
            <el-select
              v-model="form.tags"
              multiple
              filterable
              allow-create
              placeholder="选择或创建标签"
              style="width: 100%"
            >
              <el-option
                v-for="tag in availableTags"
                :key="tag.id"
                :label="tag.name"
                :value="tag.name"
              />
            </el-select>
          </el-form-item>

          <!-- 文章内容 -->
          <el-form-item label="文章内容" prop="content">
            <div class="editor-container">
              <div class="editor-toolbar">
                <el-button-group>
                  <el-button @click="insertMarkdown('**', '**')" title="加粗">
                    <strong>B</strong>
                  </el-button>
                  <el-button @click="insertMarkdown('*', '*')" title="斜体">
                    <em>I</em>
                  </el-button>
                  <el-button @click="insertMarkdown('`', '`')" title="代码">
                    Code
                  </el-button>
                  <el-button @click="insertMarkdown('### ', '')" title="标题">
                    H3
                  </el-button>
                  <el-button @click="insertMarkdown('- ', '')" title="列表">
                    List
                  </el-button>
                  <el-button @click="insertMarkdown('[链接文字](', ')')" title="链接">
                    Link
                  </el-button>
                </el-button-group>
                
                <el-upload
                  :action="uploadUrl"
                  :headers="uploadHeaders"
                  :show-file-list="false"
                  :on-success="handleContentImageSuccess"
                  :before-upload="beforeImageUpload"
                  accept="image/*"
                >
                  <el-button>
                    <el-icon><Picture /></el-icon>
                    插入图片
                  </el-button>
                </el-upload>
              </div>
              
              <div class="editor-content">
                <div class="editor-pane">
                  <el-input
                    v-model="form.content"
                    type="textarea"
                    placeholder="请输入文章内容，支持 Markdown 语法"
                    :rows="20"
                    resize="none"
                    class="content-editor"
                  />
                </div>
                
                <div class="preview-pane">
                  <div class="preview-header">预览</div>
                  <div class="preview-content" v-html="previewContent"></div>
                </div>
              </div>
            </div>
          </el-form-item>

          <!-- 发布设置 -->
          <el-form-item label="发布设置">
            <div class="publish-settings">
              <el-checkbox v-model="form.is_published">
                发布文章
              </el-checkbox>
              <el-checkbox v-model="form.allow_comments">
                允许评论
              </el-checkbox>
            </div>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useArticlesStore } from '@/stores/articles'
import { useAuthStore } from '@/stores/auth'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { Plus, Picture } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const articlesStore = useArticlesStore()
const authStore = useAuthStore()

// 表单引用
const formRef = ref<FormInstance>()

// 加载状态
const loading = ref(false)
const draftLoading = ref(false)
const updateLoading = ref(false)

// 文章ID
const articleId = computed(() => Number(route.params.id))

// 表单数据
const form = reactive({
  title: '',
  summary: '',
  content: '',
  featured_image: '',
  tags: [] as string[],
  is_published: true,
  allow_comments: true
})

// 可用标签
const availableTags = ref([
  { id: 1, name: '技术' },
  { id: 2, name: '生活' },
  { id: 3, name: '学习' },
  { id: 4, name: 'Vue.js' },
  { id: 5, name: 'Python' },
  { id: 6, name: '前端' },
  { id: 7, name: '后端' }
])

// 上传配置
const uploadUrl = computed(() => `${import.meta.env.VITE_API_BASE_URL}/api/upload`)
const uploadHeaders = computed(() => ({
  'Authorization': `Bearer ${authStore.accessToken}`
}))

// 表单验证规则
const rules: FormRules = {
  title: [
    { required: true, message: '请输入文章标题', trigger: 'blur' },
    { min: 5, max: 100, message: '标题长度在 5 到 100 个字符', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入文章内容', trigger: 'blur' },
    { min: 50, message: '文章内容不能少于 50 个字符', trigger: 'blur' }
  ]
}

// 预览内容
const previewContent = computed(() => {
  if (!form.content) return '<p class="empty-preview">在左侧编辑器中输入内容，这里将显示预览效果</p>'
  
  // 简单的 Markdown 转 HTML
  return form.content
    .replace(/\n/g, '<br>')
    .replace(/### (.*?)(<br>|$)/g, '<h3>$1</h3>')
    .replace(/## (.*?)(<br>|$)/g, '<h2>$1</h2>')
    .replace(/# (.*?)(<br>|$)/g, '<h1>$1</h1>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, '<code>$1</code>')
    .replace(/- (.*?)(<br>|$)/g, '<li>$1</li>')
    .replace(/(<li>.*<\/li>)/g, '<ul>$1</ul>')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>')
})

// 生命周期
onMounted(async () => {
  // 检查用户权限
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }

  await loadArticle()
})

// 方法
const loadArticle = async () => {
  loading.value = true
  try {
    await articlesStore.fetchArticle(articleId.value)
    const article = articlesStore.currentArticle
    
    if (!article) {
      ElMessage.error('文章不存在')
      router.push('/articles')
      return
    }

    // 检查编辑权限
    if (article.author.id !== authStore.user?.id) {
      ElMessage.error('您没有权限编辑此文章')
      router.push(`/articles/${articleId.value}`)
      return
    }

    // 填充表单数据
    Object.assign(form, {
      title: article.title,
      summary: article.summary || '',
      content: article.content,
      featured_image: article.featured_image || '',
      tags: article.tags?.map(tag => tag.name) || [],
      is_published: article.is_published,
      allow_comments: article.allow_comments
    })
  } catch (error) {
    ElMessage.error('加载文章失败')
    router.push('/articles')
  } finally {
    loading.value = false
  }
}

const insertMarkdown = (before: string, after: string) => {
  const textarea = document.querySelector('.content-editor textarea') as HTMLTextAreaElement
  if (!textarea) return

  const start = textarea.selectionStart
  const end = textarea.selectionEnd
  const selectedText = form.content.substring(start, end)
  
  const newText = before + selectedText + after
  form.content = form.content.substring(0, start) + newText + form.content.substring(end)
  
  // 重新设置光标位置
  setTimeout(() => {
    textarea.focus()
    textarea.setSelectionRange(start + before.length, start + before.length + selectedText.length)
  }, 0)
}

const beforeImageUpload = (file: File) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB!')
    return false
  }
  return true
}

const handleImageSuccess = (response: any) => {
  if (response.success) {
    form.featured_image = response.data.url
    ElMessage.success('封面上传成功')
  } else {
    ElMessage.error('封面上传失败')
  }
}

const handleContentImageSuccess = (response: any) => {
  if (response.success) {
    const imageMarkdown = `![图片](${response.data.url})`
    insertMarkdown(imageMarkdown, '')
    ElMessage.success('图片上传成功')
  } else {
    ElMessage.error('图片上传失败')
  }
}

const handleImageError = () => {
  ElMessage.error('图片上传失败，请重试')
}

const removeCover = () => {
  form.featured_image = ''
}

const saveDraft = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate(['title', 'content'])
    draftLoading.value = true

    const articleData = {
      ...form,
      is_published: false
    }

    await articlesStore.updateArticle(articleId.value, articleData)
    ElMessage.success('草稿保存成功')
  } catch (error) {
    if (typeof error === 'string') {
      ElMessage.error(error)
    } else {
      ElMessage.error('保存草稿失败')
    }
  } finally {
    draftLoading.value = false
  }
}

const updateArticle = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    updateLoading.value = true

    await articlesStore.updateArticle(articleId.value, form)
    ElMessage.success('文章更新成功')
    router.push(`/articles/${articleId.value}`)
  } catch (error) {
    if (typeof error === 'string') {
      ElMessage.error(error)
    } else {
      ElMessage.error('更新文章失败')
    }
  } finally {
    updateLoading.value = false
  }
}

const goBack = async () => {
  // 检查是否有未保存的更改
  const article = articlesStore.currentArticle
  if (article) {
    const hasChanges = 
      form.title !== article.title ||
      form.summary !== (article.summary || '') ||
      form.content !== article.content ||
      form.featured_image !== (article.featured_image || '') ||
      JSON.stringify(form.tags) !== JSON.stringify(article.tags?.map(tag => tag.name) || []) ||
      form.is_published !== article.is_published ||
      form.allow_comments !== article.allow_comments

    if (hasChanges) {
      try {
        await ElMessageBox.confirm(
          '您有未保存的更改，确定要离开吗？',
          '确认离开',
          {
            confirmButtonText: '离开',
            cancelButtonText: '取消',
            type: 'warning',
          }
        )
      } catch {
        return // 用户取消
      }
    }
  }

  router.push(`/articles/${articleId.value}`)
}
</script>

<style scoped>
/* 样式与 ArticleCreateView 相同 */
.article-edit-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 24px 0;
}

.page-header h1 {
  color: #303133;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.article-form {
  background: white;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.image-upload {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.cover-uploader {
  display: inline-block;
}

.cover-image {
  width: 200px;
  height: 112px;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid #dcdfe6;
}

.upload-placeholder {
  width: 200px;
  height: 112px;
  border: 2px dashed #dcdfe6;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: border-color 0.3s;
}

.upload-placeholder:hover {
  border-color: #409eff;
}

.upload-icon {
  font-size: 24px;
  color: #8c939d;
  margin-bottom: 8px;
}

.upload-text {
  color: #8c939d;
  font-size: 14px;
}

.upload-tips {
  font-size: 12px;
  color: #909399;
}

.editor-container {
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  overflow: hidden;
}

.editor-toolbar {
  background: #f5f7fa;
  padding: 12px;
  border-bottom: 1px solid #dcdfe6;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.editor-content {
  display: flex;
  height: 500px;
}

.editor-pane,
.preview-pane {
  flex: 1;
}

.editor-pane {
  border-right: 1px solid #dcdfe6;
}

.content-editor {
  height: 100%;
}

.content-editor :deep(.el-textarea__inner) {
  border: none;
  border-radius: 0;
  resize: none;
  height: 100% !important;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 14px;
  line-height: 1.6;
}

.preview-header {
  background: #f8f9fa;
  padding: 12px 16px;
  border-bottom: 1px solid #ebeef5;
  font-weight: 500;
  color: #606266;
}

.preview-content {
  padding: 16px;
  height: calc(100% - 45px);
  overflow-y: auto;
  font-size: 14px;
  line-height: 1.8;
}

.preview-content :deep(h1),
.preview-content :deep(h2),
.preview-content :deep(h3) {
  margin: 16px 0 8px 0;
  color: #303133;
}

.preview-content :deep(p) {
  margin: 8px 0;
}

.preview-content :deep(code) {
  background: #f1f2f3;
  padding: 2px 4px;
  border-radius: 3px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
}

.preview-content :deep(ul) {
  margin: 8px 0;
  padding-left: 20px;
}

.preview-content :deep(li) {
  margin: 4px 0;
}

.preview-content :deep(a) {
  color: #409eff;
  text-decoration: none;
}

.preview-content :deep(a:hover) {
  text-decoration: underline;
}

.empty-preview {
  color: #909399;
  font-style: italic;
  text-align: center;
  margin-top: 50px;
}

.publish-settings {
  display: flex;
  gap: 24px;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .article-form {
    padding: 20px;
  }
  
  .editor-content {
    flex-direction: column;
    height: auto;
  }
  
  .editor-pane {
    border-right: none;
    border-bottom: 1px solid #dcdfe6;
  }
  
  .content-editor {
    height: 300px;
  }
  
  .preview-content {
    height: 300px;
  }
}
</style>
