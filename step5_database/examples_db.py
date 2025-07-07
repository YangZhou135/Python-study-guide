#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库操作示例
演示SQLAlchemy的各种用法
"""

from database import create_app, QueryHelper
from models import db, User, Article, Tag, Comment
from datetime import datetime, timedelta

def basic_queries_example(app):
    """基础查询示例"""
    print("\n🔍 基础查询示例:")
    
    with app.app_context():
        # 1. 查询所有用户
        users = User.query.all()
        print(f"   所有用户数量: {len(users)}")
        
        # 2. 条件查询
        admin = User.query.filter_by(username='admin').first()
        print(f"   管理员用户: {admin.username if admin else '未找到'}")
        
        # 3. 复杂条件查询
        active_users = User.query.filter(User.is_active == True).all()
        print(f"   活跃用户数量: {len(active_users)}")
        
        # 4. 排序查询
        recent_users = User.query.order_by(User.created_at.desc()).limit(3).all()
        print(f"   最新注册用户: {[u.username for u in recent_users]}")
        
        # 5. 计数查询
        user_count = User.query.count()
        print(f"   用户总数: {user_count}")

def relationship_queries_example(app):
    """关系查询示例"""
    print("\n🔗 关系查询示例:")
    
    with app.app_context():
        # 1. 一对多关系查询
        admin = User.query.filter_by(username='admin').first()
        if admin:
            articles = admin.articles.all()
            print(f"   {admin.username} 的文章数量: {len(articles)}")
        
        # 2. 反向关系查询
        article = Article.query.first()
        if article:
            print(f"   文章 '{article.title}' 的作者: {article.author.username}")
        
        # 3. 多对多关系查询
        python_tag = Tag.query.filter_by(name='Python').first()
        if python_tag:
            articles = python_tag.articles.all()
            print(f"   标签 'Python' 的文章数量: {len(articles)}")
        
        # 4. 关联查询 (JOIN)
        articles_with_authors = db.session.query(Article, User)\
            .join(User, Article.author_id == User.id)\
            .filter(Article.is_published == True)\
            .all()
        print(f"   已发布文章及作者: {len(articles_with_authors)} 条记录")

def advanced_queries_example(app):
    """高级查询示例"""
    print("\n🚀 高级查询示例:")
    
    with app.app_context():
        # 1. 聚合查询
        from sqlalchemy import func
        
        # 统计每个用户的文章数量
        user_article_counts = db.session.query(
            User.username,
            func.count(Article.id).label('article_count')
        ).outerjoin(Article).group_by(User.id).all()
        
        print("   用户文章统计:")
        for username, count in user_article_counts:
            print(f"     {username}: {count} 篇")
        
        # 2. 子查询
        # 查找有文章的用户
        users_with_articles = User.query.filter(
            User.id.in_(
                db.session.query(Article.author_id).distinct()
            )
        ).all()
        print(f"   有文章的用户数量: {len(users_with_articles)}")
        
        # 3. 条件聚合
        popular_articles = db.session.query(Article)\
            .filter(Article.views > 20)\
            .order_by(Article.views.desc())\
            .all()
        print(f"   热门文章 (浏览量>20): {len(popular_articles)} 篇")
        
        # 4. 日期范围查询
        recent_date = datetime.utcnow() - timedelta(days=7)
        recent_articles = Article.query.filter(
            Article.created_at >= recent_date
        ).all()
        print(f"   最近7天的文章: {len(recent_articles)} 篇")

def crud_operations_example(app):
    """CRUD操作示例"""
    print("\n✏️  CRUD操作示例:")
    
    with app.app_context():
        # Create - 创建
        print("   创建操作:")
        new_user = User(
            username='test_user',
            email='test@example.com',
            password='test123'
        )
        db.session.add(new_user)
        db.session.commit()
        print(f"     创建用户: {new_user.username}")
        
        # Read - 读取
        print("   读取操作:")
        user = User.query.filter_by(username='test_user').first()
        print(f"     读取用户: {user.username if user else '未找到'}")
        
        # Update - 更新
        print("   更新操作:")
        if user:
            user.email = 'updated@example.com'
            db.session.commit()
            print(f"     更新用户邮箱: {user.email}")
        
        # Delete - 删除
        print("   删除操作:")
        if user:
            db.session.delete(user)
            db.session.commit()
            print(f"     删除用户: test_user")

def transaction_example(app):
    """事务操作示例"""
    print("\n💾 事务操作示例:")
    
    with app.app_context():
        try:
            # 开始事务
            print("   开始事务...")
            
            # 创建用户
            user = User(
                username='transaction_user',
                email='transaction@example.com',
                password='test123'
            )
            db.session.add(user)
            db.session.flush()  # 获取用户ID但不提交
            
            # 创建文章
            article = Article(
                title='事务测试文章',
                content='这是一篇测试事务的文章',
                author_id=user.id
            )
            db.session.add(article)
            
            # 提交事务
            db.session.commit()
            print("   事务提交成功")
            
            # 清理测试数据
            db.session.delete(article)
            db.session.delete(user)
            db.session.commit()
            print("   清理测试数据完成")
            
        except Exception as e:
            # 回滚事务
            db.session.rollback()
            print(f"   事务回滚: {e}")

def pagination_example(app):
    """分页查询示例"""
    print("\n📄 分页查询示例:")
    
    with app.app_context():
        # 分页查询文章
        page = 1
        per_page = 3
        
        articles = Article.query.filter_by(is_published=True)\
            .order_by(Article.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        print(f"   第 {page} 页，每页 {per_page} 条:")
        print(f"   总数: {articles.total}")
        print(f"   总页数: {articles.pages}")
        print(f"   当前页文章:")
        
        for article in articles.items:
            print(f"     - {article.title}")

def query_helper_example(app):
    """查询助手示例"""
    print("\n🛠️  查询助手示例:")
    
    with app.app_context():
        # 使用查询助手
        popular_articles = QueryHelper.get_popular_articles(3)
        print(f"   热门文章 (前3篇):")
        for article in popular_articles:
            print(f"     - {article.title} (浏览量: {article.views})")
        
        recent_articles = QueryHelper.get_recent_articles(3)
        print(f"   最新文章 (前3篇):")
        for article in recent_articles:
            print(f"     - {article.title}")
        
        popular_tags = QueryHelper.get_popular_tags(5)
        print(f"   热门标签 (前5个):")
        for tag in popular_tags:
            print(f"     - {tag.name} (使用次数: {tag.usage_count})")
        
        # 搜索文章
        search_results = QueryHelper.search_articles('Python', 3)
        print(f"   搜索 'Python' 的结果:")
        for article in search_results:
            print(f"     - {article.title}")

def performance_example(app):
    """性能优化示例"""
    print("\n⚡ 性能优化示例:")
    
    with app.app_context():
        import time
        
        # 1. 预加载关系数据 (避免N+1查询)
        start_time = time.time()
        
        # 不好的方式 - 会产生N+1查询
        articles = Article.query.filter_by(is_published=True).all()
        authors = [article.author.username for article in articles]  # 每次访问都会查询数据库
        
        end_time = time.time()
        print(f"   N+1查询耗时: {end_time - start_time:.4f} 秒")
        
        # 好的方式 - 使用joinedload预加载
        from sqlalchemy.orm import joinedload
        
        start_time = time.time()
        articles = Article.query.options(joinedload(Article.author))\
            .filter_by(is_published=True).all()
        authors = [article.author.username for article in articles]  # 不会产生额外查询
        
        end_time = time.time()
        print(f"   预加载查询耗时: {end_time - start_time:.4f} 秒")
        
        # 2. 批量操作
        print("   批量操作示例:")
        
        # 批量更新
        Article.query.filter_by(is_published=True)\
            .update({'updated_at': datetime.utcnow()})
        db.session.commit()
        print("     批量更新文章时间完成")

def main():
    """主函数"""
    print("🚀 SQLAlchemy数据库操作示例")
    
    # 创建应用
    app = create_app()
    
    # 运行示例
    basic_queries_example(app)
    relationship_queries_example(app)
    advanced_queries_example(app)
    crud_operations_example(app)
    transaction_example(app)
    pagination_example(app)
    query_helper_example(app)
    performance_example(app)
    
    print("\n✅ 所有示例运行完成！")

if __name__ == '__main__':
    main()
