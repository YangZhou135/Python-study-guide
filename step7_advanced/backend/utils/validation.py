#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据验证工具
提供通用的数据验证功能
"""

import re
from typing import Dict, List, Any, Optional, Union
from marshmallow import Schema, fields, validate, ValidationError, post_load
from werkzeug.datastructures import FileStorage

class ValidationHelper:
    """验证工具类"""
    
    # 正则表达式模式
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_]{3,20}$')
    PASSWORD_PATTERN = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,}$')
    PHONE_PATTERN = re.compile(r'^1[3-9]\d{9}$')
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """验证邮箱格式"""
        return bool(ValidationHelper.EMAIL_PATTERN.match(email))
    
    @staticmethod
    def validate_username(username: str) -> bool:
        """验证用户名格式"""
        return bool(ValidationHelper.USERNAME_PATTERN.match(username))
    
    @staticmethod
    def validate_password(password: str) -> bool:
        """验证密码强度"""
        return bool(ValidationHelper.PASSWORD_PATTERN.match(password))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """验证手机号格式"""
        return bool(ValidationHelper.PHONE_PATTERN.match(phone))
    
    @staticmethod
    def validate_file_extension(filename: str, allowed_extensions: set) -> bool:
        """验证文件扩展名"""
        if '.' not in filename:
            return False
        extension = filename.rsplit('.', 1)[1].lower()
        return extension in allowed_extensions
    
    @staticmethod
    def validate_file_size(file: FileStorage, max_size: int) -> bool:
        """验证文件大小"""
        if not file:
            return False
        
        # 获取文件大小
        file.seek(0, 2)  # 移动到文件末尾
        size = file.tell()
        file.seek(0)  # 重置文件指针
        
        return size <= max_size
    
    @staticmethod
    def validate_image_file(file: FileStorage, max_size: int = 5 * 1024 * 1024) -> Dict[str, Any]:
        """
        验证图片文件
        
        Args:
            file: 上传的文件
            max_size: 最大文件大小 (字节)
        
        Returns:
            Dict: 验证结果
        """
        result = {
            'valid': True,
            'errors': []
        }
        
        if not file or not file.filename:
            result['valid'] = False
            result['errors'].append('未选择文件')
            return result
        
        # 验证文件扩展名
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        if not ValidationHelper.validate_file_extension(file.filename, allowed_extensions):
            result['valid'] = False
            result['errors'].append('不支持的文件格式')
        
        # 验证文件大小
        if not ValidationHelper.validate_file_size(file, max_size):
            result['valid'] = False
            result['errors'].append(f'文件大小超过限制 ({max_size // (1024*1024)}MB)')
        
        return result

# Marshmallow 验证模式
class UserRegistrationSchema(Schema):
    """用户注册验证模式"""
    username = fields.Str(
        required=True,
        validate=[
            validate.Length(min=3, max=20, error='用户名长度必须在3-20个字符之间'),
            validate.Regexp(
                ValidationHelper.USERNAME_PATTERN,
                error='用户名只能包含字母、数字和下划线'
            )
        ]
    )
    email = fields.Email(required=True, error_messages={'invalid': '邮箱格式不正确'})
    password = fields.Str(
        required=True,
        validate=[
            validate.Length(min=8, error='密码长度至少8个字符'),
            validate.Regexp(
                ValidationHelper.PASSWORD_PATTERN,
                error='密码必须包含大小写字母和数字'
            )
        ]
    )
    confirm_password = fields.Str(required=True)
    
    @post_load
    def validate_passwords_match(self, data, **kwargs):
        """验证密码确认"""
        if data['password'] != data['confirm_password']:
            raise ValidationError('密码确认不匹配', field_name='confirm_password')
        data.pop('confirm_password')  # 移除确认密码字段
        return data

class UserLoginSchema(Schema):
    """用户登录验证模式"""
    username = fields.Str(required=True, validate=validate.Length(min=1, error='用户名不能为空'))
    password = fields.Str(required=True, validate=validate.Length(min=1, error='密码不能为空'))

class ArticleCreateSchema(Schema):
    """文章创建验证模式"""
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=200, error='标题长度必须在1-200个字符之间')
    )
    content = fields.Str(
        required=True,
        validate=validate.Length(min=1, error='内容不能为空')
    )
    summary = fields.Str(
        missing='',
        validate=validate.Length(max=500, error='摘要长度不能超过500个字符')
    )
    tags = fields.List(
        fields.Str(validate=validate.Length(min=1, max=50)),
        missing=[],
        validate=validate.Length(max=10, error='标签数量不能超过10个')
    )
    is_published = fields.Bool(missing=False)
    featured_image = fields.Str(missing='', allow_none=True)

class ArticleUpdateSchema(ArticleCreateSchema):
    """文章更新验证模式"""
    title = fields.Str(
        validate=validate.Length(min=1, max=200, error='标题长度必须在1-200个字符之间')
    )
    content = fields.Str(
        validate=validate.Length(min=1, error='内容不能为空')
    )

class CommentCreateSchema(Schema):
    """评论创建验证模式"""
    content = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=1000, error='评论内容长度必须在1-1000个字符之间')
    )
    article_id = fields.Int(required=True, validate=validate.Range(min=1))
    parent_id = fields.Int(missing=None, allow_none=True, validate=validate.Range(min=1))

class UserProfileUpdateSchema(Schema):
    """用户资料更新验证模式"""
    email = fields.Email(error_messages={'invalid': '邮箱格式不正确'})
    bio = fields.Str(validate=validate.Length(max=500, error='个人简介长度不能超过500个字符'))
    avatar = fields.Str(allow_none=True)

class PasswordChangeSchema(Schema):
    """密码修改验���模式"""
    current_password = fields.Str(required=True, validate=validate.Length(min=1, error='当前密码不能为空'))
    new_password = fields.Str(
        required=True,
        validate=[
            validate.Length(min=8, error='新密码长度至少8个字符'),
            validate.Regexp(
                ValidationHelper.PASSWORD_PATTERN,
                error='新密码必须包含大小写字母和数字'
            )
        ]
    )
    confirm_password = fields.Str(required=True)
    
    @post_load
    def validate_passwords(self, data, **kwargs):
        """验证密码"""
        if data['new_password'] != data['confirm_password']:
            raise ValidationError('密码确认不匹配', field_name='confirm_password')
        if data['current_password'] == data['new_password']:
            raise ValidationError('新密码不能与当前密码相同', field_name='new_password')
        data.pop('confirm_password')
        return data

class PaginationSchema(Schema):
    """分页参数验证模式"""
    page = fields.Int(missing=1, validate=validate.Range(min=1, error='页码必须大于0'))
    per_page = fields.Int(
        missing=10,
        validate=validate.Range(min=1, max=100, error='每页数量必须在1-100之间')
    )

class SearchSchema(Schema):
    """搜索参数验证模式"""
    q = fields.Str(required=True, validate=validate.Length(min=1, max=100, error='搜索关键词长度必须在1-100个字符之间'))
    category = fields.Str(missing='', validate=validate.Length(max=50))
    sort = fields.Str(missing='created_at', validate=validate.OneOf(['created_at', 'updated_at', 'views', 'likes']))
    order = fields.Str(missing='desc', validate=validate.OneOf(['asc', 'desc']))

# 评论验证模式
class CommentCreateSchema(Schema):
    """评论创建验证模式"""
    article_id = fields.Int(required=True, validate=validate.Range(min=1, error='文章ID必须大于0'))
    content = fields.Str(required=True, validate=validate.Length(min=1, max=1000, error='评论内容长度必须在1-1000个字符之间'))
    parent_id = fields.Int(validate=validate.Range(min=1, error='父评论ID必须大于0'), allow_none=True)

class CommentUpdateSchema(Schema):
    """评论更新验证模式"""
    content = fields.Str(required=True, validate=validate.Length(min=1, max=1000, error='评论内容长度必须在1-1000个字符之间'))

# 用户验证模式
class UserProfileUpdateSchema(Schema):
    """用户资料更新验证模式"""
    username = fields.Str(
        validate=[
            validate.Length(min=3, max=20, error='用户名长度必须在3-20个字符之间'),
            validate.Regexp(
                ValidationHelper.USERNAME_PATTERN,
                error='用户名只能包含字母、数字和下划线'
            )
        ]
    )
    email = fields.Email(error_messages={'invalid': '邮箱格式不正确'})

def validate_request_data(schema_class: Schema, data: Dict) -> Dict[str, Any]:
    """
    验证请求数据
    
    Args:
        schema_class: Marshmallow模式类
        data: 要验证的数据
    
    Returns:
        Dict: 验证后的数据
    
    Raises:
        ValidationError: 验证失败时抛出
    """
    schema = schema_class()
    try:
        return schema.load(data)
    except ValidationError as e:
        raise ValidationError(e.messages)

def format_validation_errors(errors: Dict) -> Dict[str, List[str]]:
    """
    格式化验证错误信息
    
    Args:
        errors: Marshmallow验证错误
    
    Returns:
        Dict: 格式化后的错误信息
    """
    formatted_errors = {}
    
    def flatten_errors(error_dict, prefix=''):
        for key, value in error_dict.items():
            field_name = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                flatten_errors(value, field_name)
            elif isinstance(value, list):
                formatted_errors[field_name] = value
            else:
                formatted_errors[field_name] = [str(value)]
    
    flatten_errors(errors)
    return formatted_errors
