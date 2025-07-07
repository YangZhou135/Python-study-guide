#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据迁移脚本
从文件存储迁移到数据库存储
"""

import os
import sys
import json
import argparse
from datetime import datetime
from database import create_app
from models import db, User, Article, Tag, Comment

class DataMigrator:
    """数据迁移器"""
    
    def __init__(self, app):
        self.app = app
        self.stats = {
            'users': {'migrated': 0, 'skipped': 0, 'errors': 0},
            'articles': {'migrated': 0, 'skipped': 0, 'errors': 0},
            'tags': {'migrated': 0, 'skipped': 0, 'errors': 0},
            'comments': {'migrated': 0, 'skipped': 0, 'errors': 0}
        }
    
    def migrate_from_files(self, source_dir='../step4_web/data'):
        """从文件存储迁移数据"""
        print("🚀 开始从文件存储迁移数据...")
        
        with self.app.app_context():
            # 清空现有数据
            if self._confirm_clear_database():
                self._clear_database()
            
            # 迁移用户数据
            self._migrate_users(source_dir)
            
            # 迁移文章数据
            self._migrate_articles(source_dir)
            
            # 打印迁移统计
            self._print_migration_stats()
    
    def _confirm_clear_database(self):
        """确认清空数据库"""
        response = input("⚠️  是否清空现有数据库数据? (y/N): ")
        return response.lower() in ['y', 'yes']
    
    def _clear_database(self):
        """清空数据库"""
        print("🧹 清空现有数据...")
        Comment.query.delete()
        Article.query.delete()
        Tag.query.delete()
        User.query.delete()
        db.session.commit()
        print("✅ 数据库已清空")
    
    def _migrate_users(self, source_dir):
        """迁移用户数据"""
        users_file = os.path.join(source_dir, 'web_users.json')
        if not os.path.exists(users_file):
            print(f"⚠️  用户文件不存在: {users_file}")
            return
        
        print("📥 迁移用户数据...")
        
        try:
            with open(users_file, 'r', encoding='utf-8') as f:
                users_data = json.load(f)
            
            for user_data in users_data:
                try:
                    # 检查用户是否已存在
                    existing_user = User.query.filter_by(username=user_data['username']).first()
                    if existing_user:
                        self.stats['users']['skipped'] += 1
                        continue
                    
                    # 创建新用户
                    user = User(
                        username=user_data['username'],
                        email=user_data['email']
                    )
                    
                    # 设置密码哈希
                    user.password_hash = user_data.get('password_hash', '')
                    
                    # 设置其他属性
                    if 'created_at' in user_data:
                        user.created_at = datetime.fromisoformat(user_data['created_at'])
                    if 'last_login' in user_data and user_data['last_login']:
                        user.last_login = datetime.fromisoformat(user_data['last_login'])
                    if 'login_count' in user_data:
                        user.login_count = user_data['login_count']
                    
                    db.session.add(user)
                    self.stats['users']['migrated'] += 1
                    
                except Exception as e:
                    print(f"❌ 迁移用户失败 {user_data.get('username', 'Unknown')}: {e}")
                    self.stats['users']['errors'] += 1
            
            db.session.commit()
            print(f"✅ 用户迁移完成: {self.stats['users']['migrated']} 个")
            
        except Exception as e:
            print(f"❌ 读取用户文件失败: {e}")
    
    def _migrate_articles(self, source_dir):
        """迁移文章数据"""
        articles_file = os.path.join(source_dir, 'web_articles.json')
        if not os.path.exists(articles_file):
            print(f"⚠️  文章文件不存在: {articles_file}")
            return
        
        print("📥 迁移文章数据...")
        
        try:
            with open(articles_file, 'r', encoding='utf-8') as f:
                articles_data = json.load(f)
            
            for article_data in articles_data:
                try:
                    # 查找作者
                    author = User.query.filter_by(username=article_data['author']).first()
                    if not author:
                        print(f"⚠️  找不到作者: {article_data['author']}")
                        self.stats['articles']['errors'] += 1
                        continue
                    
                    # 检查文章是否已存在
                    existing_article = Article.query.filter_by(title=article_data['title']).first()
                    if existing_article:
                        self.stats['articles']['skipped'] += 1
                        continue
                    
                    # 创建文章
                    article = Article(
                        title=article_data['title'],
                        content=article_data['content'],
                        author_id=author.id
                    )
                    
                    # 设置其他属性
                    article.is_published = article_data.get('is_published', False)
                    article.views = article_data.get('views', 0)
                    article.likes = article_data.get('likes', 0)
                    
                    if 'created_at' in article_data:
                        article.created_at = datetime.fromisoformat(article_data['created_at'])
                    if 'updated_at' in article_data:
                        article.updated_at = datetime.fromisoformat(article_data['updated_at'])
                    
                    db.session.add(article)
                    db.session.flush()  # 获取文章ID
                    
                    # 处理标签
                    if 'tags' in article_data:
                        for tag_name in article_data['tags']:
                            tag = Tag.query.filter_by(name=tag_name).first()
                            if not tag:
                                tag = Tag(name=tag_name)
                                db.session.add(tag)
                                self.stats['tags']['migrated'] += 1
                            
                            if tag not in article.tags:
                                article.tags.append(tag)
                                tag.usage_count += 1
                    
                    # 处理评论
                    if 'comments' in article_data:
                        for comment_data in article_data['comments']:
                            try:
                                # 查找评论作者
                                comment_author = User.query.filter_by(username=comment_data['author']).first()
                                if not comment_author:
                                    print(f"⚠️  找不到评论作者: {comment_data['author']}")
                                    continue
                                
                                comment = Comment(
                                    content=comment_data['content'],
                                    article_id=article.id,
                                    author_id=comment_author.id
                                )
                                
                                if 'created_at' in comment_data:
                                    comment.created_at = datetime.fromisoformat(comment_data['created_at'])
                                if 'is_approved' in comment_data:
                                    comment.is_approved = comment_data['is_approved']
                                
                                db.session.add(comment)
                                self.stats['comments']['migrated'] += 1
                                
                            except Exception as e:
                                print(f"❌ 迁移评论失败: {e}")
                                self.stats['comments']['errors'] += 1
                    
                    self.stats['articles']['migrated'] += 1
                    
                except Exception as e:
                    print(f"❌ 迁移文章失败 {article_data.get('title', 'Unknown')}: {e}")
                    self.stats['articles']['errors'] += 1
            
            db.session.commit()
            print(f"✅ 文章迁移完成: {self.stats['articles']['migrated']} 篇")
            
        except Exception as e:
            print(f"❌ 读取文章文件失败: {e}")
    
    def _print_migration_stats(self):
        """打印迁移统计"""
        print("\n📊 迁移统计:")
        for entity_type, stats in self.stats.items():
            total = stats['migrated'] + stats['skipped'] + stats['errors']
            if total > 0:
                print(f"   {entity_type}: {stats['migrated']} 迁移, {stats['skipped']} 跳过, {stats['errors']} 错误")
        
        print("\n✅ 数据迁移完成!")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='数据迁移工具')
    parser.add_argument('--from-files', action='store_true', help='从文件存储迁移')
    parser.add_argument('--source-dir', default='../step4_web/data', help='源数据目录')
    parser.add_argument('--config', default='development', help='配置环境')
    
    args = parser.parse_args()
    
    if not args.from_files:
        print("请指定迁移类型，例如: --from-files")
        return
    
    # 创建应用
    app = create_app(args.config)
    
    # 创建迁移器
    migrator = DataMigrator(app)
    
    # 执行迁移
    if args.from_files:
        migrator.migrate_from_files(args.source_dir)

if __name__ == '__main__':
    main()
