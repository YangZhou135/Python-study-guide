#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文章相关API
提供文章的CRUD操作、搜索、点赞等功能
"""

import asyncio
from flask import Blueprint, request, Response
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError
from sqlalchemy import or_, desc, asc

# 导入数据库模型
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../step5_database'))
from models import db, Article, User, Tag, Comment

# 导入工具函数
from utils.response import (
    success_response, error_response, validation_error_response,
    not_found_response, paginated_response, forbidden_response
)
from utils.validation import (
    ArticleCreateSchema, ArticleUpdateSchema, PaginationSchema, SearchSchema,
    validate_request_data, format_validation_errors
)
from middleware.auth import article_owner_required

# 创建蓝图
articles_bp = Blueprint('articles', __name__)

@articles_bp.route('', methods=['GET'])
def get_articles():
    """
    获取文章列表
    
    Query Parameters:
        page: 页码 (默认: 1)
        per_page: 每页数量 (默认: 10)
        published: 是否只显示已发布文章 (默认: true)
        author: 作者用户名
        tag: 标签名称
        sort: 排序字段 (created_at, updated_at, views, likes)
        order: 排序方向 (asc, desc)
    
    Returns:
        JSON: 文章列表和分页信息
    """
    try:
        # 获取查询参数
        args = request.args.to_dict()
        
        # 验证分页参数
        pagination_data = validate_request_data(PaginationSchema, {
            'page': args.get('page', 1),
            'per_page': args.get('per_page', 10)
        })
        
        # 构建查询
        query = Article.query
        
        # 过滤已发布文章
        published = args.get('published', 'true').lower() == 'true'
        if published:
            query = query.filter(Article.is_published == True)
        
        # 按作者过滤
        author = args.get('author')
        if author:
            query = query.join(User).filter(User.username == author)
        
        # 按标签过滤
        tag = args.get('tag')
        if tag:
            query = query.join(Article.tags).filter(Tag.name == tag)
        
        # 排序
        sort_field = args.get('sort', 'created_at')
        order = args.get('order', 'desc')
        
        sort_column = getattr(Article, sort_field, Article.created_at)
        if order == 'asc':
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        # 分页查询
        pagination = query.paginate(
            page=pagination_data['page'],
            per_page=pagination_data['per_page'],
            error_out=False
        )
        
        # 序列化文章数据
        articles_data = []
        for article in pagination.items:
            article_data = {
                'id': article.id,
                'title': article.title,
                'summary': article.summary or article.content[:200] + '...',
                'slug': article.slug,
                'is_published': article.is_published,
                'featured_image': article.featured_image,
                'views': article.views,
                'likes': article.likes,
                'created_at': article.created_at.isoformat(),
                'updated_at': article.updated_at.isoformat(),
                'author': {
                    'id': article.author.id,
                    'username': article.author.username
                },
                'tags': [{'id': tag.id, 'name': tag.name} for tag in article.tags],
                'comment_count': article.comment_count
            }
            articles_data.append(article_data)
        
        return paginated_response(
            data=articles_data,
            page=pagination.page,
            per_page=pagination.per_page,
            total=pagination.total,
            message='获取文章列表成功'
        )
        
    except ValidationError as e:
        return validation_error_response(
            errors=format_validation_errors(e.messages)
        )
    except Exception as e:
        return error_response(f'获取文章列表失败: {str(e)}')

@articles_bp.route('/<int:article_id>', methods=['GET'])
def get_article(article_id):
    """
    获取文章详情
    
    Path Parameters:
        article_id: 文章ID
    
    Returns:
        JSON: 文章详情
    """
    try:
        article = Article.query.get(article_id)
        
        if not article:
            return not_found_response('文章')
        
        # 检查文章是否已发布 (除非是作者本人)
        current_user_id = None
        try:
            from flask_jwt_extended import verify_jwt_in_request
            verify_jwt_in_request(optional=True)
            current_user_id = get_jwt_identity()
        except:
            pass
        
        if not article.is_published and article.author_id != current_user_id:
            return not_found_response('文章')
        
        # 增加浏览量 (如果不是作者本人)
        if current_user_id != article.author_id:
            article.add_view()
            db.session.commit()
        
        # 序列化文章数据
        article_data = {
            'id': article.id,
            'title': article.title,
            'content': article.content,
            'summary': article.summary,
            'slug': article.slug,
            'is_published': article.is_published,
            'featured_image': article.featured_image,
            'views': article.views,
            'likes': article.likes,
            'created_at': article.created_at.isoformat(),
            'updated_at': article.updated_at.isoformat(),
            'author': {
                'id': article.author.id,
                'username': article.author.username
            },
            'tags': [{'id': tag.id, 'name': tag.name} for tag in article.tags],
            'comment_count': article.comment_count
        }
        
        return success_response(
            data={'article': article_data},
            message='获取文章详情成功'
        )
        
    except Exception as e:
        return error_response(f'获取文章详情失败: {str(e)}')

# 异步任务示例
async def send_notification(article_title):
    """模拟一个耗时的异步通知任务"""
    print(f"开始为文章 '{article_title}' 发送通知...")
    await asyncio.sleep(2)  # 模拟网络延迟
    print(f"✅ 对文章 '{article_title}' 的通知发送完成。")

@articles_bp.route('', methods=['POST'])
@jwt_required()
def create_article():
    """
    创建文章
    
    Headers:
        Authorization: Bearer <access_token>
    
    Body:
        title: 文章标题
        content: 文章内容
        summary: 文章摘要 (可选)
        tags: 标签列表 (可选)
        is_published: 是否发布 (默认: false)
        featured_image: 特色图片URL (可选)
    
    Returns:
        JSON: 创建的文章信息
    """
    try:
        # 验证请求数据
        data = validate_request_data(ArticleCreateSchema, request.get_json() or {})
        
        current_user_id = get_jwt_identity()
        
        # 创建文章
        article = Article(
            title=data['title'],
            content=data['content'],
            author_id=int(current_user_id),
            tags=data.get('tags', [])
        )

        # 设置其他属性
        article.summary = data.get('summary', '')
        article.is_published = data.get('is_published', False)
        article.featured_image = data.get('featured_image')

        
        db.session.add(article)
        db.session.commit()

        # --- 异步任务演示 ---
        # 在同步的Flask路由中运行一个异步函数
        # 注意：asyncio.run()会阻塞当前线程直到任务完成。
        # 在生产环境中，通常会使用任务队列（如Celery）来处理后台任务，以避免阻塞Web服务器。
        # 这里的演示主要是为了展示async/await的语法和用法。
        try:
            asyncio.run(send_notification(article.title))
        except RuntimeError:
            # 如果当前线程已经有事件循环在运行，
            # asyncio.run()会抛出RuntimeError。
            # 此时可以使用更底层的API来运行。
            loop = asyncio.get_event_loop()
            loop.create_task(send_notification(article.title))

        
        # 序列化文章数据
        article_data = {
            'id': article.id,
            'title': article.title,
            'content': article.content,
            'summary': article.summary,
            'slug': article.slug,
            'is_published': article.is_published,
            'featured_image': article.featured_image,
            'views': article.views,
            'likes': article.likes,
            'created_at': article.created_at.isoformat(),
            'updated_at': article.updated_at.isoformat(),
            'author': {
                'id': article.author.id,
                'username': article.author.username
            },
            'tags': [{'id': tag.id, 'name': tag.name} for tag in article.tags],
            'comment_count': 0
        }
        
        return success_response(
            data={'article': article_data},
            message='文章创建成功',
            status_code=201
        )
        
    except ValidationError as e:
        return validation_error_response(
            errors=format_validation_errors(e.messages)
        )
    except Exception as e:
        return error_response(f'文章创建失败: {str(e)}')

@articles_bp.route('/<int:article_id>', methods=['PUT'])
@article_owner_required
def update_article(article_id):
    """
    更新文章

    Path Parameters:
        article_id: 文章ID

    Headers:
        Authorization: Bearer <access_token>

    Body:
        title: 文章标题 (可选)
        content: 文章内容 (���选)
        summary: 文章摘要 (可选)
        tags: 标签列表 (可选)
        is_published: 是否发布 (可选)
        featured_image: 特色图片URL (可选)

    Returns:
        JSON: 更新后的文章信息
    """
    try:
        article = Article.query.get(article_id)
        if not article:
            return not_found_response('文章')

        # 验证请求数据
        data = validate_request_data(ArticleUpdateSchema, request.get_json() or {})

        # 更新文章字段
        if 'title' in data:
            article.title = data['title']
        if 'content' in data:
            article.content = data['content']
        if 'summary' in data:
            article.summary = data['summary']
        if 'is_published' in data:
            article.is_published = data['is_published']
        if 'featured_image' in data:
            article.featured_image = data['featured_image']

        # 更新标签
        if 'tags' in data:
            # 清除现有标签
            article.tags.clear()

            # 添加新标签
            tag_names = data['tags']
            for tag_name in tag_names:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                article.tags.append(tag)

        db.session.commit()

        # 序列化文章数据
        article_data = {
            'id': article.id,
            'title': article.title,
            'content': article.content,
            'summary': article.summary,
            'slug': article.slug,
            'is_published': article.is_published,
            'featured_image': article.featured_image,
            'views': article.views,
            'likes': article.likes,
            'created_at': article.created_at.isoformat(),
            'updated_at': article.updated_at.isoformat(),
            'author': {
                'id': article.author.id,
                'username': article.author.username
            },
            'tags': [{'id': tag.id, 'name': tag.name} for tag in article.tags],
            'comment_count': article.comment_count
        }

        return success_response(
            data={'article': article_data},
            message='文章��新成功'
        )

    except ValidationError as e:
        return validation_error_response(
            errors=format_validation_errors(e.messages)
        )
    except Exception as e:
        return error_response(f'文章更新失败: {str(e)}')

@articles_bp.route('/<int:article_id>', methods=['DELETE'])
@article_owner_required
def delete_article(article_id):
    """
    删除文章

    Path Parameters:
        article_id: 文章ID

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        JSON: 删除结果
    """
    try:
        article = Article.query.get(article_id)
        if not article:
            return not_found_response('文章')

        # 删除文章 (级联删除评论)
        db.session.delete(article)
        db.session.commit()

        return success_response(message='文章删除成功')

    except Exception as e:
        return error_response(f'文章删除失败: {str(e)}')

@articles_bp.route('/<int:article_id>/like', methods=['POST'])
@jwt_required()
def like_article(article_id):
    """
    点赞文章

    Path Parameters:
        article_id: 文章ID

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        JSON: 点赞结果
    """
    try:
        article = Article.query.get(article_id)
        if not article:
            return not_found_response('文章')

        if not article.is_published:
            return not_found_response('文章')

        # 增加点赞数
        article.add_like()
        db.session.commit()

        return success_response(
            data={'likes': article.likes},
            message='点赞成功'
        )

    except Exception as e:
        return error_response(f'点赞失败: {str(e)}')

@articles_bp.route('/search', methods=['GET'])
def search_articles():
    """
    搜索文章

    Query Parameters:
        q: 搜索关键词
        category: 分类 (可选)
        sort: 排序字段 (默认: created_at)
        order: 排序方向 (默认: desc)
        page: 页码 (默认: 1)
        per_page: 每页数量 (默认: 10)

    Returns:
        JSON: 搜索结果和分页信息
    """
    try:
        # 获取查询参数
        args = request.args.to_dict()

        # 验证搜索参数
        search_data = validate_request_data(SearchSchema, args)
        pagination_data = validate_request_data(PaginationSchema, {
            'page': args.get('page', 1),
            'per_page': args.get('per_page', 10)
        })

        # 构建搜索查询
        query = Article.query.filter(Article.is_published == True)

        # 关键词搜索
        keyword = search_data['q']
        query = query.filter(
            or_(
                Article.title.contains(keyword),
                Article.content.contains(keyword),
                Article.summary.contains(keyword)
            )
        )

        # 分类过滤
        category = search_data.get('category')
        if category:
            query = query.join(Article.tags).filter(Tag.name == category)

        # 排序
        sort_field = search_data['sort']
        order = search_data['order']

        sort_column = getattr(Article, sort_field, Article.created_at)
        if order == 'asc':
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))

        # 分页查询
        pagination = query.paginate(
            page=pagination_data['page'],
            per_page=pagination_data['per_page'],
            error_out=False
        )

        # 序列化搜索结果
        articles_data = []
        for article in pagination.items:
            article_data = {
                'id': article.id,
                'title': article.title,
                'summary': article.summary or article.content[:200] + '...',
                'slug': article.slug,
                'featured_image': article.featured_image,
                'views': article.views,
                'likes': article.likes,
                'created_at': article.created_at.isoformat(),
                'author': {
                    'id': article.author.id,
                    'username': article.author.username
                },
                'tags': [{'id': tag.id, 'name': tag.name} for tag in article.tags]
            }
            articles_data.append(article_data)

        return paginated_response(
            data=articles_data,
            page=pagination.page,
            per_page=pagination.per_page,
            total=pagination.total,
            message=f'搜索到 {pagination.total} 篇文章'
        )

    except ValidationError as e:
        return validation_error_response(
            errors=format_validation_errors(e.messages)
        )
    except Exception as e:
        return error_response(f'搜索失败: {str(e)}')


@articles_bp.route('/export', methods=['GET'])
@jwt_required()
def export_articles():
    """
    导出所有文章为CSV文件 (使用生成器)
    """
    def generate_csv():
        # CSV header
        yield 'id,title,author,tags,views,likes,created_at\n'
        
        # 查询所有文章
        articles = Article.query.order_by(Article.created_at.desc()).all()
        
        for article in articles:
            tags = ';'.join([tag.name for tag in article.tags])
            row = f'"{article.id}","{article.title}","{article.author.username}","{tags}",{article.views},{article.likes},"{article.created_at.isoformat()}"\n'
            yield row

    headers = {
        'Content-Disposition': 'attachment; filename="articles_export.csv"',
        'Content-Type': 'text/csv; charset=utf-8'
    }
    
    return Response(generate_csv(), headers=headers)
