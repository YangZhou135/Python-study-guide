#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API测试脚本 - Stage 6 前后端集成
测试所有API端点的功能
"""

import requests
import json
import sys

BASE_URL = 'http://localhost:5000'
API_BASE = f'{BASE_URL}/api/v1'

def test_health():
    """测试健康检查"""
    print("🔍 测试健康检查...")
    try:
        response = requests.get(f'{API_BASE}/health')
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False

def test_auth():
    """测试认证API"""
    print("\n🔐 测试认证API...")
    
    # 测试用户注册
    print("测试用户注册...")
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "Password123",
        "confirm_password": "Password123"
    }
    
    try:
        response = requests.post(f'{API_BASE}/auth/register', json=register_data)
        print(f"注册状态码: {response.status_code}")
        print(f"注册响应: {response.json()}")
        
        if response.status_code not in [200, 201, 400, 409]:  # 409是用户已存在
            return False, None
            
    except Exception as e:
        print(f"❌ 注册失败: {e}")
        return False, None
    
    # 测试用户登录
    print("测试用户登录...")
    login_data = {
        "username": "testuser",
        "password": "Password123"
    }
    
    try:
        response = requests.post(f'{API_BASE}/auth/login', json=login_data)
        print(f"登录状态码: {response.status_code}")
        result = response.json()
        print(f"登录响应: {result}")
        
        if response.status_code == 200:
            access_token = result['data']['tokens']['access_token']
            return True, access_token
        else:
            return False, None
            
    except Exception as e:
        print(f"❌ 登录失败: {e}")
        return False, None

def test_articles(token):
    """测试文章API"""
    print("\n📝 测试文章API...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # 测试创建文章
    print("测试创建文章...")
    article_data = {
        "title": "测试文章",
        "content": "这是一篇测试文章的内容",
        "tags": ["Python", "Flask"],
        "is_published": True
    }
    
    try:
        response = requests.post(f'{API_BASE}/articles', json=article_data, headers=headers)
        print(f"创建文章状态码: {response.status_code}")
        result = response.json()
        print(f"创建文章响应: {result}")
        
        if response.status_code == 201:
            article_id = result['data']['article']['id']
            
            # 测试获取文章列表
            print("测试获取文章列表...")
            response = requests.get(f'{API_BASE}/articles')
            print(f"文章列表状态码: {response.status_code}")
            print(f"文章列表响应: {response.json()}")
            
            return True, article_id
        else:
            return False, None
            
    except Exception as e:
        print(f"❌ 文章API测试失败: {e}")
        return False, None

def test_comments(token, article_id):
    """测试评论API"""
    print("\n💬 测试评论API...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # 测试创建评论
    print("测试创建评论...")
    comment_data = {
        "article_id": article_id,
        "content": "这是一条测试评论"
    }
    
    try:
        response = requests.post(f'{API_BASE}/comments', json=comment_data, headers=headers)
        print(f"创建评论状态码: {response.status_code}")
        result = response.json()
        print(f"创建评论响应: {result}")
        
        if response.status_code == 201:
            comment_id = result['data']['comment']['id']
            
            # 测试获取评论列表
            print("测试获取评论列表...")
            response = requests.get(f'{API_BASE}/comments?article_id={article_id}')
            print(f"评论列表状态码: {response.status_code}")
            print(f"评论列表响应: {response.json()}")
            
            return True, comment_id
        else:
            return False, None
            
    except Exception as e:
        print(f"❌ 评论API测试失败: {e}")
        return False, None

def test_users(token):
    """测试用户API"""
    print("\n👤 测试用户API...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # 测试获取当前用户信息
    print("测试获取当前用户信息...")
    try:
        response = requests.get(f'{API_BASE}/users/me', headers=headers)
        print(f"用户信息状态码: {response.status_code}")
        print(f"用户信息响应: {response.json()}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ 用户API测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始API测试...")
    
    # 测试健康检查
    if not test_health():
        print("❌ 健康检查失败，退出测试")
        sys.exit(1)
    
    # 测试认证
    auth_success, token = test_auth()
    if not auth_success:
        print("❌ 认证测试失败，退出测试")
        sys.exit(1)
    
    # 测试文章
    articles_success, article_id = test_articles(token)
    if not articles_success:
        print("❌ 文章API测试失败")
    else:
        print("✅ 文章API测试成功")
        
        # 测试评论
        comments_success, comment_id = test_comments(token, article_id)
        if not comments_success:
            print("❌ 评论API测试失败")
        else:
            print("✅ 评论API测试成功")
    
    # 测试用户
    users_success = test_users(token)
    if not users_success:
        print("❌ 用户API测试失败")
    else:
        print("✅ 用户API测试成功")
    
    print("\n🎉 API测试完成！")

if __name__ == '__main__':
    main()
