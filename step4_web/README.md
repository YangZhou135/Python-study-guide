# Stage 4: Web开发基础 - Flask博客系统

## 🎯 学习目标

在这个阶段，您将学习：

1. **Flask框架基础**
   - 路由和视图函数
   - 模板系统 (Jinja2)
   - 请求处理和响应

2. **Web表单处理**
   - Flask-WTF表单
   - 数据验证
   - CSRF保护

3. **用户认证系统**
   - 用户注册和登录
   - 会话管理
   - 密码安全

4. **文件上传处理**
   - 图片上传
   - 文件验证
   - 安全存储

5. **前端集成**
   - Bootstrap样式框架
   - JavaScript交互
   - 响应式设计

## 📁 项目结构

```
step4_web/
├── app.py              # Flask应用主文件
├── config.py           # 配置文件
├── models.py           # 数据模型 (扩展自Step3)
├── forms.py            # Web表单定义
├── requirements.txt    # 依赖包列表
├── run.py             # 启动脚本
├── init_demo_data.py  # 演示数据初始化
├── templates/         # HTML模板
│   ├── base.html      # 基础模板
│   ├── index.html     # 首页
│   ├── login.html     # 登录页
│   ├── register.html  # 注册页
│   ├── article_detail.html  # 文章详情
│   ├── article_form.html    # 文章编辑
│   ├── search.html    # 搜索页面
│   ├── profile.html   # 个人中心
│   ├── my_articles.html     # 我的文章
│   └── errors/        # 错误页面
│       ├── 404.html
│       └── 500.html
├── static/            # 静态文件
│   ├── css/
│   │   └── style.css  # 自定义样式
│   ├── js/
│   │   └── main.js    # JavaScript功能
│   └── uploads/       # 上传文件目录
└── data/              # 数据存储目录
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境 (推荐)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装依赖包
pip install -r requirements.txt
```

### 2. 初始化演示数据

```bash
python init_demo_data.py
```

### 3. 启动应用

```bash
# 使用启动脚本 (推荐)
python run.py --init-data --debug

# 或直接运行
python -c "from app import create_app; create_app().run(debug=True)"
```

### 4. 访问应用

打开浏览器访问: http://localhost:5000

## 🔑 演示账户

| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin | admin123 | 管理员 |
| demo | demo123 | 演示用户 |
| 张三 | password123 | 普通用户 |
| 李四 | password123 | 普通用户 |
| 王五 | password123 | 普通用户 |

## ✨ 主要功能

### 用户功能
- ✅ 用户注册和登录
- ✅ 个人资料管理
- ✅ 密码修改
- ✅ 会话管理

### 文章功能
- ✅ 文章发布和编辑
- ✅ Markdown支持
- ✅ 图片上传
- ✅ 草稿保存
- ✅ 标签管理
- ✅ 文章搜索

### 交互功能
- ✅ 文章评论
- ✅ 点赞功能
- ✅ 浏览统计
- ✅ 分享功能

### 界面功能
- ✅ 响应式设计
- ✅ 现代化UI
- ✅ 暗色主题支持
- ✅ 移动端适配

## 🛠️ 技术栈

### 后端
- **Flask 2.3+**: Web框架
- **Flask-WTF**: 表单处理
- **Jinja2**: 模板引擎
- **Werkzeug**: WSGI工具库

### 前端
- **Bootstrap 5**: CSS框架
- **Font Awesome**: 图标库
- **JavaScript ES6+**: 交互功能
- **CSS3**: 自定义样式

### 安全
- **PBKDF2**: 密码哈希
- **CSRF保护**: 跨站请求伪造防护
- **会话安全**: 安全的会话管理
- **文件验证**: 上传文件安全检查

## 📚 核心概念学习

### 1. Flask路由系统

```python
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/article/<int:article_id>')
def article_detail(article_id):
    article = blog_manager.get_article(article_id)
    return render_template('article_detail.html', article=article)
```

### 2. 模板继承

```html
<!-- base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>

<!-- index.html -->
{% extends "base.html" %}
{% block title %}首页{% endblock %}
{% block content %}
    <h1>欢迎来到博客系统</h1>
{% endblock %}
```

### 3. 表单处理

```python
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class ArticleForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired()])
    content = TextAreaField('内容', validators=[DataRequired()])
```

### 4. 用户认证

```python
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not get_current_user():
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
```

## 🔧 配置说明

### 环境配置

```python
# config.py
class Config:
    SECRET_KEY = 'your-secret-key'
    DATA_DIR = 'data'
    UPLOAD_DIR = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
```

### 启动选项

```bash
# 开发模式
python run.py --env development --debug

# 生产模式
python run.py --env production --host 0.0.0.0 --port 80

# 初始化数据
python run.py --init-data
```

## 🧪 测试功能

### 手动测试清单

- [ ] 用户注册和登录
- [ ] 文章创建和编辑
- [ ] 图片上传
- [ ] 评论功能
- [ ] 搜索功能
- [ ] 响应式设计
- [ ] 错误处理

## 🎯 下一步

完成Stage 4后，您将掌握：
- Flask Web开发基础
- 用户认证和会话管理
- 表单处理和验证
- 模板系统和前端集成
- 文件上传和安全处理

准备好进入 **Stage 5: 数据库操作** 了吗？
