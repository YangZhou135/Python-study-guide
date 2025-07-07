#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件 - Stage 6 前后端集成
支持多环境配置和API相关设置
"""

import os
from datetime import timedelta
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = BASE_DIR.parent

class Config:
    """基础配置类"""
    
    # 基本配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{BASE_DIR}/blog.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # JWT配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_ALGORITHM = 'HS256'
    
    # CORS配置
    CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']
    CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization']
    CORS_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    
    # 文件上传配置
    UPLOAD_FOLDER = BASE_DIR / 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # API配置
    API_VERSION = 'v1'
    API_PREFIX = f'/api/{API_VERSION}'
    
    # 分页配置
    POSTS_PER_PAGE = 10
    COMMENTS_PER_PAGE = 20
    
    # 限流配置
    RATELIMIT_STORAGE_URL = 'memory://'
    RATELIMIT_DEFAULT = '100 per hour'
    
    # 缓存配置
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    
    # 邮件配置 (可选)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # 日志配置
    LOG_LEVEL = 'INFO'
    LOG_FILE = BASE_DIR / 'logs' / 'app.log'
    
    @staticmethod
    def init_app(app):
        """初始化应用配置"""
        # 创建必要的目录
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.LOG_FILE.parent, exist_ok=True)

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    TESTING = False
    
    # 开发环境数据库
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        f'sqlite:///{BASE_DIR}/blog_dev.db'
    
    # 开发环境CORS设置
    CORS_ORIGINS = ['*']  # 开发环境允许所有来源
    
    # 开发环境日志
    LOG_LEVEL = 'DEBUG'
    
    # JWT配置 (开发环境较短过期时间便于测试)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    DEBUG = True
    
    # 测试数据库 (内存数据库)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # 测试环境JWT配置
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)
    
    # 禁用CSRF保护
    WTF_CSRF_ENABLED = False
    
    # 测试环境限流配置
    RATELIMIT_ENABLED = False

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    TESTING = False
    
    # 生产环境数据库
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{BASE_DIR}/blog_prod.db'
    
    # 生产环境安全配置 (在init_app中检查)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'fallback-jwt-secret-key')
    
    # 生产环境CORS配置 (严格限制)
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',')
    
    # 生产环境日志
    LOG_LEVEL = 'WARNING'
    
    # 生产环境限流 (更严格)
    RATELIMIT_DEFAULT = '50 per hour'
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # 生产环境必须设置的环境变量检查
        SECRET_KEY = os.environ.get('SECRET_KEY')
        JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

        if not SECRET_KEY:
            raise ValueError("生产环境必须设置 SECRET_KEY 环境变量")
        if not JWT_SECRET_KEY:
            raise ValueError("生产环境必须设置 JWT_SECRET_KEY 环境变量")

        # 生产环境日志配置
        import logging
        from logging.handlers import RotatingFileHandler

        if not app.debug:
            file_handler = RotatingFileHandler(
                cls.LOG_FILE,
                maxBytes=10240000,
                backupCount=10
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            app.logger.setLevel(logging.INFO)
            app.logger.info('Blog API startup')

class DockerConfig(ProductionConfig):
    """Docker环境配置"""
    
    # Docker环境数据库
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://blog_user:blog_pass@db:5432/blog_db'
    
    # Docker环境Redis缓存
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL') or 'redis://redis:6379/0'
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.environ.get('REDIS_URL') or 'redis://redis:6379/1'

# 配置字典
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'docker': DockerConfig,
    'default': DevelopmentConfig
}

def get_config(config_name=None):
    """获取配置类"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    return config.get(config_name, config['default'])

# 环境变量示例文件内容
ENV_EXAMPLE = """
# Flask配置
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# 数据库配置
DATABASE_URL=sqlite:///blog.db
# 或者使用PostgreSQL
# DATABASE_URL=postgresql://username:password@localhost/blog_db

# CORS配置
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# 邮件配置 (可选)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Redis配置 (生产环境)
REDIS_URL=redis://localhost:6379/0
"""

if __name__ == '__main__':
    # 生成环境变量示例文件
    env_file = BASE_DIR / '.env.example'
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(ENV_EXAMPLE)
    print(f"✅ 环境变量示例文件已生成: {env_file}")
    
    # 显示当前配置
    config_name = os.environ.get('FLASK_ENV', 'development')
    current_config = get_config(config_name)
    print(f"📋 当前配置: {current_config.__name__}")
    print(f"🔧 调试模式: {getattr(current_config, 'DEBUG', False)}")
    print(f"🗄️  数据库: {current_config.SQLALCHEMY_DATABASE_URI}")
