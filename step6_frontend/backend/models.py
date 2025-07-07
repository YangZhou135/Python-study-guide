#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQLAlchemy数据库模型定义
将原有的文件存储模型转换为数据库模型
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
import secrets
import re

db = SQLAlchemy()

# 数据库初始化函数
def init_db(app):
    """初始化数据库"""
    db.init_app(app)

    with app.app_context():
        # 创建所有表
        db.create_all()

        # 创建默认数据
        create_default_data()

def create_default_data():
    """创建默认数据"""
    # 检查是否已有数据
    if User.query.first():
        return

    # 创建默认管理员用户
    admin = User(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    db.session.add(admin)

    # 创建默认标签
    default_tags = ['Python', 'Flask', 'Web开发', '数据库', '教程']
    for tag_name in default_tags:
        tag = Tag(name=tag_name, description=f'{tag_name}相关内容')
        db.session.add(tag)

    db.session.commit()
    print("✅ 默认数据创建完成")

# 文章标签关联表 (多对多关系)
article_tags = Table('article_tags', db.metadata,
    Column('article_id', Integer, ForeignKey('articles.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_login = Column(DateTime)
    login_count = Column(Integer, default=0, nullable=False)
    
    # 关系定义
    articles = relationship('Article', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    comments = relationship('Comment', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, username, email, password=None):
        """初始化用户"""
        self.username = username
        self.email = email
        if password:
            self.set_password(password)
    
    def set_password(self, password):
        """设置密码哈希"""
        # 使用Flask-Werkzeug的密码哈希
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def login(self):
        """记录登录"""
        self.last_login = datetime.utcnow()
        self.login_count += 1
        db.session.commit()
    
    @hybrid_property
    def article_count(self):
        """用户文章数量"""
        return self.articles.count()
    
    @hybrid_property
    def published_article_count(self):
        """用户已发布文章数量"""
        return self.articles.filter_by(is_published=True).count()
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'login_count': self.login_count,
            'article_count': self.article_count,
            'published_article_count': self.published_article_count
        }
    
    def __repr__(self):
        return f'<User {self.username}>'

class Tag(db.Model):
    """标签模型"""
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)
    usage_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __init__(self, name, description=None):
        """初始化标签"""
        self.name = name
        self.description = description
    
    def increment_usage(self):
        """增加使用次数"""
        self.usage_count += 1
        db.session.commit()
    
    def decrement_usage(self):
        """减少使用次数"""
        if self.usage_count > 0:
            self.usage_count -= 1
            db.session.commit()
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'usage_count': self.usage_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Tag {self.name}>'

class Article(db.Model):
    """文章模型"""
    __tablename__ = 'articles'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False)
    summary = Column(Text)
    slug = Column(String(200), unique=True, nullable=False, index=True)
    is_published = Column(Boolean, default=False, nullable=False, index=True)
    featured_image = Column(String(255))
    views = Column(Integer, default=0, nullable=False)
    likes = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 外键
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    
    # 关系定义
    tags = relationship('Tag', secondary=article_tags, backref=backref('articles', lazy='dynamic'))
    comments = relationship('Comment', backref='article', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, title, content, author_id, tags=None):
        """初始化文章"""
        self.title = title
        self.content = content
        self.author_id = author_id
        self.slug = self._generate_slug()
        
        # 添加标签
        if tags:
            for tag_name in tags:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                self.tags.append(tag)
    
    def _generate_slug(self):
        """生成URL友好的slug"""
        # 简单的slug生成
        slug = re.sub(r'[^\w\s-]', '', self.title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return f"{slug}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    
    def publish(self):
        """发布文章"""
        self.is_published = True
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def unpublish(self):
        """取消发布"""
        self.is_published = False
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def add_view(self):
        """增加浏览量"""
        self.views += 1
        db.session.commit()
    
    def add_like(self):
        """增加点赞"""
        self.likes += 1
        db.session.commit()
    
    def add_tag(self, tag_name):
        """添加标签"""
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.session.add(tag)
        if tag not in self.tags:
            self.tags.append(tag)
            tag.increment_usage()
    
    def remove_tag(self, tag_name):
        """移除标签"""
        tag = Tag.query.filter_by(name=tag_name).first()
        if tag and tag in self.tags:
            self.tags.remove(tag)
            tag.decrement_usage()
    
    @hybrid_property
    def comment_count(self):
        """评论数量"""
        return self.comments.filter_by(is_approved=True).count()
    
    @hybrid_property
    def reading_time(self):
        """估算阅读时间（分钟）"""
        return max(1, len(self.content) // 200)
    
    @hybrid_property
    def tag_names(self):
        """标签名称列表"""
        return [tag.name for tag in self.tags]
    
    def get_summary(self, max_length=150):
        """获取摘要"""
        if self.summary:
            return self.summary
        return self.content[:max_length] + "..." if len(self.content) > max_length else self.content
    
    def to_dict(self, include_content=False):
        """转换为字典"""
        data = {
            'id': self.id,
            'title': self.title,
            'summary': self.get_summary(),
            'slug': self.slug,
            'is_published': self.is_published,
            'featured_image': self.featured_image,
            'views': self.views,
            'likes': self.likes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'author': self.author.username if self.author else None,
            'author_id': self.author_id,
            'tags': self.tag_names,
            'comment_count': self.comment_count,
            'reading_time': self.reading_time
        }
        
        if include_content:
            data['content'] = self.content
        
        return data
    
    def __repr__(self):
        return f'<Article {self.title}>'

class Comment(db.Model):
    """评论模型"""
    __tablename__ = 'comments'
    
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    is_approved = Column(Boolean, default=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # 外键
    article_id = Column(Integer, ForeignKey('articles.id'), nullable=False, index=True)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey('comments.id'), index=True)  # 支持回复评论
    
    # 关系定义
    replies = relationship('Comment', backref=backref('parent', remote_side=[id]), lazy='dynamic')
    
    def __init__(self, content, article_id, author_id, parent_id=None):
        """初始化评论"""
        self.content = content
        self.article_id = article_id
        self.author_id = author_id
        self.parent_id = parent_id
    
    def approve(self):
        """审核通过"""
        self.is_approved = True
        db.session.commit()
    
    def reject(self):
        """审核拒绝"""
        self.is_approved = False
        db.session.commit()
    
    @hybrid_property
    def reply_count(self):
        """回复数量"""
        return self.replies.filter_by(is_approved=True).count()
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'content': self.content,
            'is_approved': self.is_approved,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'article_id': self.article_id,
            'author': self.author.username if self.author else None,
            'author_id': self.author_id,
            'parent_id': self.parent_id,
            'reply_count': self.reply_count
        }
    
    def __repr__(self):
        return f'<Comment {self.id} by {self.author.username if self.author else "Unknown"}>'
