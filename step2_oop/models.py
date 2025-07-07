#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
博客系统数据模型
学习Python面向对象编程的核心概念
"""

import datetime
from typing import List, Optional

class Article:
    """博客文章类"""
    
    # 类属性：所有文章的计数器
    _article_count = 0
    
    def __init__(self, title: str, content: str, author: str, tags: Optional[List[str]] = None):
        """
        初始化文章
        
        Args:
            title: 文章标题
            content: 文章内容
            author: 作者
            tags: 标签列表
        """
        # 输入验证
        if not title.strip():
            raise ValueError("文章标题不能为空")
        if not content.strip():
            raise ValueError("文章内容不能为空")
        if not author.strip():
            raise ValueError("作者不能为空")
        
        # 实例属性
        Article._article_count += 1
        self._id = Article._article_count
        self._title = title.strip()
        self._content = content.strip()
        self._author = author.strip()
        self._tags = tags or []
        self._created_at = datetime.datetime.now()
        self._views = 0
        self._likes = 0
    
    # 属性装饰器：提供受控的属性访问
    @property
    def id(self) -> int:
        """文章ID（只读）"""
        return self._id
    
    @property
    def title(self) -> str:
        """文章标题"""
        return self._title
    
    @title.setter
    def title(self, value: str):
        """设置文章标题"""
        if not value.strip():
            raise ValueError("标题不能为空")
        self._title = value.strip()
    
    @property
    def content(self) -> str:
        """文章内容"""
        return self._content
    
    @content.setter
    def content(self, value: str):
        """设置文章内容"""
        if not value.strip():
            raise ValueError("内容不能为空")
        self._content = value.strip()
    
    @property
    def author(self) -> str:
        """作者（只读）"""
        return self._author
    
    @property
    def tags(self) -> List[str]:
        """标签列表"""
        return self._tags.copy()  # 返回副本，防止外部修改
    
    @property
    def created_at(self) -> datetime.datetime:
        """创建时间（只读）"""
        return self._created_at
    
    @property
    def views(self) -> int:
        """浏览量（只读）"""
        return self._views
    
    @property
    def likes(self) -> int:
        """点赞数（只读）"""
        return self._likes
    
    # 实例方法
    def add_view(self) -> None:
        """增加浏览量"""
        self._views += 1
    
    def add_like(self) -> None:
        """增加点赞"""
        self._likes += 1
    
    def add_tag(self, tag: str) -> None:
        """添加标签"""
        tag = tag.strip()
        if tag and tag not in self._tags:
            self._tags.append(tag)
    
    def remove_tag(self, tag: str) -> bool:
        """移除标签"""
        try:
            self._tags.remove(tag)
            return True
        except ValueError:
            return False
    
    def has_tag(self, tag: str) -> bool:
        """检查是否包含指定标签"""
        return tag in self._tags
    
    def get_summary(self, max_length: int = 100) -> str:
        """获取文章摘要"""
        if len(self._content) <= max_length:
            return self._content
        return self._content[:max_length] + "..."
    
    def search_content(self, keyword: str) -> bool:
        """在标题和内容中搜索关键词"""
        keyword = keyword.lower()
        return (keyword in self._title.lower() or 
                keyword in self._content.lower() or
                any(keyword in tag.lower() for tag in self._tags))
    
    # 特殊方法
    def __str__(self) -> str:
        """字符串表示（用户友好）"""
        return f"📝 {self._title} by {self._author}"
    
    def __repr__(self) -> str:
        """字符串表示（开发者友好）"""
        return f"Article(id={self._id}, title='{self._title}', author='{self._author}')"
    
    def __len__(self) -> int:
        """返回内容长度"""
        return len(self._content)
    
    def __contains__(self, keyword: str) -> bool:
        """支持 'keyword' in article 语法"""
        return self.search_content(keyword)
    
    def __eq__(self, other) -> bool:
        """相等性比较"""
        if not isinstance(other, Article):
            return False
        return self._id == other._id
    
    def __lt__(self, other) -> bool:
        """小于比较（按创建时间）"""
        if not isinstance(other, Article):
            return NotImplemented
        return self._created_at < other._created_at
    
    # 类方法
    @classmethod
    def get_article_count(cls) -> int:
        """获取文章总数"""
        return cls._article_count
    
    @classmethod
    def reset_counter(cls) -> None:
        """重置计数器（测试用）"""
        cls._article_count = 0

class User:
    """用户类"""
    
    def __init__(self, username: str, email: str):
        """
        初始化用户
        
        Args:
            username: 用户名
            email: 邮箱
        """
        if not username.strip():
            raise ValueError("用户名不能为空")
        if not email.strip() or "@" not in email:
            raise ValueError("邮箱格式不正确")
        
        self._username = username.strip()
        self._email = email.strip()
        self._created_at = datetime.datetime.now()
        self._articles: List[Article] = []
    
    @property
    def username(self) -> str:
        """用户名（只读）"""
        return self._username
    
    @property
    def email(self) -> str:
        """邮箱"""
        return self._email
    
    @email.setter
    def email(self, value: str):
        """设置邮箱"""
        if not value.strip() or "@" not in value:
            raise ValueError("邮箱格式不正确")
        self._email = value.strip()
    
    @property
    def created_at(self) -> datetime.datetime:
        """注册时间（只读）"""
        return self._created_at
    
    @property
    def articles(self) -> List[Article]:
        """用户文章列表（只读）"""
        return self._articles.copy()
    
    def create_article(self, title: str, content: str, tags: Optional[List[str]] = None) -> Article:
        """创建文章"""
        article = Article(title, content, self._username, tags)
        self._articles.append(article)
        return article
    
    def get_article_count(self) -> int:
        """获取文章数量"""
        return len(self._articles)
    
    def get_total_views(self) -> int:
        """获取总浏览量"""
        return sum(article.views for article in self._articles)
    
    def get_popular_articles(self, limit: int = 5) -> List[Article]:
        """获取热门文章"""
        return sorted(self._articles, key=lambda x: x.views, reverse=True)[:limit]
    
    def __str__(self) -> str:
        return f"👤 {self._username} ({len(self._articles)} 篇文章)"
    
    def __repr__(self) -> str:
        return f"User(username='{self._username}', email='{self._email}')"

class Tag:
    """标签类"""
    
    def __init__(self, name: str):
        """初始化标签"""
        if not name.strip():
            raise ValueError("标签名不能为空")
        
        self._name = name.strip()
        self._usage_count = 0
    
    @property
    def name(self) -> str:
        """标签名（只读）"""
        return self._name
    
    @property
    def usage_count(self) -> int:
        """使用次数（只读）"""
        return self._usage_count
    
    def increment_usage(self) -> None:
        """增加使用次数"""
        self._usage_count += 1
    
    def __str__(self) -> str:
        return f"🏷️ {self._name} ({self._usage_count})"
    
    def __repr__(self) -> str:
        return f"Tag(name='{self._name}', usage_count={self._usage_count})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Tag):
            return False
        return self._name == other._name
    
    def __hash__(self) -> int:
        return hash(self._name)

class BlogManager:
    """博客管理器类"""
    
    def __init__(self):
        """初始化博客管理器"""
        self._articles: List[Article] = []
        self._users: List[User] = []
        self._tags: dict[str, Tag] = {}
    
    def add_user(self, username: str, email: str) -> User:
        """添加用户"""
        # 检查用户名是否已存在
        if any(user.username == username for user in self._users):
            raise ValueError(f"用户名 '{username}' 已存在")
        
        user = User(username, email)
        self._users.append(user)
        return user
    
    def get_user(self, username: str) -> Optional[User]:
        """获取用户"""
        for user in self._users:
            if user.username == username:
                return user
        return None
    
    def add_article(self, article: Article) -> None:
        """添加文章"""
        self._articles.append(article)
        
        # 更新标签统计
        for tag_name in article.tags:
            if tag_name not in self._tags:
                self._tags[tag_name] = Tag(tag_name)
            self._tags[tag_name].increment_usage()
    
    def get_all_articles(self) -> List[Article]:
        """获取所有文章"""
        return self._articles.copy()
    
    def search_articles(self, keyword: str) -> List[Article]:
        """搜索文章"""
        return [article for article in self._articles if keyword in article]
    
    def get_articles_by_tag(self, tag: str) -> List[Article]:
        """按标签获取文章"""
        return [article for article in self._articles if article.has_tag(tag)]
    
    def get_popular_tags(self, limit: int = 10) -> List[Tag]:
        """获取热门标签"""
        return sorted(self._tags.values(), key=lambda x: x.usage_count, reverse=True)[:limit]
    
    def get_statistics(self) -> dict:
        """获取统计信息"""
        total_articles = len(self._articles)
        total_views = sum(article.views for article in self._articles)
        total_users = len(self._users)
        
        return {
            "total_articles": total_articles,
            "total_views": total_views,
            "total_users": total_users,
            "average_views": total_views / total_articles if total_articles > 0 else 0,
            "total_tags": len(self._tags)
        }
    
    def __len__(self) -> int:
        """返回文章总数"""
        return len(self._articles)
    
    def __str__(self) -> str:
        stats = self.get_statistics()
        return f"📚 博客系统: {stats['total_articles']} 篇文章, {stats['total_users']} 个用户"
