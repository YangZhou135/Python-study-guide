#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库初始化脚本
创建表结构并插入演示数据
"""

import os
import argparse
from datetime import datetime, timedelta
from database import create_app
from models import db, User, Article, Tag, Comment

def create_demo_data(app):
    """创建演示数据"""
    print("🚀 创建演示数据...")
    
    with app.app_context():
        # 清空现有数据
        print("🧹 清空现有数据...")
        Comment.query.delete()
        Article.query.delete()
        Tag.query.delete()
        User.query.delete()
        db.session.commit()
        
        # 创建用户
        print("👥 创建演示用户...")
        users_data = [
            {'username': 'admin', 'email': 'admin@example.com', 'password': 'admin123'},
            {'username': 'demo', 'email': 'demo@example.com', 'password': 'demo123'},
            {'username': '张三', 'email': 'zhangsan@example.com', 'password': 'password123'},
            {'username': '李四', 'email': 'lisi@example.com', 'password': 'password123'},
            {'username': '王五', 'email': 'wangwu@example.com', 'password': 'password123'}
        ]
        
        users = {}
        for user_data in users_data:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password']
            )
            db.session.add(user)
            users[user_data['username']] = user
            print(f"✅ 创建用户: {user_data['username']}")
        
        db.session.commit()
        
        # 创建标签
        print("🏷️  创建演示标签...")
        tags_data = [
            {'name': 'Python', 'description': 'Python编程语言相关内容'},
            {'name': 'Flask', 'description': 'Flask Web框架相关内容'},
            {'name': 'Web开发', 'description': 'Web开发技术和最佳实践'},
            {'name': '数据库', 'description': '数据库设计和操作'},
            {'name': 'SQLAlchemy', 'description': 'SQLAlchemy ORM框架'},
            {'name': '教程', 'description': '学习教程和指南'},
            {'name': '最佳实践', 'description': '开发最佳实践'},
            {'name': '前端', 'description': '前端开发技术'},
            {'name': 'API', 'description': 'API设计和开发'},
            {'name': '性能优化', 'description': '性能优化技巧'}
        ]
        
        tags = {}
        for tag_data in tags_data:
            tag = Tag(name=tag_data['name'], description=tag_data['description'])
            db.session.add(tag)
            tags[tag_data['name']] = tag
            print(f"✅ 创建标签: {tag_data['name']}")
        
        db.session.commit()
        
        # 创建文章
        print("📝 创建演示文章...")
        articles_data = [
            {
                'title': 'Python Web开发入门指南',
                'content': '''# Python Web开发入门指南

Python是一门优秀的编程语言，特别适合Web开发。本文将介绍Python Web开发的基础知识。

## 为什么选择Python？

1. **简洁易读**：Python语法简洁，代码可读性强
2. **丰富的框架**：Django、Flask、FastAPI等优秀框架
3. **强大的生态**：丰富的第三方库和工具
4. **活跃的社区**：大量的学习资源和技术支持

## Flask框架介绍

Flask是一个轻量级的Web框架，具有以下特点：

- 简单易学，上手快
- 灵活性高，可扩展性强
- 文档完善，社区活跃
- 适合小到中型项目

## 开发环境搭建

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate   # Windows

# 安装Flask
pip install Flask
```

## 第一个Flask应用

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
```

这就是一个最简单的Flask应用！''',
                'author': 'admin',
                'tags': ['Python', 'Flask', 'Web开发', '教程'],
                'is_published': True
            },
            {
                'title': 'SQLAlchemy数据库操作详解',
                'content': '''# SQLAlchemy数据库操作详解

SQLAlchemy是Python最流行的ORM框架，提供了强大的数据库操作能力。

## 什么是ORM？

ORM（Object-Relational Mapping）对象关系映射，是一种程序设计技术，用于实现面向对象编程语言里不同类型系统的数据之间的转换。

## SQLAlchemy的优势

1. **功能强大**：支持复杂查询和关系映射
2. **性能优秀**：提供连接池和查询优化
3. **灵活性高**：支持多种数据库
4. **文档完善**：详细的官方文档

## 模型定义

```python
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
```

## 数据库查询

```python
# 查询所有用户
users = session.query(User).all()

# 条件查询
user = session.query(User).filter_by(username='admin').first()

# 复杂查询
users = session.query(User).filter(User.id > 10).order_by(User.username).all()
```''',
                'author': '张三',
                'tags': ['Python', 'SQLAlchemy', '数据库', '教程'],
                'is_published': True
            },
            {
                'title': 'Web应用性能优化技巧',
                'content': '''# Web应用性能优化技巧

性能优化是Web开发中的重要话题，本文分享一些实用的优化技巧。

## 数据库优化

1. **索引优化**：为常用查询字段添加索引
2. **查询优化**：避免N+1查询问题
3. **连接池**：使用数据库连接池
4. **缓存策略**：合理使用缓存

## 前端优化

1. **资源压缩**：压缩CSS、JS文件
2. **图片优化**：使用合适的图片格式
3. **CDN加速**：使用内容分发网络
4. **懒加载**：按需加载资源

## 服务器优化

1. **负载均衡**：分散服务器压力
2. **反向代理**：使用Nginx等反向代理
3. **缓存服务**：Redis、Memcached
4. **监控告警**：实时监控系统状态

## Flask性能优化

```python
# 使用缓存
from flask_caching import Cache

cache = Cache(app)

@app.route('/api/data')
@cache.cached(timeout=300)
def get_data():
    # 耗时操作
    return expensive_operation()
```''',
                'author': '李四',
                'tags': ['性能优化', 'Web开发', '最佳实践'],
                'is_published': True
            },
            {
                'title': 'RESTful API设计指南',
                'content': '''# RESTful API设计指南

REST是一种软件架构风格，用于设计网络应用程序的接口。

## REST原则

1. **统一接口**：使用标准HTTP方法
2. **无状态**：每个请求都包含完整信息
3. **可缓存**：响应可以被缓存
4. **分层系统**：支持分层架构

## HTTP方法

- **GET**：获取资源
- **POST**：创建资源
- **PUT**：更新资源
- **DELETE**：删除资源
- **PATCH**：部分更新

## URL设计

```
GET    /api/users          # 获取用户列表
GET    /api/users/1        # 获取特定用户
POST   /api/users          # 创建用户
PUT    /api/users/1        # 更新用户
DELETE /api/users/1        # 删除用户
```

## 状态码

- **200 OK**：请求成功
- **201 Created**：资源创建成功
- **400 Bad Request**：请求错误
- **401 Unauthorized**：未授权
- **404 Not Found**：资源不存在
- **500 Internal Server Error**：服务器错误''',
                'author': 'demo',
                'tags': ['API', 'Web开发', '最佳实践'],
                'is_published': True
            },
            {
                'title': '我的学习笔记草稿',
                'content': '''这是一篇草稿文章，记录我的学习心得...

## 今天学到的内容

1. SQLAlchemy的基本用法
2. Flask路由设计
3. 数据库迁移

还需要继续完善...''',
                'author': 'demo',
                'tags': ['学习笔记'],
                'is_published': False
            }
        ]
        
        articles = []
        for i, article_data in enumerate(articles_data):
            author = users[article_data['author']]
            
            article = Article(
                title=article_data['title'],
                content=article_data['content'],
                author_id=author.id
            )
            article.is_published = article_data['is_published']
            
            # 设置创建时间（模拟不同时间创建）
            article.created_at = datetime.utcnow() - timedelta(days=len(articles_data)-i)
            
            # 添加标签
            for tag_name in article_data['tags']:
                if tag_name in tags:
                    article.tags.append(tags[tag_name])
                    tags[tag_name].usage_count += 1
            
            # 模拟浏览量和点赞
            if article.is_published:
                article.views = (i + 1) * 25 + 10
                article.likes = (i + 1) * 5 + 2
            
            db.session.add(article)
            articles.append(article)
            print(f"✅ 创建文章: {article_data['title']}")
        
        db.session.commit()
        
        # 创建评论
        print("💬 创建演示评论...")
        comments_data = [
            {
                'article_index': 0,
                'author': '张三',
                'content': '这篇文章写得很好！对初学者很有帮助。'
            },
            {
                'article_index': 0,
                'author': '李四',
                'content': 'Flask确实是一个很好的入门框架，简单易学。'
            },
            {
                'article_index': 1,
                'author': '王五',
                'content': 'SQLAlchemy的功能确实很强大，感谢分享！'
            },
            {
                'article_index': 1,
                'author': 'demo',
                'content': 'ORM的概念很重要，这篇文章解释得很清楚。'
            },
            {
                'article_index': 2,
                'author': 'admin',
                'content': '性能优化确实需要从多个方面考虑，这些技巧很实用。'
            },
            {
                'article_index': 3,
                'author': '张三',
                'content': 'RESTful API设计规范很重要，谢谢总结！'
            }
        ]
        
        published_articles = [a for a in articles if a.is_published]
        
        for comment_data in comments_data:
            if comment_data['article_index'] >= len(published_articles):
                continue
            
            article = published_articles[comment_data['article_index']]
            author = users[comment_data['author']]
            
            comment = Comment(
                content=comment_data['content'],
                article_id=article.id,
                author_id=author.id
            )
            
            # 设置评论时间
            comment.created_at = article.created_at + timedelta(hours=comment_data['article_index']+1)
            
            db.session.add(comment)
            print(f"✅ 为文章 '{article.title}' 添加评论 (作者: {author.username})")
        
        db.session.commit()
        
        print("\n✅ 演示数据创建完成！")
        
        # 打印统计信息
        app.db_manager.print_statistics()
        
        print("\n🔑 演示账户:")
        print("   管理员: admin / admin123")
        print("   演示用户: demo / demo123")
        print("   其他用户: 用户名 / password123")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='数据库初始化工具')
    parser.add_argument('--config', default='development', help='配置环境')
    parser.add_argument('--demo-data', action='store_true', help='创建演示数据')
    
    args = parser.parse_args()
    
    # 创建应用
    app = create_app(args.config)
    
    with app.app_context():
        print("🗄️  初始化数据库...")
        
        # 创建表
        db.create_all()
        print("✅ 数据库表创建完成")
        
        # 创建演示数据
        if args.demo_data:
            create_demo_data(app)
        
        print("\n🌐 现在可以运行应用:")
        print("   python app.py")

if __name__ == '__main__':
    main()
