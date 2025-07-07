#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask应用配置文件
"""

import os
from datetime import timedelta

class Config:
    """基础配置类"""
    
    # 应用基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    
    # 数据存储配置
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
    UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    
    # 会话配置
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = False  # 在生产环境中设置为True
    SESSION_COOKIE_HTTPONLY = True
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'md'}
    
    # 分页配置
    ARTICLES_PER_PAGE = 10
    COMMENTS_PER_PAGE = 20
    
    # 应用信息
    APP_NAME = "Python博客系统"
    APP_VERSION = "4.0.0"
    APP_DESCRIPTION = "基于Flask的博客管理系统"

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    """测试环境配置"""
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False

# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
