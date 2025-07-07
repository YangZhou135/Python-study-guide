#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库初始化脚本
"""

import os
import sys

# 设置环境变量
os.environ['FLASK_ENV'] = 'development'
os.environ['SECRET_KEY'] = 'dev-secret-key-for-testing'
os.environ['JWT_SECRET_KEY'] = 'dev-jwt-secret-key-for-testing'

# 添加step5_database到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '../step5_database'))

from app import create_app
from models import db, User, Article, Tag

def init_database():
    """初始化数据库"""
    app = create_app('development')
    
    with app.app_context():
        # 创建所有表
        db.create_all()
        print('✅ 数据库表创建完成')
        
        # 创建示例用户
        if not User.query.filter_by(username='demo').first():
            demo_user = User(username='demo', email='demo@example.com', password='demo123')
            db.session.add(demo_user)

            # 创建管理员用户
            admin_user = User(username='admin', email='admin@example.com', password='admin123')
            db.session.add(admin_user)
            
            db.session.commit()
            print('✅ 示例用户创建完成')
            
            # 创建示例文章
            sample_article = Article(
                title='欢迎使用个人博客管理系统',
                content='''# 欢迎使用个人博客管理系统

这是一个使用Flask和Vue.js构建的现代化博客系统。

## 主要功能

- 用户注册和登录
- 文章创建、编辑、删除
- 文章分类和标签
- 评论系统
- 搜索功能
- 响应式设计

## 技术栈

### 后端
- Flask 2.3.3
- SQLAlchemy 2.0.23
- Flask-JWT-Extended
- Flask-CORS

### 前端
- Vue.js 3
- TypeScript
- Pinia状态管理
- Element Plus UI

## 开始使用

1. 注册账户或使用演示账户登录
2. 创建你的第一篇文章
3. 探索更多功能

祝你使用愉快！''',
                author_id=demo_user.id
            )

            # 设置其他属性
            sample_article.summary = '个人博客管理系统介绍和使用指南'
            sample_article.is_published = True
            
            # 创建示例标签
            tags = ['Flask', 'Vue.js', 'Python', 'JavaScript', '全栈开发']
            for tag_name in tags:
                tag = Tag(name=tag_name)
                db.session.add(tag)
                if tag_name in ['Flask', 'Vue.js', 'Python']:
                    sample_article.tags.append(tag)
            
            db.session.add(sample_article)
            db.session.commit()
            print('✅ 示例文章和标签创建完成')
            
            print(f'''
🎉 数据库初始化完成！

示例账户：
- 普通用户: demo / demo123
- 管理员: admin / admin123

API地址: http://localhost:5000/api/v1
API文档: http://localhost:5000/api/v1/docs
''')
        else:
            print('⚠️  数据库已存在数据，跳过示例数据创建')

if __name__ == '__main__':
    init_database()
