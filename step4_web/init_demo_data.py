#!/usr/bin/env python3
"""
演示数据初始化脚本
创建示例用户和文章数据，用于测试Web应用功能
"""

import os
import sys
from datetime import datetime, timedelta
from models import WebUser, WebArticle, Comment, WebBlogManager

def create_demo_users(blog_manager):
    """创建演示用户"""
    print("创建演示用户...")
    
    # 创建管理员用户
    admin = blog_manager.register_user("admin", "admin@example.com", "admin123")
    if admin:
        print(f"✅ 创建管理员用户: {admin.username}")
    else:
        print("❌ 管理员用户创建失败")

    # 创建普通用户
    users_data = [
        ("张三", "zhangsan@example.com", "password123"),
        ("李四", "lisi@example.com", "password123"),
        ("王五", "wangwu@example.com", "password123"),
        ("demo", "demo@example.com", "demo123"),  # 演示账户
    ]

    for username, email, password in users_data:
        user = blog_manager.register_user(username, email, password)
        if user:
            print(f"✅ 创建用户: {username}")
        else:
            print(f"❌ 用户 {username} 创建失败")
    
    return blog_manager.users

def create_demo_articles(blog_manager, users):
    """创建演示文章"""
    print("\n创建演示文章...")
    
    articles_data = [
        {
            "title": "Python Web开发入门指南",
            "content": """# Python Web开发入门指南

欢迎来到Python Web开发的世界！本文将为您介绍Python Web开发的基础知识。

## 什么是Web开发？

Web开发是创建网站和Web应用程序的过程。它包括：

- **前端开发**：用户界面和用户体验
- **后端开发**：服务器逻辑和数据处理
- **数据库**：数据存储和管理

## Python Web框架

Python有许多优秀的Web框架：

### Flask
- 轻量级微框架
- 灵活性高
- 适合小到中型项目

### Django
- 全功能框架
- 内置管理后台
- 适合大型项目

## 开始您的第一个Flask应用

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
```

这就是一个最简单的Flask应用！

## 总结

Python Web开发是一个充满可能性的领域。通过学习Flask或Django，您可以创建功能强大的Web应用程序。

祝您学习愉快！""",
            "summary": "本文介绍了Python Web开发的基础知识，包括常用框架Flask和Django的特点，以及如何创建第一个Flask应用。",
            "tags": ["Python", "Web开发", "Flask", "Django", "入门教程"],
            "author": "admin",
            "is_published": True
        },
        {
            "title": "Flask模板系统详解",
            "content": """# Flask模板系统详解

Flask使用Jinja2作为模板引擎，提供了强大的模板功能。

## 模板基础

### 变量输出
```html
<h1>{{ title }}</h1>
<p>作者：{{ author }}</p>
```

### 控制结构
```html
{% if user %}
    <p>欢迎，{{ user.username }}！</p>
{% else %}
    <p>请登录</p>
{% endif %}
```

### 循环
```html
<ul>
{% for item in items %}
    <li>{{ item }}</li>
{% endfor %}
</ul>
```

## 模板继承

### 基础模板 (base.html)
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```

### 子模板
```html
{% extends "base.html" %}

{% block title %}首页{% endblock %}

{% block content %}
    <h1>欢迎来到我的网站</h1>
{% endblock %}
```

## 过滤器

Jinja2提供了许多有用的过滤器：

```html
{{ name|upper }}  <!-- 转换为大写 -->
{{ date|strftime('%Y-%m-%d') }}  <!-- 格式化日期 -->
{{ content|truncate(100) }}  <!-- 截断文本 -->
```

## 总结

掌握Flask模板系统是Web开发的重要技能。通过模板继承和过滤器，您可以创建灵活且可维护的Web界面。""",
            "summary": "详细介绍Flask的Jinja2模板系统，包括变量输出、控制结构、模板继承和过滤器的使用方法。",
            "tags": ["Flask", "Jinja2", "模板", "Web开发"],
            "author": "张三",
            "is_published": True
        },
        {
            "title": "数据库设计最佳实践",
            "content": """# 数据库设计最佳实践

良好的数据库设计是应用程序成功的基础。

## 设计原则

### 1. 规范化
- 第一范式（1NF）：原子性
- 第二范式（2NF）：完全函数依赖
- 第三范式（3NF）：消除传递依赖

### 2. 命名规范
- 表名使用复数形式
- 字段名清晰明确
- 使用一致的命名约定

### 3. 数据类型选择
- 选择合适的数据类型
- 考虑存储空间和性能
- 使用约束确保数据完整性

## 索引策略

### 主键索引
每个表都应该有主键，通常使用自增ID。

### 外键索引
外键字段应该创建索引以提高查询性能。

### 复合索引
对于多字段查询，考虑创建复合索引。

## 性能优化

### 查询优化
- 避免SELECT *
- 使用适当的WHERE条件
- 考虑查询执行计划

### 表结构优化
- 合理的字段长度
- 适当的数据类型
- 避免过度规范化

## 安全考虑

### 数据验证
- 输入验证
- 数据类型检查
- 长度限制

### 访问控制
- 用户权限管理
- 数据加密
- 审计日志

## 总结

数据库设计需要平衡规范化、性能和可维护性。遵循最佳实践可以创建高效、安全的数据库系统。""",
            "summary": "介绍数据库设计的最佳实践，包括规范化原则、命名规范、索引策略、性能优化和安全考虑。",
            "tags": ["数据库", "设计", "性能优化", "安全"],
            "author": "李四",
            "is_published": True
        },
        {
            "title": "前端开发趋势2024",
            "content": """# 前端开发趋势2024

前端技术发展迅速，让我们看看2024年的主要趋势。

## 框架和库

### React 18+
- 并发特性
- Suspense改进
- 自动批处理

### Vue 3
- Composition API
- 更好的TypeScript支持
- 性能提升

### Svelte/SvelteKit
- 编译时优化
- 更小的包体积
- 简洁的语法

## 开发工具

### Vite
- 快速的开发服务器
- 优化的构建过程
- 插件生态系统

### TypeScript
- 类型安全
- 更好的IDE支持
- 逐步采用

## CSS发展

### CSS-in-JS
- Styled Components
- Emotion
- 运行时vs编译时

### CSS框架
- Tailwind CSS持续流行
- 原子化CSS
- 设计系统

## 性能优化

### Core Web Vitals
- LCP (Largest Contentful Paint)
- FID (First Input Delay)
- CLS (Cumulative Layout Shift)

### 代码分割
- 动态导入
- 路由级分割
- 组件级分割

## 新兴技术

### WebAssembly
- 高性能计算
- 跨语言支持
- 浏览器原生支持

### PWA
- 离线功能
- 推送通知
- 应用级体验

## 总结

前端开发继续快速发展。保持学习和适应新技术是前端开发者的必备技能。""",
            "summary": "分析2024年前端开发的主要趋势，包括新框架、开发工具、CSS发展、性能优化和新兴技术。",
            "tags": ["前端", "React", "Vue", "性能优化", "趋势"],
            "author": "王五",
            "is_published": True
        },
        {
            "title": "API设计指南",
            "content": """# RESTful API设计指南

设计良好的API是现代应用程序的核心。

## REST原则

### 1. 统一接口
- 使用标准HTTP方法
- 资源标识符（URI）
- 表现层状态转换

### 2. 无状态
- 每个请求包含所有必要信息
- 服务器不保存客户端状态
- 提高可扩展性

### 3. 可缓存
- 响应应该明确是否可缓存
- 提高性能和可扩展性

## HTTP方法

### GET
- 获取资源
- 幂等操作
- 可缓存

### POST
- 创建资源
- 非幂等操作
- 不可缓存

### PUT
- 更新资源
- 幂等操作
- 完整替换

### DELETE
- 删除资源
- 幂等操作

## URL设计

### 资源命名
```
GET /api/users          # 获取用户列表
GET /api/users/123      # 获取特定用户
POST /api/users         # 创建用户
PUT /api/users/123      # 更新用户
DELETE /api/users/123   # 删除用户
```

### 嵌套资源
```
GET /api/users/123/posts     # 获取用户的文章
POST /api/users/123/posts    # 为用户创建文章
```

## 响应格式

### 成功响应
```json
{
  "status": "success",
  "data": {
    "id": 123,
    "name": "张三",
    "email": "zhangsan@example.com"
  }
}
```

### 错误响应
```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "邮箱格式不正确",
    "details": {
      "field": "email",
      "value": "invalid-email"
    }
  }
}
```

## 版本控制

### URL版本控制
```
/api/v1/users
/api/v2/users
```

### 请求头版本控制
```
Accept: application/vnd.api+json;version=1
```

## 安全考虑

### 认证
- JWT Token
- OAuth 2.0
- API Key

### 授权
- 基于角色的访问控制
- 资源级权限
- 速率限制

## 文档

### OpenAPI/Swagger
- 自动生成文档
- 交互式测试
- 代码生成

## 总结

良好的API设计需要考虑一致性、可用性、安全性和可维护性。遵循REST原则和最佳实践可以创建高质量的API。""",
            "summary": "全面介绍RESTful API设计的最佳实践，包括REST原则、HTTP方法、URL设计、响应格式、版本控制和安全考虑。",
            "tags": ["API", "REST", "HTTP", "设计", "后端"],
            "author": "demo",
            "is_published": True
        },
        {
            "title": "我的第一篇草稿",
            "content": """# 我的第一篇草稿

这是一篇还在编写中的文章...

## 待完成的内容

- [ ] 添加更多示例
- [ ] 完善代码片段
- [ ] 添加图片
- [ ] 校对文字

## 当前想法

这里记录一些初步的想法和大纲。

### 主要观点

1. 观点一
2. 观点二
3. 观点三

### 需要研究的问题

- 问题A
- 问题B
- 问题C

## 参考资料

- 资料1
- 资料2
- 资料3

---

*这篇文章还在编写中，请稍后查看完整版本。*""",
            "summary": "这是一篇正在编写中的草稿文章，包含了一些初步的想法和大纲。",
            "tags": ["草稿", "待完成"],
            "author": "demo",
            "is_published": False
        }
    ]
    
    # 创建文章
    for i, article_data in enumerate(articles_data):
        # 找到对应的作者
        author = None
        for user in users:
            if user.username == article_data["author"]:
                author = user
                break
        
        if not author:
            print(f"❌ 找不到作者: {article_data['author']}")
            continue
        
        # 创建文章
        article = WebArticle(
            title=article_data["title"],
            content=article_data["content"],
            author=author.username
        )
        
        # 设置其他属性
        article.summary = article_data["summary"]
        # 添加标签
        for tag in article_data["tags"]:
            article.add_tag(tag)
        # 设置发布状态
        if article_data["is_published"]:
            article.publish()
        
        # 设置创建时间（模拟不同时间创建）
        days_ago = len(articles_data) - i
        article._created_at = datetime.now() - timedelta(days=days_ago)
        
        # 模拟一些浏览量和点赞
        if article.is_published:
            # 使用add_view方法增加浏览量
            for _ in range((i + 1) * 15 + 10):
                article.add_view()
            # 使用add_like方法增加点赞
            for _ in range((i + 1) * 3 + 2):
                article.add_like()
        
        # 使用WebBlogManager的方法添加文章
        blog_manager._articles.append(article)
        print(f"✅ 创建文章: {article.title} (作者: {author.username})")
    
    return blog_manager.articles

def create_demo_comments(blog_manager, users, articles):
    """创建演示评论"""
    print("\n创建演示评论...")
    
    comments_data = [
        {
            "article_index": 0,
            "author": "张三",
            "content": "这篇文章写得很好！对初学者很有帮助。"
        },
        {
            "article_index": 0,
            "author": "李四",
            "content": "Flask确实是一个很好的入门框架，简单易学。"
        },
        {
            "article_index": 1,
            "author": "王五",
            "content": "模板继承的概念很重要，谢谢分享！"
        },
        {
            "article_index": 1,
            "author": "demo",
            "content": "Jinja2的过滤器功能很强大，学到了新知识。"
        },
        {
            "article_index": 2,
            "author": "admin",
            "content": "数据库设计确实需要仔细考虑，这些原则很实用。"
        },
        {
            "article_index": 3,
            "author": "张三",
            "content": "前端技术发展太快了，需要持续学习。"
        },
        {
            "article_index": 4,
            "author": "李四",
            "content": "API设计规范很重要，这篇文章总结得很全面。"
        }
    ]
    
    published_articles = [a for a in articles if a.is_published]
    
    for comment_data in comments_data:
        if comment_data["article_index"] >= len(published_articles):
            continue
            
        article = published_articles[comment_data["article_index"]]
        
        # 找到评论作者
        author = None
        for user in users:
            if user.username == comment_data["author"]:
                author = user
                break
        
        if not author:
            continue
        
        # 创建评论
        comment = Comment(
            content=comment_data["content"],
            author=author.username,
            article_id=article.id
        )
        
        # 添加评论到文章
        article.add_comment(comment)
        print(f"✅ 为文章 '{article.title}' 添加评论 (作者: {author.username})")

def main():
    """主函数"""
    print("🚀 开始初始化演示数据...\n")

    # 创建博客管理器
    blog_manager = WebBlogManager()

    # 清除现有数据
    print("🧹 清除现有数据...")
    blog_manager._users.clear()
    blog_manager._articles.clear()
    
    try:
        # 创建演示数据
        users = create_demo_users(blog_manager)
        articles = create_demo_articles(blog_manager, users)
        create_demo_comments(blog_manager, users, articles)
        
        # 保存数据
        print("\n💾 保存数据到文件...")
        blog_manager._save_web_data()
        
        print("\n✅ 演示数据初始化完成！")
        print("\n📊 数据统计:")
        print(f"   用户数量: {len(users)}")
        print(f"   文章数量: {len(articles)}")
        print(f"   已发布文章: {len([a for a in articles if a.is_published])}")
        print(f"   草稿文章: {len([a for a in articles if not a.is_published])}")
        
        print("\n🔑 演示账户:")
        print("   管理员: admin / admin123")
        print("   演示用户: demo / demo123")
        print("   其他用户: 用户名 / password123")
        
        print("\n🌐 现在可以运行 Flask 应用:")
        print("   python app.py")
        
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
