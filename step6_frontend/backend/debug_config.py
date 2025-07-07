#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置调试脚本
"""

from app import create_app

app = create_app()

with app.app_context():
    print("Flask配置:")
    print(f"SECRET_KEY: {app.config.get('SECRET_KEY')}")
    print(f"JWT_SECRET_KEY: {app.config.get('JWT_SECRET_KEY')}")
    print(f"JWT_ACCESS_TOKEN_EXPIRES: {app.config.get('JWT_ACCESS_TOKEN_EXPIRES')}")
    print(f"JWT_ALGORITHM: {app.config.get('JWT_ALGORITHM')}")
