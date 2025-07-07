#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask博客应用 - 数据库版本
使用SQLAlchemy进行数据持久化
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime
import math

from database import create_app, DatabaseManager, QueryHelper
from models import db, User, Article, Tag, Comment
from config import get_config

# 创建应用实例
app = create_app()

# 路由定义
@app.route('/')
def index():
    """首页"""
    page = request.args.get('page', 1, type=int)
    per_page = app.config.get('POSTS_PER_PAGE', 10)
    
    # 分页查询已发布文章
    articles = Article.query.filter_by(is_published=True)\
        .order_by(Article.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    # 获取热门标签
    popular_tags = QueryHelper.get_popular_tags(10)
    
    # 获取最新评论
    recent_comments = QueryHelper.get_recent_comments(5)
    
    return render_template('index.html',
                         articles=articles,
                         popular_tags=popular_tags,
                         recent_comments=recent_comments)

@app.route('/article/<int:article_id>')
def article_detail(article_id):
    """文章详情"""
    article = Article.query.get_or_404(article_id)
    
    # 检查文章是否已发布
    if not article.is_published and session.get('user_id') != article.author_id:
        abort(404)
    
    # 增加浏览量
    article.add_view()
    
    # 获取评论
    page = request.args.get('page', 1, type=int)
    per_page = app.config.get('COMMENTS_PER_PAGE', 20)
    
    comments = Comment.query.filter_by(article_id=article_id, is_approved=True)\
        .order_by(Comment.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    # 获取相关文章
    related_articles = []
    if article.tags:
        related_articles = Article.query.join(Article.tags)\
            .filter(Tag.id.in_([tag.id for tag in article.tags]))\
            .filter(Article.id != article_id)\
            .filter(Article.is_published == True)\
            .limit(5).all()
    
    return render_template('article_detail.html',
                         article=article,
                         comments=comments,
                         related_articles=related_articles)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            user.login()  # 记录登录
            flash('登录成功！', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('用户名或密码错误', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # 检查用户是否已存在
        if User.query.filter_by(username=username).first():
            flash('用户名已存在', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('邮箱已被注册', 'error')
            return render_template('register.html')
        
        # 创建新用户
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        
        flash('注册成功！请登录', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """用户登出"""
    session.clear()
    flash('已退出登录', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    """用户仪表板"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    
    # 获取用户文章
    articles = Article.query.filter_by(author_id=user.id)\
        .order_by(Article.created_at.desc()).all()
    
    # 获取统计信息
    stats = {
        'total_articles': len(articles),
        'published_articles': len([a for a in articles if a.is_published]),
        'draft_articles': len([a for a in articles if not a.is_published]),
        'total_views': sum(a.views for a in articles),
        'total_likes': sum(a.likes for a in articles),
        'total_comments': sum(a.comment_count for a in articles)
    }
    
    return render_template('dashboard.html', user=user, articles=articles, stats=stats)

@app.route('/write', methods=['GET', 'POST'])
def write_article():
    """写文章"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        tags = request.form.get('tags', '').split(',')
        is_published = 'publish' in request.form
        
        # 创建文章
        article = Article(
            title=title,
            content=content,
            author_id=session['user_id']
        )
        article.is_published = is_published
        
        # 添加标签
        for tag_name in tags:
            tag_name = tag_name.strip()
            if tag_name:
                article.add_tag(tag_name)
        
        db.session.add(article)
        db.session.commit()
        
        flash('文章保存成功！', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('write_article.html')

@app.route('/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    """编辑文章"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    article = Article.query.get_or_404(article_id)
    
    # 检查权限
    if article.author_id != session['user_id']:
        abort(403)
    
    if request.method == 'POST':
        article.title = request.form.get('title')
        article.content = request.form.get('content')
        article.is_published = 'publish' in request.form
        article.updated_at = datetime.utcnow()
        
        # 更新标签
        new_tags = request.form.get('tags', '').split(',')
        
        # 移除旧标签
        for tag in article.tags[:]:
            article.remove_tag(tag.name)
        
        # 添加新标签
        for tag_name in new_tags:
            tag_name = tag_name.strip()
            if tag_name:
                article.add_tag(tag_name)
        
        db.session.commit()
        flash('文章更新成功！', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('edit_article.html', article=article)

@app.route('/search')
def search():
    """搜索文章"""
    keyword = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    per_page = app.config.get('POSTS_PER_PAGE', 10)
    
    if keyword:
        # 搜索文章
        search_term = f"%{keyword}%"
        articles = Article.query.filter_by(is_published=True)\
            .filter(
                Article.title.like(search_term) |
                Article.content.like(search_term)
            )\
            .order_by(Article.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
    else:
        articles = None
    
    return render_template('search.html', articles=articles, keyword=keyword)

@app.route('/tag/<tag_name>')
def articles_by_tag(tag_name):
    """按标签查看文章"""
    tag = Tag.query.filter_by(name=tag_name).first_or_404()
    
    page = request.args.get('page', 1, type=int)
    per_page = app.config.get('POSTS_PER_PAGE', 10)
    
    articles = Article.query.join(Article.tags)\
        .filter(Tag.name == tag_name)\
        .filter(Article.is_published == True)\
        .order_by(Article.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('articles_by_tag.html', articles=articles, tag=tag)

@app.route('/api/like/<int:article_id>', methods=['POST'])
def like_article(article_id):
    """点赞文章"""
    article = Article.query.get_or_404(article_id)
    article.add_like()
    return jsonify({'likes': article.likes})

@app.route('/api/comment', methods=['POST'])
def add_comment():
    """添加评论"""
    if 'user_id' not in session:
        return jsonify({'error': '请先登录'}), 401
    
    article_id = request.json.get('article_id')
    content = request.json.get('content')
    
    if not content or not content.strip():
        return jsonify({'error': '评论内容不能为空'}), 400
    
    comment = Comment(
        content=content.strip(),
        article_id=article_id,
        author_id=session['user_id']
    )
    
    db.session.add(comment)
    db.session.commit()
    
    return jsonify({
        'id': comment.id,
        'content': comment.content,
        'author': comment.author.username,
        'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
    })

# 模板上下文处理器
@app.context_processor
def inject_common_data():
    """注入通用模板数据"""
    return {
        'current_user': User.query.get(session.get('user_id')) if 'user_id' in session else None,
        'popular_tags': QueryHelper.get_popular_tags(10)
    }

# 错误处理
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        # 创建数据库表
        db.create_all()
        
        # 打印统计信息
        app.db_manager.print_statistics()
    
    print("\n🌐 Flask博客应用 (数据库版) 启动中...")
    print("🔗 访问地址: http://127.0.0.1:5000")
    print("💡 使用 Ctrl+C 停止服务器")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
