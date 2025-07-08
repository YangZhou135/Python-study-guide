#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开发服务器启动脚本
"""

import os
from app import create_app

# 设置开发环境变量
os.environ['FLASK_ENV'] = 'development'
os.environ['SECRET_KEY'] = 'dev-secret-key-for-testing'
os.environ['JWT_SECRET_KEY'] = 'dev-jwt-secret-key-for-testing'

# 加载环境变量
if os.path.exists('.env'):
    from dotenv import load_dotenv
    load_dotenv()

# 创建应用
app = create_app('development')

if __name__ == '__main__':
    print("🚀 启动个人博客管理系统 API 服务器...")
    print(f"📍 访问地址: http://localhost:5000")
    print(f"📖 API文档: http://localhost:5000/api/v1/docs")
    print(f"💚 健康检查: http://localhost:5000/health")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )
