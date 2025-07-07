#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库工具和管理功能
"""

import os
import json
from datetime import datetime
from flask import Flask
from models import db, User, Article, Tag, Comment, init_db
from config import get_config

class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """初始化应用"""
        self.app = app
        init_db(app)
    
    def create_tables(self):
        """创建所有表"""
        with self.app.app_context():
            db.create_all()
            print("✅ 数据库表创建完成")
    
    def drop_tables(self):
        """删除所有表"""
        with self.app.app_context():
            db.drop_all()
            print("✅ 数据库表删除完成")
    
    def reset_database(self):
        """重置数据库"""
        self.drop_tables()
        self.create_tables()
        print("✅ 数据库重置完成")
    
    def backup_database(self, backup_file=None):
        """备份数据库到JSON文件"""
        if not backup_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = f'backup_{timestamp}.json'
        
        with self.app.app_context():
            backup_data = {
                'users': [user.to_dict() for user in User.query.all()],
                'tags': [tag.to_dict() for tag in Tag.query.all()],
                'articles': [article.to_dict(include_content=True) for article in Article.query.all()],
                'comments': [comment.to_dict() for comment in Comment.query.all()],
                'backup_time': datetime.now().isoformat()
            }
            
            os.makedirs('backups', exist_ok=True)
            backup_path = os.path.join('backups', backup_file)
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 数据库备份完成: {backup_path}")
            return backup_path
    
    def get_statistics(self):
        """获取数据库统计信息"""
        with self.app.app_context():
            stats = {
                'users': {
                    'total': User.query.count(),
                    'active': User.query.filter_by(is_active=True).count()
                },
                'articles': {
                    'total': Article.query.count(),
                    'published': Article.query.filter_by(is_published=True).count(),
                    'drafts': Article.query.filter_by(is_published=False).count()
                },
                'tags': {
                    'total': Tag.query.count(),
                    'used': Tag.query.filter(Tag.usage_count > 0).count()
                },
                'comments': {
                    'total': Comment.query.count(),
                    'approved': Comment.query.filter_by(is_approved=True).count(),
                    'pending': Comment.query.filter_by(is_approved=False).count()
                }
            }
            return stats
    
    def print_statistics(self):
        """打印数据库统计信息"""
        stats = self.get_statistics()
        
        print("\n📊 数据库统计信息:")
        print(f"   用户: {stats['users']['total']} 总计, {stats['users']['active']} 活跃")
        print(f"   文章: {stats['articles']['total']} 总计, {stats['articles']['published']} 已发布, {stats['articles']['drafts']} 草稿")
        print(f"   标签: {stats['tags']['total']} 总计, {stats['tags']['used']} 已使用")
        print(f"   评论: {stats['comments']['total']} 总计, {stats['comments']['approved']} 已审核, {stats['comments']['pending']} 待审核")

class QueryHelper:
    """查询助手类"""
    
    @staticmethod
    def get_popular_articles(limit=10):
        """获取热门文章"""
        return Article.query.filter_by(is_published=True)\
            .order_by(Article.views.desc())\
            .limit(limit).all()
    
    @staticmethod
    def get_recent_articles(limit=10):
        """获取最新文章"""
        return Article.query.filter_by(is_published=True)\
            .order_by(Article.created_at.desc())\
            .limit(limit).all()
    
    @staticmethod
    def get_articles_by_tag(tag_name, limit=None):
        """根据标签获取文章"""
        query = Article.query.join(Article.tags)\
            .filter(Tag.name == tag_name)\
            .filter(Article.is_published == True)\
            .order_by(Article.created_at.desc())
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    @staticmethod
    def get_articles_by_author(username, limit=None):
        """根据作者获取文章"""
        query = Article.query.join(Article.author)\
            .filter(User.username == username)\
            .filter(Article.is_published == True)\
            .order_by(Article.created_at.desc())
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    @staticmethod
    def search_articles(keyword, limit=None):
        """搜索文章"""
        search_term = f"%{keyword}%"
        query = Article.query.filter_by(is_published=True)\
            .filter(
                Article.title.like(search_term) |
                Article.content.like(search_term)
            )\
            .order_by(Article.created_at.desc())
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    @staticmethod
    def get_popular_tags(limit=10):
        """获取热门标签"""
        return Tag.query.filter(Tag.usage_count > 0)\
            .order_by(Tag.usage_count.desc())\
            .limit(limit).all()
    
    @staticmethod
    def get_recent_comments(limit=10):
        """获取最新评论"""
        return Comment.query.filter_by(is_approved=True)\
            .order_by(Comment.created_at.desc())\
            .limit(limit).all()

def create_app(config_name='development'):
    """创建Flask应用"""
    app = Flask(__name__)
    
    # 加载配置
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    
    # 确保实例目录存在
    os.makedirs(os.path.join(app.instance_path), exist_ok=True)
    
    # 初始化数据库
    db_manager = DatabaseManager(app)
    
    # 注册数据库管理器到应用
    app.db_manager = db_manager
    
    return app

if __name__ == '__main__':
    # 创建应用并测试数据库连接
    app = create_app()
    
    with app.app_context():
        # 创建表
        db.create_all()
        
        # 打印统计信息
        app.db_manager.print_statistics()
        
        # 测试查询
        print("\n🔍 测试查询:")
        popular_articles = QueryHelper.get_popular_articles(5)
        print(f"   热门文章: {len(popular_articles)} 篇")
        
        recent_articles = QueryHelper.get_recent_articles(5)
        print(f"   最新文章: {len(recent_articles)} 篇")
        
        popular_tags = QueryHelper.get_popular_tags(5)
        print(f"   热门标签: {len(popular_tags)} 个")
        
        print("\n✅ 数据库测试完成")
