#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask表单定义
使用Flask-WTF处理表单验证
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SelectField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional
from flask_wtf.file import FileAllowed

class LoginForm(FlaskForm):
    """登录表单"""
    username = StringField('用户名', validators=[
        DataRequired(message='用户名不能为空'),
        Length(min=3, max=20, message='用户名长度必须在3-20个字符之间')
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不能为空')
    ])
    remember_me = BooleanField('记住我')

class RegisterForm(FlaskForm):
    """注册表单"""
    username = StringField('用户名', validators=[
        DataRequired(message='用户名不能为空'),
        Length(min=3, max=20, message='用户名长度必须在3-20个字符之间')
    ])
    email = StringField('邮箱', validators=[
        DataRequired(message='邮箱不能为空'),
        Email(message='请输入有效的邮箱地址')
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不能为空'),
        Length(min=6, message='密码长度至少6个字符')
    ])
    password2 = PasswordField('确认密码', validators=[
        DataRequired(message='请确认密码'),
        EqualTo('password', message='两次输入的密码不一致')
    ])

class ArticleForm(FlaskForm):
    """文章表单"""
    title = StringField('标题', validators=[
        DataRequired(message='标题不能为空'),
        Length(min=1, max=200, message='标题长度必须在1-200个字符之间')
    ])
    content = TextAreaField('内容', validators=[
        DataRequired(message='内容不能为空'),
        Length(min=10, message='内容至少需要10个字符')
    ])
    summary = TextAreaField('摘要', validators=[
        Optional(),
        Length(max=500, message='摘要不能超过500个字符')
    ])
    tags = StringField('标签', validators=[
        Optional(),
        Length(max=200, message='标签总长度不能超过200个字符')
    ])
    featured_image = FileField('特色图片', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], message='只支持jpg、jpeg、png、gif格式的图片')
    ])
    is_published = BooleanField('立即发布')

class CommentForm(FlaskForm):
    """评论表单"""
    content = TextAreaField('评论内容', validators=[
        DataRequired(message='评论内容不能为空'),
        Length(min=1, max=1000, message='评论长度必须在1-1000个字符之间')
    ])

class SearchForm(FlaskForm):
    """搜索表单"""
    query = StringField('搜索关键词', validators=[
        DataRequired(message='请输入搜索关键词'),
        Length(min=1, max=100, message='搜索关键词长度必须在1-100个字符之间')
    ])

class ProfileForm(FlaskForm):
    """个人资料表单"""
    email = StringField('邮箱', validators=[
        DataRequired(message='邮箱不能为空'),
        Email(message='请输入有效的邮箱地址')
    ])
    current_password = PasswordField('当前密码', validators=[
        Optional()
    ])
    new_password = PasswordField('新密码', validators=[
        Optional(),
        Length(min=6, message='密码长度至少6个字符')
    ])
    new_password2 = PasswordField('确认新密码', validators=[
        Optional(),
        EqualTo('new_password', message='两次输入的密码不一致')
    ])

class ChangePasswordForm(FlaskForm):
    """修改密码表单"""
    current_password = PasswordField('当前密码', validators=[
        DataRequired(message='请输入当前密码')
    ])
    new_password = PasswordField('新密码', validators=[
        DataRequired(message='请输入新密码'),
        Length(min=6, message='密码长度至少6个字符')
    ])
    new_password2 = PasswordField('确认新密码', validators=[
        DataRequired(message='请确认新密码'),
        EqualTo('new_password', message='两次输入的密码不一致')
    ])
