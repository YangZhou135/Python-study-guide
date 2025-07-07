# Stage 5: 数据库操作 - SQLAlchemy集成

## 🎯 学习目标

在这个阶段，您将学习：

1. **SQLAlchemy ORM基础**
   - 数据库连接和配置
   - 模型定义和关系映射
   - 查询构建器和会话管理

2. **数据库设计**
   - 表结构设计
   - 外键关系
   - 索引优化

3. **数据迁移**
   - 从文件存储迁移到数据库
   - 数据库版本管理
   - 数据备份和恢复

4. **高级查询**
   - 复杂查询构建
   - 聚合函数
   - 分页和排序

5. **性能优化**
   - 查询优化
   - 连接池配置
   - 缓存策略

## 📁 项目结构

```
step5_database/
├── README.md              # 本文件
├── requirements.txt       # 数据库相关依赖
├── config.py             # 数据库配置
├── models.py             # SQLAlchemy模型定义
├── database.py           # 数据库初始化和工具
├── migration.py          # 数据迁移脚本
├── app.py               # Flask应用 (数据库版)
├── init_db.py           # 数据库初始化脚本
├── examples_db.py       # 数据库操作示例
├── migrations/          # 数据库迁移文件
├── instance/           # 数据库文件目录
│   └── blog.db         # SQLite数据库文件
└── tests/              # 数据库测试
    ├── test_models.py
    └── test_queries.py
```

## 🗄️ 数据库设计

### 表结构

```sql
-- 用户表
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    login_count INTEGER DEFAULT 0
);

-- 文章表
CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    summary TEXT,
    slug VARCHAR(200) UNIQUE NOT NULL,
    is_published BOOLEAN DEFAULT FALSE,
    featured_image VARCHAR(255),
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    author_id INTEGER NOT NULL,
    FOREIGN KEY (author_id) REFERENCES users (id)
);

-- 标签表
CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 文章标签关联表 (多对多)
CREATE TABLE article_tags (
    article_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (article_id, tag_id),
    FOREIGN KEY (article_id) REFERENCES articles (id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE
);

-- 评论表
CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    is_approved BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    article_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    parent_id INTEGER,  -- 支持回复评论
    FOREIGN KEY (article_id) REFERENCES articles (id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES users (id),
    FOREIGN KEY (parent_id) REFERENCES comments (id)
);
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd step5_database
pip install -r requirements.txt
```

### 2. 初始化数据库

```bash
python init_db.py
```

### 3. 迁移现有数据

```bash
python migration.py --from-files
```

### 4. 运行数据库版应用

```bash
python app.py
```

## 📚 核心概念学习

### 1. SQLAlchemy模型定义

```python
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    
    # 关系定义
    articles = relationship('Article', backref='author', lazy='dynamic')
    comments = relationship('Comment', backref='author', lazy='dynamic')
```

### 2. 数据库查询

```python
# 基本查询
users = session.query(User).all()
user = session.query(User).filter_by(username='admin').first()

# 复杂查询
popular_articles = session.query(Article)\
    .filter(Article.is_published == True)\
    .order_by(Article.views.desc())\
    .limit(10).all()

# 关联查询
articles_with_comments = session.query(Article)\
    .join(Comment)\
    .filter(Article.is_published == True)\
    .all()
```

### 3. 数据库事务

```python
try:
    # 开始事务
    article = Article(title="新文章", content="内容")
    session.add(article)
    
    # 添加标签
    tag = Tag(name="Python")
    article.tags.append(tag)
    
    # 提交事务
    session.commit()
except Exception as e:
    # 回滚事务
    session.rollback()
    raise e
```

## 🔧 配置说明

### 数据库连接配置

```python
# config.py
import os

class DatabaseConfig:
    # SQLite配置 (开发环境)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/blog.db'
    
    # PostgreSQL配置 (生产环境)
    # SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@localhost/blog'
    
    # MySQL配置 (可选)
    # SQLALCHEMY_DATABASE_URI = 'mysql://user:pass@localhost/blog'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # 开发时显示SQL语句
```

## 🧪 测试功能

### 数据库操作测试

```bash
python examples_db.py
```

### 单元测试

```bash
python -m pytest tests/
```

## 📊 性能监控

### 查询性能分析

```python
# 启用SQL日志
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# 查询执行时间监控
from sqlalchemy import event
from sqlalchemy.engine import Engine
import time

@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    context._query_start_time = time.time()

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - context._query_start_time
    print(f"Query took {total:.4f} seconds")
```

## 🎯 下一步

完成Stage 5后，您将掌握：
- SQLAlchemy ORM的使用
- 数据库设计和优化
- 数据迁移和版本管理
- 复杂查询构建
- 数据库性能监控

准备好进入 **Stage 6: 前后端集成** 了吗？
