#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stage 6 前后端集成测试脚本
验证前后端API连接和基本功能
"""

import requests
import json
import time
from datetime import datetime

# API配置
BACKEND_URL = "http://127.0.0.1:5000/api/v1"
FRONTEND_URL = "http://localhost:5173"

def test_backend_health():
    """测试后端健康状态"""
    print("🔍 测试后端健康状态...")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 后端健康状态: {data['status']}")
            print(f"   数据库状态: {data['database']}")
            return True
        else:
            print(f"❌ 后端健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 后端连接失败: {e}")
        return False

def test_frontend_access():
    """测试前端访问"""
    print("\n🔍 测试前端访问...")
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print("✅ 前端服务正常访问")
            return True
        else:
            print(f"❌ 前端访问失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 前端连接失败: {e}")
        return False

def test_articles_api():
    """测试文章API"""
    print("\n🔍 测试文章API...")
    try:
        response = requests.get(f"{BACKEND_URL}/articles", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 'SUCCESS':
                articles = data.get('data', [])
                print(f"✅ 文章API正常，返回 {len(articles)} 篇文章")
                if articles:
                    print(f"   示例文章: {articles[0]['title']}")
                return True
            else:
                print(f"❌ 文章API返回错误: {data}")
                return False
        else:
            print(f"❌ 文章API请求失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 文章API连接失败: {e}")
        return False

def test_user_registration():
    """测试用户注册API"""
    print("\n🔍 测试用户注册API...")
    test_user = {
        "username": f"testuser_{int(time.time())}",
        "email": f"test_{int(time.time())}@example.com",
        "password": "TestPassword123",
        "confirm_password": "TestPassword123"
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/auth/register",
            json=test_user,
            timeout=5
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            if data.get('code') == 'SUCCESS':
                print("✅ 用户注册API正常")
                return True, test_user
            else:
                print(f"❌ 用户注册失败: {data}")
                return False, None
        else:
            print(f"❌ 用户注册请求失败: {response.status_code}")
            print(f"   响应内容: {response.text}")
            return False, None
    except Exception as e:
        print(f"❌ 用户注册API连接失败: {e}")
        return False, None

def test_user_login(user_data):
    """测试用户登录API"""
    print("\n🔍 测试用户登录API...")
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/auth/login",
            json=login_data,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 'SUCCESS':
                print("✅ 用户登录API正常")
                token = data['data']['tokens']['access_token']
                return True, token
            else:
                print(f"❌ 用户登录失败: {data}")
                return False, None
        else:
            print(f"❌ 用户登录请求失败: {response.status_code}")
            return False, None
    except Exception as e:
        print(f"❌ 用户登录API连接失败: {e}")
        return False, None

def main():
    """主测试函数"""
    print("🚀 开始 Stage 6 前后端集成测试")
    print("=" * 50)
    
    # 测试结果统计
    tests_passed = 0
    total_tests = 5
    
    # 1. 测试后端健康状态
    if test_backend_health():
        tests_passed += 1
    
    # 2. 测试前端访问
    if test_frontend_access():
        tests_passed += 1
    
    # 3. 测试文章API
    if test_articles_api():
        tests_passed += 1
    
    # 4. 测试用户注册
    registration_success, test_user = test_user_registration()
    if registration_success:
        tests_passed += 1
        
        # 5. 测试用户登录
        if test_user_login(test_user):
            tests_passed += 1
    else:
        print("\n⚠️  跳过登录测试（注册失败）")
    
    # 输出测试结果
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {tests_passed}/{total_tests} 通过")
    
    if tests_passed == total_tests:
        print("🎉 所有测试通过！前后端集成成功！")
        print("\n📝 下一步建议:")
        print("   1. 在浏览器中访问 http://localhost:5173")
        print("   2. 测试用户注册和登录功能")
        print("   3. 测试文章创建和管理功能")
        print("   4. 测试评论系统功能")
    else:
        print("⚠️  部分测试失败，请检查相关服务状态")
    
    print("\n🔗 服务地址:")
    print(f"   前端: {FRONTEND_URL}")
    print(f"   后端: {BACKEND_URL}")

if __name__ == "__main__":
    main()
