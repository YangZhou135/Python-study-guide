#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一API响应格式工具
提供标准化的JSON响应格式
"""

from flask import jsonify
from typing import Any, Dict, Optional, Union
from datetime import datetime

class ResponseCode:
    """响应状态码常量"""
    SUCCESS = 'SUCCESS'
    ERROR = 'ERROR'
    VALIDATION_ERROR = 'VALIDATION_ERROR'
    AUTHENTICATION_ERROR = 'AUTHENTICATION_ERROR'
    AUTHORIZATION_ERROR = 'AUTHORIZATION_ERROR'
    NOT_FOUND = 'NOT_FOUND'
    CONFLICT = 'CONFLICT'
    RATE_LIMIT_ERROR = 'RATE_LIMIT_ERROR'
    INTERNAL_ERROR = 'INTERNAL_ERROR'

class ResponseMessage:
    """响应消息常量"""
    SUCCESS = '操作成功'
    ERROR = '操作失败'
    VALIDATION_ERROR = '参数验证失败'
    AUTHENTICATION_ERROR = '认证失败'
    AUTHORIZATION_ERROR = '权限不足'
    NOT_FOUND = '资源不存在'
    CONFLICT = '资源冲突'
    RATE_LIMIT_ERROR = '��求过于频繁'
    INTERNAL_ERROR = '服务器内部错误'

def success_response(
    data: Any = None,
    message: str = ResponseMessage.SUCCESS,
    code: str = ResponseCode.SUCCESS,
    status_code: int = 200,
    **kwargs
) -> tuple:
    """
    成功响应格式
    
    Args:
        data: 响应数据
        message: 响应消息
        code: 响应代码
        status_code: HTTP状态码
        **kwargs: 额外的响应字段
    
    Returns:
        tuple: (响应JSON, HTTP状态码)
    """
    response_data = {
        'success': True,
        'code': code,
        'message': message,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    
    if data is not None:
        response_data['data'] = data
    
    # 添加额外字段
    response_data.update(kwargs)
    
    return jsonify(response_data), status_code

def error_response(
    message: str = ResponseMessage.ERROR,
    code: str = ResponseCode.ERROR,
    status_code: int = 400,
    details: Optional[Dict] = None,
    **kwargs
) -> tuple:
    """
    错误响应格式
    
    Args:
        message: 错误��息
        code: 错误代码
        status_code: HTTP状态码
        details: 错误详情
        **kwargs: 额外的响应字段
    
    Returns:
        tuple: (响应JSON, HTTP状态码)
    """
    response_data = {
        'success': False,
        'error': {
            'code': code,
            'message': message,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
    }
    
    if details:
        response_data['error']['details'] = details
    
    # 添加额外字段
    response_data.update(kwargs)
    
    return jsonify(response_data), status_code

def validation_error_response(
    message: str = ResponseMessage.VALIDATION_ERROR,
    errors: Optional[Dict] = None,
    status_code: int = 422
) -> tuple:
    """
    验证错误响应
    
    Args:
        message: 错误消息
        errors: 验证错误详情
        status_code: HTTP状态码
    
    Returns:
        tuple: (响应JSON, HTTP状态码)
    """
    details = {}
    if errors:
        details['validation_errors'] = errors
    
    return error_response(
        message=message,
        code=ResponseCode.VALIDATION_ERROR,
        status_code=status_code,
        details=details
    )

def not_found_response(
    resource: str = '资源',
    message: Optional[str] = None
) -> tuple:
    """
    资源不存在响应
    
    Args:
        resource: 资源名称
        message: 自定义消息
    
    Returns:
        tuple: (响应JSON, HTTP状态码)
    """
    if message is None:
        message = f'{resource}不存在'
    
    return error_response(
        message=message,
        code=ResponseCode.NOT_FOUND,
        status_code=404
    )

def unauthorized_response(
    message: str = ResponseMessage.AUTHENTICATION_ERROR
) -> tuple:
    """
    未认证响应
    
    Args:
        message: 错误消息
    
    Returns:
        tuple: (响应JSON, HTTP状态码)
    """
    return error_response(
        message=message,
        code=ResponseCode.AUTHENTICATION_ERROR,
        status_code=401
    )

def forbidden_response(
    message: str = ResponseMessage.AUTHORIZATION_ERROR
) -> tuple:
    """
    权限不足响应
    
    Args:
        message: 错误消息
    
    Returns:
        tuple: (响应JSON, HTTP状态码)
    """
    return error_response(
        message=message,
        code=ResponseCode.AUTHORIZATION_ERROR,
        status_code=403
    )

def conflict_response(
    message: str = ResponseMessage.CONFLICT,
    details: Optional[Dict] = None
) -> tuple:
    """
    资源冲突响应
    
    Args:
        message: 错误消息
        details: 冲突详情
    
    Returns:
        tuple: (响应JSON, HTTP状态码)
    """
    return error_response(
        message=message,
        code=ResponseCode.CONFLICT,
        status_code=409,
        details=details
    )

def rate_limit_response(
    message: str = ResponseMessage.RATE_LIMIT_ERROR
) -> tuple:
    """
    限流响应
    
    Args:
        message: 错误消息
    
    Returns:
        tuple: (响应JSON, HTTP状态码)
    """
    return error_response(
        message=message,
        code=ResponseCode.RATE_LIMIT_ERROR,
        status_code=429
    )

def internal_error_response(
    message: str = ResponseMessage.INTERNAL_ERROR,
    details: Optional[Dict] = None
) -> tuple:
    """
    服务器内部错误响应
    
    Args:
        message: 错误消息
        details: 错误详情
    
    Returns:
        tuple: (响应JSON, HTTP状态码)
    """
    return error_response(
        message=message,
        code=ResponseCode.INTERNAL_ERROR,
        status_code=500,
        details=details
    )

def paginated_response(
    data: list,
    page: int,
    per_page: int,
    total: int,
    message: str = ResponseMessage.SUCCESS
) -> tuple:
    """
    分页响应格式
    
    Args:
        data: 分页数据
        page: 当前页码
        per_page: 每页数量
        total: 总数量
        message: 响应消息
    
    Returns:
        tuple: (响应JSON, HTTP状态码)
    """
    import math
    
    pagination_info = {
        'page': page,
        'per_page': per_page,
        'total': total,
        'pages': math.ceil(total / per_page) if per_page > 0 else 0,
        'has_prev': page > 1,
        'has_next': page < math.ceil(total / per_page) if per_page > 0 else False
    }
    
    return success_response(
        data=data,
        message=message,
        pagination=pagination_info
    )

# 响应装饰器
def api_response(func):
    """
    API响应装饰器
    自动处理异常并返回标准格式响应
    """
    from functools import wraps
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return validation_error_response(str(e))
        except PermissionError as e:
            return forbidden_response(str(e))
        except FileNotFoundError as e:
            return not_found_response(message=str(e))
        except Exception as e:
            # 记录错误日志
            import logging
            logging.error(f"API错误: {str(e)}", exc_info=True)
            return internal_error_response()
    
    return wrapper
