#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web版博客数据模型
扩展原有模型以支持Web功能
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from step2_oop.models import Article, User, Tag, BlogManager
from step3_files.file_manager import FileManager
import datetime
import hashlib
import secrets
from typing import Dict, List, Any, Optional

class WebUser(User):
    """Web版用户类，扩展原有User类"""
    
    def __init__(self, username: str, email: str, password: str = None):
        """
        初始化Web用户
        
        Args:
            username: 用户名
            email: 邮箱
            password: 密码（明文，会自动哈希）
        """
        super().__init__(username, email)
        self._password_hash = None
        self._is_active = True
        self._last_login = None
        self._login_count = 0
        
        if password:
            self.set_password(password)
    
    def set_password(self, password: str) -> None:
        """设置密码（自动哈希）"""
        # 生成盐值
        salt = secrets.token_hex(16)
        # 创建哈希
        password_hash = hashlib.pbkdf2_hmac('sha256', 
                                          password.encode('utf-8'), 
                                          salt.encode('utf-8'), 
                                          100000)
        # 存储盐值和哈希
        self._password_hash = salt + password_hash.hex()
    
    def check_password(self, password: str) -> bool:
        """验证密码"""
        if not self._password_hash:
            return False
        
        # 提取盐值
        salt = self._password_hash[:32]
        stored_hash = self._password_hash[32:]
        
        # 计算输入密码的哈希
        password_hash = hashlib.pbkdf2_hmac('sha256',
                                          password.encode('utf-8'),
                                          salt.encode('utf-8'),
                                          100000)
        
        return password_hash.hex() == stored_hash
    
    def login(self) -> None:
        """记录登录"""
        self._last_login = datetime.datetime.now()
        self._login_count += 1
    
    @property
    def is_active(self) -> bool:
        """用户是否激活"""
        return self._is_active
    
    @property
    def last_login(self) -> Optional[datetime.datetime]:
        """最后登录时间"""
        return self._last_login
    
    @property
    def login_count(self) -> int:
        """登录次数"""
        return self._login_count
    
    def deactivate(self) -> None:
        """停用用户"""
        self._is_active = False
    
    def activate(self) -> None:
        """激活用户"""
        self._is_active = True
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典（用于JSON序列化）"""
        return {
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "is_active": self._is_active,
            "last_login": self._last_login.isoformat() if self._last_login else None,
            "login_count": self._login_count,
            "password_hash": self._password_hash,
            "article_count": len(self._articles)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WebUser':
        """从字典创建用户对象"""
        user = cls(data["username"], data["email"])
        user._created_at = datetime.datetime.fromisoformat(data["created_at"])
        user._is_active = data.get("is_active", True)
        user._login_count = data.get("login_count", 0)
        user._password_hash = data.get("password_hash")
        
        if data.get("last_login"):
            user._last_login = datetime.datetime.fromisoformat(data["last_login"])
        
        return user

class WebArticle(Article):
    """Web版文章类，扩展原有Article类"""
    
    def __init__(self, title: str, content: str, author: str, tags: List[str] = None):
        """初始化Web文章"""
        super().__init__(title, content, author, tags)
        self._is_published = False
        self._summary = ""
        self._featured_image = None
        self._comments = []
        self._slug = self._generate_slug()
    
    def _generate_slug(self) -> str:
        """生成URL友好的slug"""
        import re
        # 简单的slug生成（实际项目中可能需要更复杂的逻辑）
        slug = re.sub(r'[^\w\s-]', '', self.title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return f"{slug}-{self.id}"
    
    @property
    def is_published(self) -> bool:
        """文章是否已发布"""
        return self._is_published
    
    @property
    def summary(self) -> str:
        """文章摘要"""
        if self._summary:
            return self._summary
        # 自动生成摘要（取前150个字符）
        return self.content[:150] + "..." if len(self.content) > 150 else self.content
    
    @summary.setter
    def summary(self, value: str) -> None:
        """设置文章摘要"""
        self._summary = value
    
    @property
    def featured_image(self) -> Optional[str]:
        """特色图片"""
        return self._featured_image
    
    @featured_image.setter
    def featured_image(self, value: str) -> None:
        """设置特色图片"""
        self._featured_image = value
    
    @property
    def slug(self) -> str:
        """URL slug"""
        return self._slug
    
    @property
    def comments(self) -> List['Comment']:
        """文章评论"""
        return self._comments
    
    def publish(self) -> None:
        """发布文章"""
        self._is_published = True
    
    def unpublish(self) -> None:
        """取消发布"""
        self._is_published = False
    
    def add_comment(self, comment: 'Comment') -> None:
        """添加评论"""
        self._comments.append(comment)
    
    def get_reading_time(self) -> int:
        """估算阅读时间（分钟）"""
        # 假设每分钟阅读200个字符
        return max(1, len(self.content) // 200)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        base_dict = {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "author": self.author,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "views": self.views,
            "likes": self.likes,
            "is_published": self._is_published,
            "summary": self._summary,
            "featured_image": self._featured_image,
            "slug": self._slug,
            "comments": [comment.to_dict() for comment in self._comments]
        }
        return base_dict
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WebArticle':
        """从字典创建文章对象"""
        article = cls(data["title"], data["content"], data["author"], data.get("tags", []))
        article._id = data["id"]
        article._created_at = datetime.datetime.fromisoformat(data["created_at"])
        article._views = data.get("views", 0)
        article._likes = data.get("likes", 0)
        article._is_published = data.get("is_published", False)
        article._summary = data.get("summary", "")
        article._featured_image = data.get("featured_image")
        article._slug = data.get("slug", article._generate_slug())
        
        # 加载评论
        for comment_data in data.get("comments", []):
            comment = Comment.from_dict(comment_data)
            article._comments.append(comment)
        
        return article

class Comment:
    """评论类"""
    
    _comment_count = 0
    
    def __init__(self, content: str, author: str, article_id: int):
        """
        初始化评论
        
        Args:
            content: 评论内容
            author: 评论作者
            article_id: 所属文章ID
        """
        Comment._comment_count += 1
        self._id = Comment._comment_count
        self._content = content
        self._author = author
        self._article_id = article_id
        self._created_at = datetime.datetime.now()
        self._is_approved = True  # 简单起见，默认审核通过
    
    @property
    def id(self) -> int:
        """评论ID"""
        return self._id
    
    @property
    def content(self) -> str:
        """评论内容"""
        return self._content
    
    @property
    def author(self) -> str:
        """评论作者"""
        return self._author
    
    @property
    def article_id(self) -> int:
        """所属文章ID"""
        return self._article_id
    
    @property
    def created_at(self) -> datetime.datetime:
        """创建时间"""
        return self._created_at
    
    @property
    def is_approved(self) -> bool:
        """是否审核通过"""
        return self._is_approved
    
    def approve(self) -> None:
        """审核通过"""
        self._is_approved = True
    
    def reject(self) -> None:
        """审核拒绝"""
        self._is_approved = False
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self._id,
            "content": self._content,
            "author": self._author,
            "article_id": self._article_id,
            "created_at": self._created_at.isoformat(),
            "is_approved": self._is_approved
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Comment':
        """从字典创建评论对象"""
        comment = cls(data["content"], data["author"], data["article_id"])
        comment._id = data["id"]
        comment._created_at = datetime.datetime.fromisoformat(data["created_at"])
        comment._is_approved = data.get("is_approved", True)
        return comment

class WebBlogManager(BlogManager):
    """Web版博客管理器"""
    
    def __init__(self):
        """初始化Web博客管理器"""
        super().__init__()
        self.file_manager = FileManager()
        self._current_user = None
        self._load_web_data()
    
    def _load_web_data(self):
        """加载Web版数据"""
        try:
            # 加载用户数据
            users_data = self.file_manager.load_json("web_users.json", [])
            self._users = []
            for user_data in users_data:
                user = WebUser.from_dict(user_data)
                self._users.append(user)
            
            # 加载文章数据
            articles_data = self.file_manager.load_json("web_articles.json", [])
            self._articles = []
            for article_data in articles_data:
                article = WebArticle.from_dict(article_data)
                self._articles.append(article)
                
                # 关联文章到用户
                author_user = self.get_user(article.author)
                if author_user:
                    author_user._articles.append(article)
            
            # 更新计数器
            if self._users:
                # 这里需要更新WebUser的计数器，但原始User类没有这个功能
                pass
            if self._articles:
                Article._article_count = max(article.id for article in self._articles)
                WebArticle._article_count = Article._article_count
            
            print(f"✅ Web数据加载完成: {len(self._users)} 个用户, {len(self._articles)} 篇文章")
            
        except Exception as e:
            print(f"❌ 加载Web数据失败: {e}")
    
    def _save_web_data(self):
        """保存Web版数据"""
        try:
            # 保存用户数据
            users_data = [user.to_dict() for user in self._users]
            self.file_manager.save_json("web_users.json", users_data)
            
            # 保存文章数据
            articles_data = [article.to_dict() for article in self._articles]
            self.file_manager.save_json("web_articles.json", articles_data)
            
            print("✅ Web数据保存成功")
            
        except Exception as e:
            print(f"❌ 保存Web数据失败: {e}")
    
    def register_user(self, username: str, email: str, password: str) -> Optional[WebUser]:
        """注册新用户"""
        # 检查用户名是否已存在
        if self.get_user(username):
            return None
        
        # 检查邮箱是否已存在
        for user in self._users:
            if user.email == email:
                return None
        
        # 创建新用户
        user = WebUser(username, email, password)
        self._users.append(user)
        self._save_web_data()
        
        return user
    
    def authenticate_user(self, username: str, password: str) -> Optional[WebUser]:
        """用户认证"""
        user = self.get_user(username)
        if user and isinstance(user, WebUser) and user.check_password(password):
            user.login()
            self._save_web_data()
            return user
        return None
    
    def set_current_user(self, user: WebUser) -> None:
        """设置当前用户"""
        self._current_user = user
    
    def get_current_user(self) -> Optional[WebUser]:
        """获取当前用户"""
        return self._current_user
    
    def logout_user(self) -> None:
        """用户登出"""
        self._current_user = None
    
    def create_article(self, title: str, content: str, author: str, 
                      tags: List[str] = None, summary: str = "", 
                      featured_image: str = None) -> WebArticle:
        """创建文章"""
        article = WebArticle(title, content, author, tags)
        if summary:
            article.summary = summary
        if featured_image:
            article.featured_image = featured_image
        
        self.add_article(article)
        return article
    
    def get_published_articles(self) -> List[WebArticle]:
        """获取已发布的文章"""
        return [article for article in self._articles 
                if isinstance(article, WebArticle) and article.is_published]
    
    def get_articles_by_user(self, username: str, published_only: bool = False) -> List[WebArticle]:
        """获取用户的文章"""
        user_articles = [article for article in self._articles 
                        if article.author == username and isinstance(article, WebArticle)]
        
        if published_only:
            user_articles = [article for article in user_articles if article.is_published]
        
        return user_articles
    
    def search_articles(self, query: str, published_only: bool = True) -> List[WebArticle]:
        """搜索文章"""
        results = []
        query_lower = query.lower()
        
        for article in self._articles:
            if not isinstance(article, WebArticle):
                continue
            
            if published_only and not article.is_published:
                continue
            
            # 在标题、内容、标签中搜索
            if (query_lower in article.title.lower() or 
                query_lower in article.content.lower() or 
                any(query_lower in tag.lower() for tag in article.tags)):
                results.append(article)
        
        return results
    
    def add_comment(self, article_id: int, content: str, author: str) -> Optional[Comment]:
        """添加评论"""
        article = self.get_article(article_id)
        if article and isinstance(article, WebArticle):
            comment = Comment(content, author, article_id)
            article.add_comment(comment)
            self._save_web_data()
            return comment
        return None
    
    def get_recent_articles(self, limit: int = 5, published_only: bool = True) -> List[WebArticle]:
        """获取最新文章"""
        articles = [article for article in self._articles if isinstance(article, WebArticle)]
        
        if published_only:
            articles = [article for article in articles if article.is_published]
        
        # 按创建时间排序
        articles.sort(key=lambda x: x.created_at, reverse=True)
        return articles[:limit]
    
    def get_popular_articles(self, limit: int = 5, published_only: bool = True) -> List[WebArticle]:
        """获取热门文章（按浏览量）"""
        articles = [article for article in self._articles if isinstance(article, WebArticle)]
        
        if published_only:
            articles = [article for article in articles if article.is_published]
        
        # 按浏览量排序
        articles.sort(key=lambda x: x.views, reverse=True)
        return articles[:limit]

    @property
    def users(self) -> List[WebUser]:
        """获取所有用户"""
        return self._users

    @property
    def articles(self) -> List[WebArticle]:
        """获取所有文章"""
        return self._articles
