#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户API模块 - Stage 6 前后端集成
提供用户管理和个人资料操作
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from sqlalchemy import desc, asc, func

# 导入数据库模型
from models import db, User, Article, Comment

# 导入工具函数
from utils.response import (
    success_response, error_response, validation_error_response,
    not_found_response, paginated_response
)
from utils.validation import (
    validate_request_data, format_validation_errors,
    UserProfileUpdateSchema, PaginationSchema
)
from middleware.auth import admin_required

# 创建蓝图
users_bp = Blueprint('users', __name__)

@users_bp.route('', methods=['GET'])
@admin_required
def get_users():
    """
    获取用户列表 (仅管理员)
    
    Query Parameters:
        search: 搜索关键词 (用户名或邮箱)
        sort: 排序字段 (默认: created_at)
        order: 排序方向 (默认: desc)
        page: 页码 (默认: 1)
        per_page: 每页数量 (默认: 20)
    
    Returns:
        JSON: 用户列表和分页信息
    """
    try:
        # 获取查询参数
        args = request.args.to_dict()
        
        # 验证分页参数
        pagination_data = validate_request_data(PaginationSchema, {
            'page': args.get('page', 1),
            'per_page': args.get('per_page', 20)
        })
        
        # 构建查询
        query = User.query
        
        # 搜索过滤
        search = args.get('search')
        if search:
            search_pattern = f'%{search}%'
            query = query.filter(
                db.or_(
                    User.username.like(search_pattern),
                    User.email.like(search_pattern)
                )
            )
        
        # 排序
        sort_field = args.get('sort', 'created_at')
        order = args.get('order', 'desc')
        
        sort_column = getattr(User, sort_field, User.created_at)
        if order == 'asc':
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        # 分页查询
        pagination = query.paginate(
            page=pagination_data['page'],
            per_page=pagination_data['per_page'],
            error_out=False
        )
        
        # 序列化用户数据
        users_data = []
        for user in pagination.items:
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_active': user.is_active,
                'created_at': user.created_at.isoformat(),
                'last_login': user.last_login.isoformat() if user.last_login else None,
                'login_count': user.login_count,
                'articles_count': user.articles.count(),
                'comments_count': user.comments.count()
            }
            users_data.append(user_data)
        
        return paginated_response(
            data=users_data,
            page=pagination.page,
            per_page=pagination.per_page,
            total=pagination.total,
            message=f'获取到 {pagination.total} 个用户'
        )
        
    except ValidationError as e:
        return validation_error_response(
            errors=format_validation_errors(e.messages)
        )
    except Exception as e:
        return error_response(f'获取用户列表失败: {str(e)}')

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    获取用户详情
    
    Path Parameters:
        user_id: 用户ID
    
    Returns:
        JSON: 用户详细信息
    """
    try:
        user = User.query.get(user_id)
        if not user:
            return not_found_response('用户')
        
        # 获取用户统计信息
        articles_count = user.articles.filter_by(is_published=True).count()
        comments_count = user.comments.count()
        total_views = db.session.query(func.sum(Article.views)).filter_by(author_id=user_id, is_published=True).scalar() or 0
        total_likes = db.session.query(func.sum(Article.likes)).filter_by(author_id=user_id, is_published=True).scalar() or 0
        
        # 获取最近文章
        recent_articles = user.articles.filter_by(is_published=True).order_by(desc(Article.created_at)).limit(5).all()
        
        # 序列化用户数据
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat(),
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'login_count': user.login_count,
            'statistics': {
                'articles_count': articles_count,
                'comments_count': comments_count,
                'total_views': total_views,
                'total_likes': total_likes
            },
            'recent_articles': [
                {
                    'id': article.id,
                    'title': article.title,
                    'created_at': article.created_at.isoformat(),
                    'views': article.views,
                    'likes': article.likes
                }
                for article in recent_articles
            ]
        }
        
        return success_response(
            data={'user': user_data},
            message='用户信息获取成功'
        )
        
    except Exception as e:
        return error_response(f'获取用户信息失败: {str(e)}')

@users_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    获取当前用户信息
    
    Headers:
        Authorization: Bearer <access_token>
    
    Returns:
        JSON: 当前用户详细信息
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return not_found_response('用户')
        
        # 获取用户统计信息
        articles_count = user.articles.filter_by(is_published=True).count()
        draft_count = user.articles.filter_by(is_published=False).count()
        comments_count = user.comments.count()
        total_views = db.session.query(func.sum(Article.views)).filter_by(author_id=current_user_id, is_published=True).scalar() or 0
        total_likes = db.session.query(func.sum(Article.likes)).filter_by(author_id=current_user_id, is_published=True).scalar() or 0
        
        # 序列化用户数据
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat(),
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'login_count': user.login_count,
            'statistics': {
                'articles_count': articles_count,
                'draft_count': draft_count,
                'comments_count': comments_count,
                'total_views': total_views,
                'total_likes': total_likes
            }
        }
        
        return success_response(
            data={'user': user_data},
            message='用户信息获取成功'
        )
        
    except Exception as e:
        return error_response(f'获取用户信息失败: {str(e)}')

@users_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_current_user():
    """
    更新当前用户信息
    
    Headers:
        Authorization: Bearer <access_token>
    
    Body:
        username: 用户名 (可选)
        email: 邮箱 (可选)
    
    Returns:
        JSON: 更新后的用户信息
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return not_found_response('用户')
        
        # 验证请求数据
        data = validate_request_data(UserProfileUpdateSchema, request.get_json() or {})
        
        # 检查用户名是否已被使用
        if 'username' in data and data['username'] != user.username:
            existing_user = User.query.filter_by(username=data['username']).first()
            if existing_user:
                return error_response('用户名已被使用', status_code=400)
            user.username = data['username']
        
        # 检查邮箱是否已被使用
        if 'email' in data and data['email'] != user.email:
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user:
                return error_response('邮箱已被使用', status_code=400)
            user.email = data['email']
        
        db.session.commit()
        
        # 序列化用户数据
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat(),
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'login_count': user.login_count
        }
        
        return success_response(
            data={'user': user_data},
            message='用户信息更新成功'
        )
        
    except ValidationError as e:
        return validation_error_response(
            errors=format_validation_errors(e.messages)
        )
    except Exception as e:
        return error_response(f'用户信息更新失败: {str(e)}')

@users_bp.route('/<int:user_id>/toggle-status', methods=['POST'])
@jwt_required()
@admin_required
def toggle_user_status(user_id):
    """
    切换用户状态 (仅管理员)
    
    Path Parameters:
        user_id: 用户ID
    
    Headers:
        Authorization: Bearer <access_token>
    
    Returns:
        JSON: 操作结果
    """
    try:
        user = User.query.get(user_id)
        if not user:
            return not_found_response('用户')
        
        # 切换用户状态
        user.is_active = not user.is_active
        db.session.commit()
        
        status_text = '激活' if user.is_active else '禁用'
        
        return success_response(
            data={'user_id': user_id, 'is_active': user.is_active},
            message=f'用户已{status_text}'
        )
        
    except Exception as e:
        return error_response(f'用户状态切换失败: {str(e)}')
