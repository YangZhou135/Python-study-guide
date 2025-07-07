#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask Web博客应用
基于Flask框架的博客管理系统
"""

import os
import secrets
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename
from config import config
from models import WebBlogManager, WebUser, WebArticle
from forms import LoginForm, RegisterForm, ArticleForm, CommentForm, SearchForm, ProfileForm

def create_app(config_name='default'):
    """应用工厂函数"""
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config[config_name])
    
    # 确保必要的目录存在
    os.makedirs(app.config['DATA_DIR'], exist_ok=True)
    os.makedirs(app.config['UPLOAD_DIR'], exist_ok=True)
    
    # 初始化博客管理器
    blog_manager = WebBlogManager()
    
    # 工具函数
    def get_current_user():
        """获取当前登录用户"""
        if 'user_id' in session:
            return blog_manager.get_user(session['user_id'])
        return None
    
    def login_required(f):
        """登录装饰器"""
        from functools import wraps
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not get_current_user():
                flash('请先登录', 'warning')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    
    def save_uploaded_file(file):
        """保存上传的文件"""
        if file and file.filename:
            filename = secure_filename(file.filename)
            # 添加随机前缀避免文件名冲突
            filename = f"{secrets.token_hex(8)}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_DIR'], filename)
            file.save(file_path)
            return filename
        return None
    
    # 模板上下文处理器
    @app.context_processor
    def inject_user():
        """向模板注入当前用户"""
        return dict(current_user=get_current_user())
    
    @app.context_processor
    def inject_app_info():
        """向模板注入应用信息"""
        return dict(
            app_name=app.config['APP_NAME'],
            app_version=app.config['APP_VERSION']
        )
    
    # 路由定义
    @app.route('/')
    def index():
        """首页"""
        page = request.args.get('page', 1, type=int)
        per_page = app.config['ARTICLES_PER_PAGE']
        
        # 获取已发布的文章
        articles = blog_manager.get_published_articles()
        articles.sort(key=lambda x: x.created_at, reverse=True)
        
        # 简单分页
        start = (page - 1) * per_page
        end = start + per_page
        articles_page = articles[start:end]
        
        # 分页信息
        has_prev = page > 1
        has_next = end < len(articles)
        prev_num = page - 1 if has_prev else None
        next_num = page + 1 if has_next else None
        
        return render_template('index.html',
                             articles=articles_page,
                             has_prev=has_prev,
                             has_next=has_next,
                             prev_num=prev_num,
                             next_num=next_num)
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """用户登录"""
        if get_current_user():
            return redirect(url_for('index'))
        
        form = LoginForm()
        if form.validate_on_submit():
            user = blog_manager.authenticate_user(form.username.data, form.password.data)
            if user:
                session['user_id'] = user.username
                session.permanent = form.remember_me.data
                flash(f'欢迎回来，{user.username}！', 'success')
                
                # 重定向到之前访问的页面
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('index'))
            else:
                flash('用户名或密码错误', 'error')
        
        return render_template('login.html', form=form)
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """用户注册"""
        if get_current_user():
            return redirect(url_for('index'))
        
        form = RegisterForm()
        if form.validate_on_submit():
            user = blog_manager.register_user(
                form.username.data,
                form.email.data,
                form.password.data
            )
            if user:
                flash('注册成功！请登录', 'success')
                return redirect(url_for('login'))
            else:
                flash('用户名或邮箱已存在', 'error')
        
        return render_template('register.html', form=form)
    
    @app.route('/logout')
    def logout():
        """用户登出"""
        session.pop('user_id', None)
        flash('您已成功登出', 'info')
        return redirect(url_for('index'))
    
    @app.route('/article/<int:article_id>')
    def article_detail(article_id):
        """文章详情"""
        article = blog_manager.get_article(article_id)
        if not article or not isinstance(article, WebArticle):
            flash('文章不存在', 'error')
            return redirect(url_for('index'))
        
        # 只有已发布的文章或作者本人可以查看
        current_user = get_current_user()
        if not article.is_published and (not current_user or current_user.username != article.author):
            flash('文章不存在', 'error')
            return redirect(url_for('index'))
        
        # 增加浏览量
        article.add_view()
        blog_manager._save_web_data()
        
        # 评论表单
        comment_form = CommentForm()
        
        return render_template('article_detail.html', 
                             article=article, 
                             comment_form=comment_form)
    
    @app.route('/article/<int:article_id>/comment', methods=['POST'])
    @login_required
    def add_comment(article_id):
        """添加评论"""
        form = CommentForm()
        if form.validate_on_submit():
            current_user = get_current_user()
            comment = blog_manager.add_comment(
                article_id,
                form.content.data,
                current_user.username
            )
            if comment:
                flash('评论添加成功', 'success')
            else:
                flash('评论添加失败', 'error')
        else:
            flash('评论内容不能为空', 'error')
        
        return redirect(url_for('article_detail', article_id=article_id))
    
    @app.route('/write', methods=['GET', 'POST'])
    @login_required
    def write_article():
        """写文章"""
        form = ArticleForm()
        if form.validate_on_submit():
            current_user = get_current_user()
            
            # 处理上传的图片
            featured_image = None
            if form.featured_image.data:
                featured_image = save_uploaded_file(form.featured_image.data)
            
            # 处理标签
            tags = []
            if form.tags.data:
                tags = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()]
            
            # 创建文章
            article = blog_manager.create_article(
                title=form.title.data,
                content=form.content.data,
                author=current_user.username,
                tags=tags,
                summary=form.summary.data,
                featured_image=featured_image
            )
            
            # 是否立即发布
            if form.is_published.data:
                article.publish()
                blog_manager._save_web_data()
                flash('文章发布成功！', 'success')
            else:
                flash('文章保存为草稿', 'info')
            
            return redirect(url_for('article_detail', article_id=article.id))
        
        return render_template('article_form.html', form=form, title='写文章')
    
    @app.route('/article/<int:article_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_article(article_id):
        """编辑文章"""
        article = blog_manager.get_article(article_id)
        if not article or not isinstance(article, WebArticle):
            flash('文章不存在', 'error')
            return redirect(url_for('index'))
        
        current_user = get_current_user()
        if current_user.username != article.author:
            flash('您没有权限编辑此文章', 'error')
            return redirect(url_for('article_detail', article_id=article_id))
        
        form = ArticleForm()
        
        if form.validate_on_submit():
            # 更新文章信息
            article._title = form.title.data
            article._content = form.content.data
            article.summary = form.summary.data
            
            # 处理标签
            if form.tags.data:
                article._tags = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()]
            else:
                article._tags = []
            
            # 处理上传的图片
            if form.featured_image.data:
                featured_image = save_uploaded_file(form.featured_image.data)
                article.featured_image = featured_image
            
            # 更新发布状态
            if form.is_published.data:
                article.publish()
            else:
                article.unpublish()
            
            blog_manager._save_web_data()
            flash('文章更新成功！', 'success')
            return redirect(url_for('article_detail', article_id=article.id))
        
        # 预填充表单
        form.title.data = article.title
        form.content.data = article.content
        form.summary.data = article.summary
        form.tags.data = ', '.join(article.tags)
        form.is_published.data = article.is_published
        
        return render_template('article_form.html', form=form, title='编辑文章', article=article)
    
    @app.route('/search')
    def search():
        """搜索文章"""
        form = SearchForm()
        articles = []
        query = request.args.get('query', '').strip()
        
        if query:
            form.query.data = query
            articles = blog_manager.search_articles(query)
        
        return render_template('search.html', form=form, articles=articles, query=query)
    
    @app.route('/profile')
    @login_required
    def profile():
        """个人中心"""
        current_user = get_current_user()
        user_articles = blog_manager.get_articles_by_user(current_user.username)
        
        # 统计信息
        stats = {
            'total_articles': len(user_articles),
            'published_articles': len([a for a in user_articles if a.is_published]),
            'draft_articles': len([a for a in user_articles if not a.is_published]),
            'total_views': sum(a.views for a in user_articles),
            'total_likes': sum(a.likes for a in user_articles)
        }
        
        return render_template('profile.html', user=current_user, articles=user_articles, stats=stats)
    
    @app.route('/my-articles')
    @login_required
    def my_articles():
        """我的文章"""
        current_user = get_current_user()
        articles = blog_manager.get_articles_by_user(current_user.username)
        articles.sort(key=lambda x: x.created_at, reverse=True)
        
        return render_template('my_articles.html', articles=articles)
    
    @app.route('/api/article/<int:article_id>/like', methods=['POST'])
    @login_required
    def like_article(article_id):
        """点赞文章（API）"""
        article = blog_manager.get_article(article_id)
        if article:
            article.add_like()
            blog_manager._save_web_data()
            return jsonify({'success': True, 'likes': article.likes})
        return jsonify({'success': False}), 404
    
    # 错误处理
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500
    
    return app

def main():
    """主函数"""
    app = create_app('development')
    
    print("🌐 启动Flask Web博客应用")
    print("=" * 40)
    print(f"📱 应用名称: {app.config['APP_NAME']}")
    print(f"🔧 版本: {app.config['APP_VERSION']}")
    print(f"🌍 访问地址: http://localhost:5000")
    print(f"📁 数据目录: {app.config['DATA_DIR']}")
    print("=" * 40)
    print("💡 功能特性:")
    print("   ✅ 用户注册和登录")
    print("   ✅ 文章创建和编辑")
    print("   ✅ 评论系统")
    print("   ✅ 搜索功能")
    print("   ✅ 个人中心")
    print("   ✅ 响应式设计")
    print("=" * 40)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Web应用已停止")

if __name__ == "__main__":
    main()
