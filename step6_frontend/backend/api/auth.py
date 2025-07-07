#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
认证相关API
提供用户注册、登录、令牌刷新等功能
"""

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, get_jwt
from marshmallow import ValidationError
from werkzeug.security import check_password_hash

# 导入数据库模型 (需要从step5复制)
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../step5_database'))
from models import db, User

# 导入工具函数
from utils.response import (
    success_response, error_response, validation_error_response,
    unauthorized_response, conflict_response
)
from utils.jwt_helper import JWTHelper, TokenBlacklist
from utils.validation import (
    UserRegistrationSchema, UserLoginSchema, PasswordChangeSchema,
    validate_request_data, format_validation_errors
)
from middleware.auth import jwt_required

# 创建蓝图
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    用户注册
    
    Body:
        username: 用户名
        email: 邮箱
        password: 密码
        confirm_password: 确认密码
    
    Returns:
        JSON: 注册结果和用户信息
    """
    try:
        raw_data = request.get_json() or {}
        # 手动检查密码确认
        password = raw_data.get('password')
        confirm_password = raw_data.get('confirm_password')

        if not password or not confirm_password:
            return validation_error_response(errors={'confirm_password': ['密码和确认密码是必填项。']})

        if password != confirm_password:
            return validation_error_response(errors={'confirm_password': ['两次输入的密码不匹配。']})

        # 验证请求数据
        data = validate_request_data(UserRegistrationSchema, raw_data)
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=data['username']).first():
            return conflict_response('用户名已存在')
        
        # 检查邮箱是否已存在
        if User.query.filter_by(email=data['email']).first():
            return conflict_response('邮箱已被注册')
        
        # 创建新用户
        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # 生成JWT令牌
        tokens = JWTHelper.generate_tokens(user.id)
        
        # 返回用户信息和令牌
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at.isoformat(),
            'is_active': user.is_active
        }
        
        return success_response(
            data={
                'user': user_data,
                'tokens': tokens
            },
            message='注册成功'
        )
        
    except ValidationError as e:
        return validation_error_response(
            errors=format_validation_errors(e.messages)
        )
    except Exception as e:
        return error_response(f'注册失败: {str(e)}')

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    用户登录
    
    Body:
        username: 用户名或邮箱
        password: 密码
    
    Returns:
        JSON: 登录结果和令牌
    """
    try:
        # 验证请求数据
        data = validate_request_data(UserLoginSchema, request.get_json() or {})
        
        # 查找用户 (支持用户名或邮箱登录)
        user = User.query.filter(
            (User.username == data['username']) | 
            (User.email == data['username'])
        ).first()
        
        # 验证用户和密码
        if not user or not user.check_password(data['password']):
            return unauthorized_response('用户名或密码错误')
        
        # 检查用户是否激活
        if not user.is_active:
            return unauthorized_response('账户已被禁用')
        
        # 更新登录信息
        user.login()
        
        # 生成JWT令牌
        tokens = JWTHelper.generate_tokens(user.id, {
            'username': user.username,
            'email': user.email
        })
        
        # 返回用户信息和令牌
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'login_count': user.login_count,
            'is_active': user.is_active
        }
        
        return success_response(
            data={
                'user': user_data,
                'tokens': tokens
            },
            message='登录成功'
        )
        
    except ValidationError as e:
        return validation_error_response(
            errors=format_validation_errors(e.messages)
        )
    except Exception as e:
        return error_response(f'登录失败: {str(e)}')

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required()
def refresh_token():
    """
    刷新访问令牌
    
    Headers:
        Authorization: Bearer <refresh_token>
    
    Returns:
        JSON: 新的访问令牌
    """
    try:
        current_user_id = get_jwt_identity()
        
        # 验证用户是否存在且激活
        user = User.query.get(current_user_id)
        if not user or not user.is_active:
            return unauthorized_response('用户不存在或已被禁用')
        
        # 生成新的访问令牌
        tokens = JWTHelper.generate_tokens(user.id, {
            'username': user.username,
            'email': user.email
        })
        
        return success_response(
            data={'tokens': tokens},
            message='令牌刷新成功'
        )
        
    except Exception as e:
        return error_response(f'令牌刷新失败: {str(e)}')

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    用户登出
    
    Headers:
        Authorization: Bearer <access_token>
    
    Returns:
        JSON: 登出结果
    """
    try:
        # 获取当前令牌的JTI (JWT ID)
        jti = get_jwt().get('jti')
        
        # 将令牌添加到黑名单
        if jti:
            TokenBlacklist.add_token(jti)
        
        return success_response(message='登出成功')
        
    except Exception as e:
        return error_response(f'登出失败: {str(e)}')

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    获取当前用户信息
    
    Headers:
        Authorization: Bearer <access_token>
    
    Returns:
        JSON: 当前用户信息
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return unauthorized_response('用户不存在')
        
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at.isoformat(),
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'login_count': user.login_count,
            'is_active': user.is_active,
            'article_count': user.article_count,
            'comment_count': user.comment_count
        }
        
        return success_response(
            data={'user': user_data},
            message='获取用户信息成功'
        )
        
    except Exception as e:
        return error_response(f'获取用户信息失败: {str(e)}')

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """
    修改密码
    
    Headers:
        Authorization: Bearer <access_token>
    
    Body:
        current_password: 当前密码
        new_password: 新密码
        confirm_password: 确认新密码
    
    Returns:
        JSON: 修改结果
    """
    try:
        # 验证请求数据
        data = validate_request_data(PasswordChangeSchema, request.get_json() or {})
        
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return unauthorized_response('用户不存在')
        
        # 验证当前密码
        if not user.check_password(data['current_password']):
            return unauthorized_response('当前密码错误')
        
        # 设置新密码
        user.set_password(data['new_password'])
        db.session.commit()
        
        return success_response(message='密码修改成功')
        
    except ValidationError as e:
        return validation_error_response(
            errors=format_validation_errors(e.messages)
        )
    except Exception as e:
        return error_response(f'密码修改失败: {str(e)}')

@auth_bp.route('/check-username', methods=['POST'])
def check_username():
    """
    检查用户名是否可用
    
    Body:
        username: 要检查的用户名
    
    Returns:
        JSON: 检查结果
    """
    try:
        data = request.get_json() or {}
        username = data.get('username', '').strip()
        
        if not username:
            return validation_error_response('用户名不能为空')
        
        # 检查用户名格式
        from utils.validation import ValidationHelper
        if not ValidationHelper.validate_username(username):
            return validation_error_response('用户名格式不正确')
        
        # 检查是否已存在
        exists = User.query.filter_by(username=username).first() is not None
        
        return success_response(
            data={
                'username': username,
                'available': not exists
            },
            message='检查完成'
        )
        
    except Exception as e:
        return error_response(f'检查失败: {str(e)}')

@auth_bp.route('/check-email', methods=['POST'])
def check_email():
    """
    检查邮箱是否可用
    
    Body:
        email: 要检查的邮箱
    
    Returns:
        JSON: 检查结果
    """
    try:
        data = request.get_json() or {}
        email = data.get('email', '').strip()
        
        if not email:
            return validation_error_response('邮箱不能为空')
        
        # 检查邮箱格式
        from utils.validation import ValidationHelper
        if not ValidationHelper.validate_email(email):
            return validation_error_response('邮箱格式不正确')
        
        # 检查是否已存在
        exists = User.query.filter_by(email=email).first() is not None
        
        return success_response(
            data={
                'email': email,
                'available': not exists
            },
            message='检查完成'
        )
        
    except Exception as e:
        return error_response(f'检查失败: {str(e)}')
