#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask应用主文件 - Stage 6 前后端集成
提供完整的REST API服务
"""

import os
from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# 导入配置
from config import get_config

# 导入数据库模型
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../step5_database'))
from models import db, User, Article, Comment, Tag

# 导入工具和中间件
from utils.response import error_response, internal_error_response
from utils.jwt_helper import TokenBlacklist
from middleware.auth import AuthMiddleware

# 导入API蓝图
from api.auth import auth_bp
from api.articles import articles_bp
from api.comments import comments_bp
from api.users import users_bp
from api.upload import upload_bp

def create_app(config_name=None):
    """
    应用工厂函数
    
    Args:
        config_name: 配置名称
    
    Returns:
        Flask: 配置好的Flask应用实例
    """
    app = Flask(__name__)
    
    # 加载配置
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    
    # 初始化配置
    config_class.init_app(app)
    
    # 初始化扩展
    init_extensions(app)
    
    # 注册蓝图
    register_blueprints(app)
    
    # 注册错误处理器
    register_error_handlers(app)
    
    # 注册CLI命令
    register_cli_commands(app)
    
    return app

def init_extensions(app):
    """初始化Flask扩展"""
    
    # 初始化数据库
    db.init_app(app)
    
    # 初始化CORS
    CORS(app, 
         origins=app.config['CORS_ORIGINS'],
         allow_headers=app.config['CORS_ALLOW_HEADERS'],
         methods=app.config['CORS_METHODS'],
         supports_credentials=True)
    
    # 初始化JWT
    jwt = JWTManager(app)
    
    # JWT错误处理
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return error_response('令牌已过期', status_code=401)
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        print(f"JWT无效令牌错误: {error}")
        return error_response('无效的令牌', status_code=401)
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        print(f"JWT缺少令牌错误: {error}")
        return error_response('缺少认证令牌', status_code=401)
    
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        return TokenBlacklist.is_token_revoked(jti)
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return error_response('令牌已被撤销', status_code=401)
    
    # 初始化限流器
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=[app.config['RATELIMIT_DEFAULT']],
        storage_uri=app.config['RATELIMIT_STORAGE_URL']
    )
    limiter.init_app(app)
    
    # 初始化认证中间件
    auth_middleware = AuthMiddleware(app)

def register_blueprints(app):
    """注册蓝图"""
    
    # API前缀
    api_prefix = app.config['API_PREFIX']
    
    # 注册认证API
    app.register_blueprint(auth_bp, url_prefix=f'{api_prefix}/auth')

    # 注册文章API
    app.register_blueprint(articles_bp, url_prefix=f'{api_prefix}/articles')

    # 注册评论API
    app.register_blueprint(comments_bp, url_prefix=f'{api_prefix}/comments')

    # 注册用户API
    app.register_blueprint(users_bp, url_prefix=f'{api_prefix}/users')

    # 注册上传API
    app.register_blueprint(upload_bp, url_prefix=f'{api_prefix}/upload')
    
    # 根路径
    @app.route('/')
    def index():
        return jsonify({
            'message': '个人博客管理系统 API',
            'version': app.config['API_VERSION'],
            'status': 'running',
            'endpoints': {
                'auth': f"{api_prefix}/auth",
                'articles': f"{api_prefix}/articles",
                'comments': f"{api_prefix}/comments",
                'users': f"{api_prefix}/users",
                'upload': f"{api_prefix}/upload",
                'docs': f"{api_prefix}/docs"
            }
        })
    
    # 健康检查
    @app.route(f'{api_prefix}/health')
    def health_check():
        try:
            # 测试数据库连接
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.utcnow().isoformat(),
                'database': 'connected'
            })
        except Exception as e:
            return jsonify({
                'status': 'unhealthy',
                'timestamp': datetime.utcnow().isoformat(),
                'database': 'disconnected',
                'error': str(e)
            }), 500
    
    # API文档 (简单版本)
    @app.route(f'{api_prefix}/docs')
    def api_docs():
        return jsonify({
            'title': '个人博客管理系统 API 文档',
            'version': app.config['API_VERSION'],
            'base_url': api_prefix,
            'authentication': 'JWT Bearer Token',
            'endpoints': {
                'auth': {
                    'POST /auth/register': '用户注册',
                    'POST /auth/login': '用户登录',
                    'POST /auth/refresh': '刷新令牌',
                    'POST /auth/logout': '用户登出',
                    'GET /auth/me': '获取当前用户信息',
                    'POST /auth/change-password': '修改密码'
                },
                'articles': {
                    'GET /articles': '获取文章列表',
                    'POST /articles': '创建文章',
                    'GET /articles/{id}': '获取文章详情',
                    'PUT /articles/{id}': '更新文章',
                    'DELETE /articles/{id}': '删除文章',
                    'POST /articles/{id}/like': '点赞文章',
                    'GET /articles/search': '搜索文章'
                }
            }
        })

def register_error_handlers(app):
    """注册错误处理器"""
    
    @app.errorhandler(400)
    def bad_request(error):
        return error_response('请求参数错误', status_code=400)
    
    @app.errorhandler(401)
    def unauthorized(error):
        return error_response('未授权访问', status_code=401)
    
    @app.errorhandler(403)
    def forbidden(error):
        return error_response('禁止访问', status_code=403)
    
    @app.errorhandler(404)
    def not_found(error):
        return error_response('资源不存在', status_code=404)
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return error_response('请求方法不允许', status_code=405)
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        return error_response('请求过于频繁，请稍后再试', status_code=429)
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return internal_error_response()
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.error(f'未处理的异常: {str(error)}', exc_info=True)
        db.session.rollback()
        return internal_error_response()

def register_cli_commands(app):
    """注册CLI命令"""
    
    @app.cli.command()
    def init_db():
        """初始化数据库"""
        db.create_all()
        print('✅ 数据库初始化完成')
    
    @app.cli.command()
    def create_admin():
        """创建管理员用户"""
        username = input('管理员用户名: ')
        email = input('管理员邮箱: ')
        password = input('管理员密码: ')
        
        # 检查用户是否已存在
        if User.query.filter_by(username=username).first():
            print('❌ 用户名已存在')
            return
        
        if User.query.filter_by(email=email).first():
            print('❌ 邮箱已被注册')
            return
        
        # 创建管理员用户
        admin = User(username=username, email=email, is_admin=True)
        admin.set_password(password)
        
        db.session.add(admin)
        db.session.commit()
        
        print(f'✅ 管理员用户 {username} 创建成功')
    
    @app.cli.command()
    def create_sample_data():
        """创建示例数据"""
        # 创建示例用户
        if not User.query.filter_by(username='demo').first():
            demo_user = User(username='demo', email='demo@example.com')
            demo_user.set_password('demo123')
            db.session.add(demo_user)
            db.session.commit()
            
            # 创建示例文章
            sample_article = Article(
                title='欢迎使用个人博客管理系统',
                content='这是一个使用Flask和Vue.js构建的现代化博客系统。支持文章管理、用户认证、评论系统等功能。',
                summary='个人博客管理系统介绍',
                is_published=True,
                author_id=demo_user.id
            )
            
            # 创建示例标签
            tag1 = Tag(name='Flask')
            tag2 = Tag(name='Vue.js')
            tag3 = Tag(name='Python')
            
            sample_article.tags.extend([tag1, tag2, tag3])
            
            db.session.add(sample_article)
            db.session.commit()
            
            print('✅ 示例数据创建完成')
        else:
            print('⚠️  示例数据已存在')

# 创建应用实例
app = create_app()

if __name__ == '__main__':
    # 开发环境运行
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
