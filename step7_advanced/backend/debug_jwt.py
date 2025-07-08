#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JWT调试脚本
"""

import requests
import jwt
import json

# 获取token
login_data = {
    "username": "testuser",
    "password": "Password123"
}

response = requests.post('http://localhost:5000/api/v1/auth/login', json=login_data)
print(f"登录响应: {response.status_code}")
result = response.json()

if response.status_code == 200:
    token = result['data']['tokens']['access_token']
    print(f"Token: {token}")
    
    # 解码token查看内容
    try:
        # 不验证签名，只查看内容
        decoded = jwt.decode(token, options={"verify_signature": False})
        print(f"Token内容: {json.dumps(decoded, indent=2)}")
    except Exception as e:
        print(f"解码失败: {e}")
    
    # 测试使用token访问API
    headers = {'Authorization': f'Bearer {token}'}
    test_response = requests.get('http://localhost:5000/api/v1/users/me', headers=headers)
    print(f"API测试响应: {test_response.status_code}")
    print(f"API测试内容: {test_response.json()}")
else:
    print(f"登录失败: {result}")
