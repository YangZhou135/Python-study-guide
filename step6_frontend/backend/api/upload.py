#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件上传API模块 - Stage 6 前后端集成
提供文件上传和图片处理功能
"""

import os
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from PIL import Image
import mimetypes

# 导入工具函数
from utils.response import success_response, error_response
from utils.validation import ValidationHelper

# 创建蓝图
upload_bp = Blueprint('upload', __name__)

# 配置常量
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
ALLOWED_FILE_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_IMAGE_SIZE = 5 * 1024 * 1024   # 5MB
IMAGE_QUALITY = 85
THUMBNAIL_SIZE = (300, 300)

def allowed_file(filename, file_type='image'):
    """检查文件扩展名是否允许"""
    if '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    
    if file_type == 'image':
        return extension in ALLOWED_IMAGE_EXTENSIONS
    elif file_type == 'file':
        return extension in ALLOWED_FILE_EXTENSIONS
    else:
        return extension in (ALLOWED_IMAGE_EXTENSIONS | ALLOWED_FILE_EXTENSIONS)

def get_file_size(file):
    """获取文件大小"""
    file.seek(0, 2)  # 移动到文件末尾
    size = file.tell()
    file.seek(0)     # 重置到文件开头
    return size

def generate_unique_filename(original_filename):
    """生成唯一文件名"""
    extension = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
    unique_name = f"{uuid.uuid4().hex}.{extension}" if extension else uuid.uuid4().hex
    return unique_name

def create_upload_directory(upload_type='images'):
    """创建上传目录"""
    today = datetime.now()
    upload_dir = os.path.join(
        current_app.config.get('UPLOAD_FOLDER', 'uploads'),
        upload_type,
        today.strftime('%Y'),
        today.strftime('%m')
    )
    
    os.makedirs(upload_dir, exist_ok=True)
    return upload_dir

def process_image(image_path, max_size=(1920, 1080)):
    """处理图片：压缩和调整大小"""
    try:
        with Image.open(image_path) as img:
            # 转换为RGB模式（如果是RGBA）
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # 调整大小（保持比例）
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # 保存压缩后的图片
            img.save(image_path, 'JPEG', quality=IMAGE_QUALITY, optimize=True)
            
        return True
    except Exception as e:
        current_app.logger.error(f'图片处理失败: {str(e)}')
        return False

def create_thumbnail(image_path, thumbnail_path):
    """创建缩略图"""
    try:
        with Image.open(image_path) as img:
            # 转换为RGB模式
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # 创建缩略图
            img.thumbnail(THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
            img.save(thumbnail_path, 'JPEG', quality=IMAGE_QUALITY, optimize=True)
            
        return True
    except Exception as e:
        current_app.logger.error(f'缩略图创建失败: {str(e)}')
        return False

@upload_bp.route('/image', methods=['POST'])
@jwt_required()
def upload_image():
    """
    上传图片
    
    Headers:
        Authorization: Bearer <access_token>
    
    Form Data:
        file: 图片文件
        create_thumbnail: 是否创建缩略图 (可选，默认false)
    
    Returns:
        JSON: 上传结果和文件信息
    """
    try:
        current_user_id = get_jwt_identity()
        
        # 检查是否有文件
        if 'file' not in request.files:
            return error_response('未选择文件', status_code=400)
        
        file = request.files['file']
        if file.filename == '':
            return error_response('未选择文件', status_code=400)
        
        # 检查文件类型
        if not allowed_file(file.filename, 'image'):
            return error_response(
                f'不支持的文件类型，支持的格式: {", ".join(ALLOWED_IMAGE_EXTENSIONS)}',
                status_code=400
            )
        
        # 检查文件大小
        file_size = get_file_size(file)
        if file_size > MAX_IMAGE_SIZE:
            return error_response(
                f'文件大小超过限制 ({MAX_IMAGE_SIZE // (1024*1024)}MB)',
                status_code=400
            )
        
        # 生成文件名和路径
        filename = generate_unique_filename(file.filename)
        upload_dir = create_upload_directory('images')
        file_path = os.path.join(upload_dir, filename)
        
        # 保存文件
        file.save(file_path)
        
        # 处理图片
        if not process_image(file_path):
            os.remove(file_path)
            return error_response('图片处理失败', status_code=500)
        
        # 创建缩略图（如果需要）
        thumbnail_url = None
        create_thumb = request.form.get('create_thumbnail', 'false').lower() == 'true'
        if create_thumb:
            thumbnail_filename = f"thumb_{filename}"
            thumbnail_path = os.path.join(upload_dir, thumbnail_filename)
            
            if create_thumbnail(file_path, thumbnail_path):
                thumbnail_url = f"/upload/images/{datetime.now().strftime('%Y/%m')}/{thumbnail_filename}"
        
        # 获取文件信息
        file_info = os.stat(file_path)
        mime_type = mimetypes.guess_type(file_path)[0] or 'image/jpeg'
        
        # 构建响应数据
        file_url = f"/upload/images/{datetime.now().strftime('%Y/%m')}/{filename}"
        
        response_data = {
            'file': {
                'filename': filename,
                'original_filename': file.filename,
                'url': file_url,
                'thumbnail_url': thumbnail_url,
                'size': file_info.st_size,
                'mime_type': mime_type,
                'uploaded_by': current_user_id,
                'uploaded_at': datetime.now().isoformat()
            }
        }
        
        return success_response(
            data=response_data,
            message='图片上传成功'
        )
        
    except Exception as e:
        return error_response(f'图片上传失败: {str(e)}')

@upload_bp.route('/file', methods=['POST'])
@jwt_required()
def upload_file():
    """
    上传文件
    
    Headers:
        Authorization: Bearer <access_token>
    
    Form Data:
        file: 文件
    
    Returns:
        JSON: 上传结果和文件信息
    """
    try:
        current_user_id = get_jwt_identity()
        
        # 检查是否有文件
        if 'file' not in request.files:
            return error_response('未选择文件', status_code=400)
        
        file = request.files['file']
        if file.filename == '':
            return error_response('未选择文件', status_code=400)
        
        # 检查文件类型
        if not allowed_file(file.filename, 'file'):
            return error_response(
                f'不支持的文件类型，支持的格式: {", ".join(ALLOWED_FILE_EXTENSIONS)}',
                status_code=400
            )
        
        # 检查文件大小
        file_size = get_file_size(file)
        if file_size > MAX_FILE_SIZE:
            return error_response(
                f'文件大小超过限制 ({MAX_FILE_SIZE // (1024*1024)}MB)',
                status_code=400
            )
        
        # 生成文件名和路径
        filename = generate_unique_filename(file.filename)
        upload_dir = create_upload_directory('files')
        file_path = os.path.join(upload_dir, filename)
        
        # 保存文件
        file.save(file_path)
        
        # 获取文件信息
        file_info = os.stat(file_path)
        mime_type = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
        
        # 构建响应数据
        file_url = f"/upload/files/{datetime.now().strftime('%Y/%m')}/{filename}"
        
        response_data = {
            'file': {
                'filename': filename,
                'original_filename': file.filename,
                'url': file_url,
                'size': file_info.st_size,
                'mime_type': mime_type,
                'uploaded_by': current_user_id,
                'uploaded_at': datetime.now().isoformat()
            }
        }
        
        return success_response(
            data=response_data,
            message='文件上传成功'
        )
        
    except Exception as e:
        return error_response(f'文件上传失败: {str(e)}')

@upload_bp.route('/<path:file_type>/<path:filename>')
def serve_file(file_type, filename):
    """
    提供文件访问服务
    
    Path Parameters:
        file_type: 文件类型目录 (images/files)
        filename: 文件路径 (包含年/月/文件名)
    
    Returns:
        File: 请求的文件
    """
    try:
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        file_path = os.path.join(upload_folder, file_type)
        
        return send_from_directory(file_path, filename)
        
    except Exception as e:
        return error_response(f'文件访问失败: {str(e)}', status_code=404)
