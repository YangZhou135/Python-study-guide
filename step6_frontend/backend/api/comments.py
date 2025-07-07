#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
评论API模块 - Stage 6 前后端集成
提供评论的CRUD操作和管理功能
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from sqlalchemy import desc, asc, or_

# 导入数据库模型
from models import db, Comment, Article, User

# 导入工具函数
from utils.response import (
    success_response, error_response, validation_error_response,
    not_found_response, paginated_response
)
from utils.validation import (
    validate_request_data, format_validation_errors,
    CommentCreateSchema, CommentUpdateSchema, PaginationSchema
)
from middleware.auth import owner_or_admin_required

# 创建蓝图
comments_bp = Blueprint('comments', __name__)

def comment_owner_required(f):
    """评论所有者权限装饰器"""
    def decorated_function(comment_id, *args, **kwargs):
        comment = Comment.query.get(comment_id)
        if not comment:
            return not_found_response('评论')
        
        current_user_id = get_jwt_identity()
        if comment.author_id != current_user_id:
            return error_response('无权限操作此评论', status_code=403)
        
        return f(comment_id, *args, **kwargs)
    
    decorated_function.__name__ = f.__name__
    return decorated_function

@comments_bp.route('', methods=['GET'])
def get_comments():
    """
    获取评论列表
    
    Query Parameters:
        article_id: 文章ID (可选)
        author_id: 作者ID (可选)
        sort: 排序字段 (默认: created_at)
        order: 排序方向 (默认: desc)
        page: 页码 (默认: 1)
        per_page: 每页数量 (默认: 20)
    
    Returns:
        JSON: 评论列表和分页信息
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
        query = Comment.query
        
        # 文章过滤
        article_id = args.get('article_id')
        if article_id:
            query = query.filter(Comment.article_id == article_id)
        
        # 作者过滤
        author_id = args.get('author_id')
        if author_id:
            query = query.filter(Comment.author_id == author_id)
        
        # 排序
        sort_field = args.get('sort', 'created_at')
        order = args.get('order', 'desc')
        
        sort_column = getattr(Comment, sort_field, Comment.created_at)
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
        
        # 序列化评论数据
        comments_data = []
        for comment in pagination.items:
            comment_data = {
                'id': comment.id,
                'content': comment.content,
                'created_at': comment.created_at.isoformat(),
                'author': {
                    'id': comment.author.id,
                    'username': comment.author.username
                },
                'article': {
                    'id': comment.article.id,
                    'title': comment.article.title
                },
                'parent_id': comment.parent_id,
                'replies_count': comment.replies.count() if hasattr(comment, 'replies') else 0
            }
            comments_data.append(comment_data)
        
        return paginated_response(
            data=comments_data,
            page=pagination.page,
            per_page=pagination.per_page,
            total=pagination.total,
            message=f'获取到 {pagination.total} 条评论'
        )
        
    except ValidationError as e:
        return validation_error_response(
            errors=format_validation_errors(e.messages)
        )
    except Exception as e:
        return error_response(f'获取评论列表失败: {str(e)}')

@comments_bp.route('/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    """
    获取评论详情
    
    Path Parameters:
        comment_id: 评论ID
    
    Returns:
        JSON: 评论详细信息
    """
    try:
        comment = Comment.query.get(comment_id)
        if not comment:
            return not_found_response('评论')
        
        # 获取回复评论
        replies = Comment.query.filter_by(parent_id=comment_id).order_by(Comment.created_at.asc()).all()
        
        # 序列化评论数据
        comment_data = {
            'id': comment.id,
            'content': comment.content,
            'created_at': comment.created_at.isoformat(),
            'author': {
                'id': comment.author.id,
                'username': comment.author.username
            },
            'article': {
                'id': comment.article.id,
                'title': comment.article.title
            },
            'parent_id': comment.parent_id,
            'replies': [
                {
                    'id': reply.id,
                    'content': reply.content,
                    'created_at': reply.created_at.isoformat(),
                    'author': {
                        'id': reply.author.id,
                        'username': reply.author.username
                    }
                }
                for reply in replies
            ]
        }
        
        return success_response(
            data={'comment': comment_data},
            message='评论获取成功'
        )
        
    except Exception as e:
        return error_response(f'获取评论失败: {str(e)}')

@comments_bp.route('', methods=['POST'])
@jwt_required()
def create_comment():
    """
    创建评论
    
    Headers:
        Authorization: Bearer <access_token>
    
    Body:
        article_id: 文章ID
        content: 评论内容
        parent_id: 父评论ID (可选，用于回复)
    
    Returns:
        JSON: 创建的评论信息
    """
    try:
        current_user_id = get_jwt_identity()
        
        # 验证请求数据
        data = validate_request_data(CommentCreateSchema, request.get_json() or {})
        
        # 检查文章是否存在
        article = Article.query.get(data['article_id'])
        if not article:
            return not_found_response('文章')
        
        if not article.is_published:
            return error_response('无法对未发布的文章评论', status_code=400)
        
        # 检查父评论是否存在（如果是回复）
        parent_comment = None
        if data.get('parent_id'):
            parent_comment = Comment.query.get(data['parent_id'])
            if not parent_comment:
                return not_found_response('父评论')
            
            # 确保父评论属于同一篇文章
            if parent_comment.article_id != data['article_id']:
                return error_response('父评论不属于指定文章', status_code=400)
        
        # 创建评论
        comment = Comment(
            content=data['content'],
            article_id=data['article_id'],
            author_id=current_user_id,
            parent_id=data.get('parent_id')
        )
        
        db.session.add(comment)
        db.session.commit()
        
        # 序列化评论数据
        comment_data = {
            'id': comment.id,
            'content': comment.content,
            'created_at': comment.created_at.isoformat(),
            'author': {
                'id': comment.author.id,
                'username': comment.author.username
            },
            'article': {
                'id': comment.article.id,
                'title': comment.article.title
            },
            'parent_id': comment.parent_id
        }
        
        return success_response(
            data={'comment': comment_data},
            message='评论创建成功',
            status_code=201
        )
        
    except ValidationError as e:
        return validation_error_response(
            errors=format_validation_errors(e.messages)
        )
    except Exception as e:
        return error_response(f'评论创建失败: {str(e)}')

@comments_bp.route('/<int:comment_id>', methods=['PUT'])
@jwt_required()
@comment_owner_required
def update_comment(comment_id):
    """
    更新评论
    
    Path Parameters:
        comment_id: 评论ID
    
    Headers:
        Authorization: Bearer <access_token>
    
    Body:
        content: 评论内容
    
    Returns:
        JSON: 更新后的评论信息
    """
    try:
        comment = Comment.query.get(comment_id)
        
        # 验证请求数据
        data = validate_request_data(CommentUpdateSchema, request.get_json() or {})
        
        # 更新评论内容
        comment.content = data['content']
        db.session.commit()
        
        # 序列化评论数据
        comment_data = {
            'id': comment.id,
            'content': comment.content,
            'created_at': comment.created_at.isoformat(),
            'author': {
                'id': comment.author.id,
                'username': comment.author.username
            },
            'article': {
                'id': comment.article.id,
                'title': comment.article.title
            },
            'parent_id': comment.parent_id
        }
        
        return success_response(
            data={'comment': comment_data},
            message='评论更新成功'
        )
        
    except ValidationError as e:
        return validation_error_response(
            errors=format_validation_errors(e.messages)
        )
    except Exception as e:
        return error_response(f'评论更新失败: {str(e)}')

@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required()
@comment_owner_required
def delete_comment(comment_id):
    """
    删除评论
    
    Path Parameters:
        comment_id: 评论ID
    
    Headers:
        Authorization: Bearer <access_token>
    
    Returns:
        JSON: 删除结果
    """
    try:
        comment = Comment.query.get(comment_id)
        
        # 删除评论 (级联删除回复)
        db.session.delete(comment)
        db.session.commit()
        
        return success_response(message='评论删除成功')
        
    except Exception as e:
        return error_response(f'评论删除失败: {str(e)}')
