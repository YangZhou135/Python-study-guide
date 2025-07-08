#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
认证中间件
提供JWT认证和权限验证功能
"""

from functools import wraps
from flask import request, current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from utils.response import unauthorized_response, forbidden_response
from utils.jwt_helper import JWTHelper, TokenBlacklist

def jwt_required(optional=False):
    """
    JWT认证装饰器
    
    Args:
        optional: 是否可选认证
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request(optional=optional)
                
                # 检查令牌是否在黑名单中
                if not optional:
                    jti = get_jwt().get('jti')
                    if jti and TokenBlacklist.is_token_revoked(jti):
                        return unauthorized_response('令牌已失效')
                
                return f(*args, **kwargs)
            except Exception as e:
                if optional:
                    return f(*args, **kwargs)
                return unauthorized_response('认证失败')
        return wrapper
    return decorator

def admin_required(f):
    """
    管理员权限装饰器
    """
    @wraps(f)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        try:
            from models import User
            user = User.query.get(user_id)
            if not user or not user.is_admin:
                return forbidden_response('需要管理员权限')
        except Exception as e:
            current_app.logger.error(f"Admin check failed: {e}")
            return forbidden_response('权限验证失败')
        
        return f(*args, **kwargs)
    return wrapper

def owner_or_admin_required(get_resource_owner_id):
    """
    资源所有者或管理员权限装饰器
    
    Args:
        get_resource_owner_id: 获取资源所有者ID的函数
    """
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def wrapper(*args, **kwargs):
            current_user_id = get_jwt_identity()
            
            # 获取资源所有者ID
            resource_owner_id = get_resource_owner_id(*args, **kwargs)
            
            # 检查是否为资源所有者
            if current_user_id == resource_owner_id:
                return f(*args, **kwargs)
            
            # 检查是否为管理员
            try:
                from models import User
                user = User.query.get(current_user_id)
                if user and user.is_admin:
                    return f(*args, **kwargs)
            except:
                pass
            
            return forbidden_response('权限不足')
        return wrapper
    return decorator

def rate_limit_by_user():
    """
    基于用户的限流装饰器
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # 获取用户ID
            user_id = None
            try:
                verify_jwt_in_request(optional=True)
                user_id = get_jwt_identity()
            except:
                pass
            
            # 使用IP地址作为备用标识
            if not user_id:
                user_id = request.remote_addr
            
            # 这里可以实现具体的限流逻辑
            # 例如使用Redis存储用户请求计数
            
            return f(*args, **kwargs)
        return wrapper
    return decorator

class AuthMiddleware:
    """认证中间件类"""
    
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """初始化应用"""
        app.before_request(self.before_request)
        app.after_request(self.after_request)
    
    def before_request(self):
        """请求前处理"""
        # 记录请求信息
        if current_app.debug:
            current_app.logger.debug(f"API请求: {request.method} {request.path}")
        
        # 检查API版本
        if request.path.startswith('/api/'):
            api_version = request.headers.get('API-Version')
            if api_version and api_version != current_app.config.get('API_VERSION', 'v1'):
                return {'error': '不支持的API版本'}, 400
    
    def after_request(self, response):
        """请求后处理"""
        # 添加安全头
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # 添加API版本头
        if request.path.startswith('/api/'):
            response.headers['API-Version'] = current_app.config.get('API_VERSION', 'v1')
        
        return response

def validate_api_key():
    """
    API密钥验证装饰器 (可选功能)
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            api_key = request.headers.get('X-API-Key')
            
            # 如果配置了API密钥验证
            if current_app.config.get('REQUIRE_API_KEY'):
                valid_api_keys = current_app.config.get('VALID_API_KEYS', [])
                if not api_key or api_key not in valid_api_keys:
                    return unauthorized_response('无效的API密钥')
            
            return f(*args, **kwargs)
        return wrapper
    return decorator

def cors_preflight_handler():
    """
    CORS预检请求处理器
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if request.method == 'OPTIONS':
                response = current_app.make_default_options_response()
                headers = response.headers
                
                headers['Access-Control-Allow-Origin'] = '*'
                headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
                headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-API-Key'
                headers['Access-Control-Max-Age'] = '86400'
                
                return response
            
            return f(*args, **kwargs)
        return wrapper
    return decorator

def log_api_usage():
    """
    API使用日志装饰器
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            import time
            start_time = time.time()
            
            # 记录请求开始
            current_app.logger.info(f"API调用开始: {request.method} {request.path}")
            
            try:
                result = f(*args, **kwargs)
                
                # 记录成功响应
                duration = time.time() - start_time
                current_app.logger.info(f"API调用成功: {request.method} {request.path} - {duration:.3f}s")
                
                return result
            except Exception as e:
                # 记录错误
                duration = time.time() - start_time
                current_app.logger.error(f"API调用失败: {request.method} {request.path} - {duration:.3f}s - {str(e)}")
                raise
        return wrapper
    return decorator

# 权限检查辅助函数
def check_article_permission(article_id):
    """检查文章权限"""
    try:
        from models import Article
        article = Article.query.get(article_id)
        return article.author_id if article else None
    except:
        return None

def check_comment_permission(comment_id):
    """检查评论权限"""
    try:
        from models import Comment
        comment = Comment.query.get(comment_id)
        return comment.author_id if comment else None
    except:
        return None

# 预定义的权限装饰器
article_owner_required = owner_or_admin_required(
    lambda article_id, **kwargs: check_article_permission(article_id)
)

comment_owner_required = owner_or_admin_required(
    lambda comment_id, **kwargs: check_comment_permission(comment_id)
)
