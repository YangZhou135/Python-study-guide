#!/usr/bin/env python3
"""
上传API测试脚本
"""

import requests
import io
from PIL import Image

# API配置
API_BASE = 'http://localhost:5000/api/v1'

def test_upload_api():
    """测试上传API"""
    print("🚀 开始上传API测试...")
    
    # 先登录获取token
    print("🔐 登录获取token...")
    login_data = {
        "username": "testuser",
        "password": "Password123"
    }
    
    try:
        response = requests.post(f'{API_BASE}/auth/login', json=login_data)
        if response.status_code != 200:
            print(f"❌ 登录失败: {response.status_code}")
            return
        
        token = response.json()['data']['tokens']['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        print("✅ 登录成功")
        
    except Exception as e:
        print(f"❌ 登录失败: {e}")
        return
    
    # 创建测试图片
    print("📸 创建测试图片...")
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    # 测试图片上传
    print("📤 测试图片上传...")
    files = {
        'file': ('test.png', img_bytes, 'image/png')
    }
    
    try:
        response = requests.post(f'{API_BASE}/upload/image', files=files, headers=headers)
        print(f"上传状态码: {response.status_code}")
        print(f"上传响应: {response.json()}")
        
        if response.status_code == 200:
            print("✅ 图片上传测试成功")
        else:
            print("❌ 图片上传测试失败")
            
    except Exception as e:
        print(f"❌ 图片上传失败: {e}")
    
    # 测试文件上传
    print("📄 测试文件上传...")
    text_content = "这是一个测试文件内容"
    text_bytes = io.BytesIO(text_content.encode('utf-8'))
    
    files = {
        'file': ('test.txt', text_bytes, 'text/plain')
    }
    
    try:
        response = requests.post(f'{API_BASE}/upload/file', files=files, headers=headers)
        print(f"文件上传状态码: {response.status_code}")
        print(f"文件上传响应: {response.json()}")
        
        if response.status_code == 200:
            print("✅ 文件上传测试成功")
        else:
            print("❌ 文件上传测试失败")
            
    except Exception as e:
        print(f"❌ 文件上传失败: {e}")
    
    print("🎉 上传API测试完成！")

if __name__ == '__main__':
    test_upload_api()
