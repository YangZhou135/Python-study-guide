#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JWT认证工具
提供JWT token的生成、验证和管理功能
"""

from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, verify_jwt_in_request
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
import jwt

class JWTHelper:
    """JWT工具类"""
    
    @staticmethod
    def generate_tokens(user_id: int, additional_claims: Optional[Dict] = None) -> Dict[str, str]:
        """
        生成访问令牌和刷新令牌
        
        Args:
            user_id: 用户ID
            additional_claims: 额外的声明信息
        
        Returns:
            Dict: 包含access_token和refresh_token的字典
        """
        # 准备额外声明
        claims = additional_claims or {}
        claims.update({
            'user_id': user_id,
            'type': 'access'
        })
        
        # 生成访问令牌
        access_token = create_access_token(
            identity=str(user_id),
            additional_claims=claims
        )
        
        # 生成刷新令牌
        refresh_claims = {
            'user_id': user_id,
            'type': 'refresh'
        }
        refresh_token = create_refresh_token(
            identity=str(user_id),
            additional_claims=refresh_claims
        )
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer',
            'expires_in': int(current_app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds())
        }
    
    @staticmethod
    def decode_token(token: str) -> Optional[Dict[str, Any]]:
        """
        解码JWT令牌
        
        Args:
            token: JWT令牌
        
        Returns:
            Dict: 解码后的载荷，如果失败返回None
        """
        try:
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=[current_app.config['JWT_ALGORITHM']]
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def get_current_user_id() -> Optional[int]:
        """
        获取当前用户ID
        
        Returns:
            int: 用户ID，如果未认证返回None
        """
        try:
            verify_jwt_in_request()
            return get_jwt_identity()
        except:
            return None
    
    @staticmethod
    def is_token_expired(token: str) -> bool:
        """
        检查令牌是否过期
        
        Args:
            token: JWT令牌
        
        Returns:
            bool: 是否过期
        """
        payload = JWTHelper.decode_token(token)
        if not payload:
            return True
        
        exp = payload.get('exp')
        if not exp:
            return True
        
        return datetime.utcnow().timestamp() > exp
    
    @staticmethod
    def get_token_remaining_time(token: str) -> Optional[timedelta]:
        """
        获取令牌剩余有效时间
        
        Args:
            token: JWT令牌
        
        Returns:
            timedelta: 剩余时间，如果令牌无效返回None
        """
        payload = JWTHelper.decode_token(token)
        if not payload:
            return None
        
        exp = payload.get('exp')
        if not exp:
            return None
        
        remaining_seconds = exp - datetime.utcnow().timestamp()
        if remaining_seconds <= 0:
            return None
        
        return timedelta(seconds=remaining_seconds)
    
    @staticmethod
    def refresh_access_token(refresh_token: str) -> Optional[Dict[str, str]]:
        """
        使用刷新令牌生成新的访问令牌
        
        Args:
            refresh_token: 刷新令牌
        
        Returns:
            Dict: 新的令牌信息，如果失败返回None
        """
        payload = JWTHelper.decode_token(refresh_token)
        if not payload:
            return None
        
        # 验证是否为刷新令牌
        if payload.get('type') != 'refresh':
            return None
        
        user_id = payload.get('user_id')
        if not user_id:
            return None
        
        # 生成新的访问令牌
        return JWTHelper.generate_tokens(user_id)
    
    @staticmethod
    def create_password_reset_token(user_id: int, expires_delta: Optional[timedelta] = None) -> str:
        """
        创建密码重置令牌
        
        Args:
            user_id: 用户ID
            expires_delta: 过期时间间隔
        
        Returns:
            str: 密码重置令牌
        """
        if expires_delta is None:
            expires_delta = timedelta(hours=1)
        
        payload = {
            'user_id': user_id,
            'type': 'password_reset',
            'exp': datetime.utcnow() + expires_delta,
            'iat': datetime.utcnow()
        }
        
        return jwt.encode(
            payload,
            current_app.config['JWT_SECRET_KEY'],
            algorithm=current_app.config['JWT_ALGORITHM']
        )
    
    @staticmethod
    def verify_password_reset_token(token: str) -> Optional[int]:
        """
        验证密码重置令牌
        
        Args:
            token: 密码重置令牌
        
        Returns:
            int: 用户ID，如果验证失败返回None
        """
        payload = JWTHelper.decode_token(token)
        if not payload:
            return None
        
        # 验证令牌类型
        if payload.get('type') != 'password_reset':
            return None
        
        return payload.get('user_id')
    
    @staticmethod
    def create_email_verification_token(user_id: int, email: str) -> str:
        """
        创建邮箱验证令牌
        
        Args:
            user_id: 用户ID
            email: 邮箱地址
        
        Returns:
            str: 邮箱验证令牌
        """
        payload = {
            'user_id': user_id,
            'email': email,
            'type': 'email_verification',
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow()
        }
        
        return jwt.encode(
            payload,
            current_app.config['JWT_SECRET_KEY'],
            algorithm=current_app.config['JWT_ALGORITHM']
        )
    
    @staticmethod
    def verify_email_verification_token(token: str) -> Optional[Dict[str, Any]]:
        """
        验证邮箱验证令牌
        
        Args:
            token: 邮箱验证令牌
        
        Returns:
            Dict: 包含user_id和email的字典，如果验证失败返回None
        """
        payload = JWTHelper.decode_token(token)
        if not payload:
            return None
        
        # 验证令牌类型
        if payload.get('type') != 'email_verification':
            return None
        
        user_id = payload.get('user_id')
        email = payload.get('email')
        
        if not user_id or not email:
            return None
        
        return {
            'user_id': user_id,
            'email': email
        }

# 黑名单管理 (简单实现，生产环境建议使用Redis)
class TokenBlacklist:
    """令牌黑名单管理"""
    
    _blacklist = set()
    
    @classmethod
    def add_token(cls, jti: str):
        """添加令牌到黑名单"""
        cls._blacklist.add(jti)
    
    @classmethod
    def is_token_revoked(cls, jti: str) -> bool:
        """检查令牌是否被撤销"""
        return jti in cls._blacklist
    
    @classmethod
    def clear_expired_tokens(cls):
        """清理过期的令牌 (简单实现)"""
        # 在实际应用中，应该定期清理过期的令牌
        # 这里只是一个占位符实现
        pass
