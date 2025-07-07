#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库配置文件
支持多种数据库和环境配置
"""

import os
from datetime import timedelta

class Config:
    """基础配置类"""
    
    # 基本Flask配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # 数据库配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = 'static/uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    
    # 分页配置
    POSTS_PER_PAGE = 10
    COMMENTS_PER_PAGE = 20
    
    # 缓存配置
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    
    # 邮件配置 (如果需要)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # 日志配置
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    
    @staticmethod
    def init_app(app):
        """初始化应用配置"""
        pass

class DevelopmentConfig(Config):
    """开发环境配置"""
    
    DEBUG = True
    
    # SQLite数据库 (开发环境)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.dirname(__file__), 'instance', 'blog_dev.db')
    
    # 显示SQL语句
    SQLALCHEMY_ECHO = True
    
    # 开发工具
    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    
    # 缓存配置 (开发环境使用简单缓存)
    CACHE_TYPE = 'simple'

class TestingConfig(Config):
    """测试环境配置"""
    
    TESTING = True
    WTF_CSRF_ENABLED = False
    
    # 内存数据库 (测试环境)
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///:memory:'
    
    # 禁用CSRF保护 (测试环境)
    WTF_CSRF_ENABLED = False
    
    # 测试缓存
    CACHE_TYPE = 'null'

class ProductionConfig(Config):
    """生产环境配置"""
    
    DEBUG = False
    
    # 生产数据库 (PostgreSQL推荐)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.dirname(__file__), 'instance', 'blog.db')
    
    # 生产环境不显示SQL
    SQLALCHEMY_ECHO = False
    
    # 生产环境安全配置
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    
    # Redis缓存 (生产环境)
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # 日志配置
    LOG_TO_STDOUT = True
    
    @classmethod
    def init_app(cls, app):
        """生产环境初始化"""
        Config.init_app(app)
        
        # 日志配置
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not app.debug and not app.testing:
            if app.config['LOG_TO_STDOUT']:
                stream_handler = logging.StreamHandler()
                stream_handler.setLevel(logging.INFO)
                app.logger.addHandler(stream_handler)
            else:
                if not os.path.exists('logs'):
                    os.mkdir('logs')
                file_handler = RotatingFileHandler('logs/blog.log',
                                                 maxBytes=10240, backupCount=10)
                file_handler.setFormatter(logging.Formatter(
                    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
                file_handler.setLevel(logging.INFO)
                app.logger.addHandler(file_handler)
            
            app.logger.setLevel(logging.INFO)
            app.logger.info('Blog application startup')

class DockerConfig(ProductionConfig):
    """Docker环境配置"""
    
    @classmethod
    def init_app(cls, app):
        """Docker环境初始化"""
        ProductionConfig.init_app(app)
        
        # Docker环境日志到stdout
        import logging
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
        app.logger.setLevel(logging.INFO)

# 配置字典
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'docker': DockerConfig,
    'default': DevelopmentConfig
}

# 数据库连接字符串示例
DATABASE_EXAMPLES = {
    'sqlite': 'sqlite:///blog.db',
    'postgresql': 'postgresql://username:password@localhost/blog',
    'mysql': 'mysql://username:password@localhost/blog',
    'docker_postgres': 'postgresql://blog_user:blog_pass@db:5432/blog_db'
}

def get_config(config_name=None):
    """获取配置对象"""
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')
    return config.get(config_name, config['default'])
