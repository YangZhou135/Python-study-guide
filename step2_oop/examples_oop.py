#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python面向对象编程概念示例
对比函数式编程，学习OOP核心概念
"""

from models import Article, User, BlogManager

def demonstrate_classes_and_objects():
    """演示类和对象的基本概念"""
    print("=== 类和对象基础 ===")
    
    # 创建对象实例
    article1 = Article("Python OOP入门", "学习面向对象编程的基础概念", "张三", ["Python", "OOP"])
    article2 = Article("设计模式", "常用的设计模式介绍", "李四", ["设计模式", "编程"])
    
    print("创建的文章对象:")
    print(f"文章1: {article1}")
    print(f"文章2: {article2}")
    
    # 访问对象属性
    print(f"\n文章1详情:")
    print(f"  ID: {article1.id}")
    print(f"  标题: {article1.title}")
    print(f"  作者: {article1.author}")
    print(f"  标签: {article1.tags}")
    print(f"  创建时间: {article1.created_at}")
    
    # 调用对象方法
    print(f"\n调用对象方法:")
    print(f"  浏览前: {article1.views} 次")
    article1.add_view()
    article1.add_view()
    print(f"  浏览后: {article1.views} 次")
    
    article1.add_like()
    print(f"  点赞数: {article1.likes}")
    
    # 类属性和类方法
    print(f"\n类属性和方法:")
    print(f"  文章总数: {Article.get_article_count()}")
    print()

def demonstrate_encapsulation():
    """演示封装概念"""
    print("=== 封装和属性控制 ===")
    
    article = Article("封装示例", "演示Python的封装特性", "程序员")
    
    # 属性访问控制
    print("属性访问:")
    print(f"  标题: {article.title}")
    
    # 尝试修改属性
    print("\n修改属性:")
    try:
        article.title = "新标题"
        print(f"  修改后标题: {article.title}")
    except Exception as e:
        print(f"  修改失败: {e}")
    
    # 尝试设置无效值
    print("\n设置无效值:")
    try:
        article.title = ""  # 空标题
    except ValueError as e:
        print(f"  验证失败: {e}")
    
    # 只读属性
    print(f"\n只读属性:")
    print(f"  文章ID: {article.id} (只读)")
    print(f"  作者: {article.author} (只读)")
    
    # 受控的方法调用
    print(f"\n受控的方法调用:")
    print(f"  添加标签前: {article.tags}")
    article.add_tag("新标签")
    article.add_tag("Python")  # 重复标签不会添加
    print(f"  添加标签后: {article.tags}")
    print()

def demonstrate_inheritance():
    """演示继承概念"""
    print("=== 继承和多态 ===")
    
    # 定义继承示例类
    class SpecialArticle(Article):
        """特殊文章类 - 继承自Article"""
        
        def __init__(self, title, content, author, tags=None, is_featured=False):
            super().__init__(title, content, author, tags)
            self.is_featured = is_featured
        
        def add_view(self):
            """重写父类方法 - 特殊文章浏览量加倍"""
            super().add_view()
            if self.is_featured:
                super().add_view()  # 精选文章额外加一次
        
        def __str__(self):
            """重写字符串表示"""
            base_str = super().__str__()
            return f"⭐ {base_str}" if self.is_featured else base_str
    
    # 创建普通文章和特殊文章
    normal_article = Article("普通文章", "这是一篇普通文章", "作者A")
    special_article = SpecialArticle("精选文章", "这是一篇精选文章", "作者B", ["精选"], True)
    
    print("文章类型:")
    print(f"  普通文章: {normal_article}")
    print(f"  特殊文章: {special_article}")
    
    # 多态性演示
    print(f"\n多态性演示 - 浏览量增加:")
    articles = [normal_article, special_article]
    
    for article in articles:
        print(f"  {article.title}: 浏览前 {article.views}")
        article.add_view()  # 同样的方法调用，不同的行为
        print(f"  {article.title}: 浏览后 {article.views}")
    
    # isinstance检查
    print(f"\n类型检查:")
    print(f"  normal_article是Article? {isinstance(normal_article, Article)}")
    print(f"  special_article是Article? {isinstance(special_article, Article)}")
    print(f"  special_article是SpecialArticle? {isinstance(special_article, SpecialArticle)}")
    print()

def demonstrate_special_methods():
    """演示特殊方法（魔术方法）"""
    print("=== 特殊方法 ===")
    
    article1 = Article("Python基础", "Python编程基础教程内容很长很详细", "张三", ["Python"])
    article2 = Article("Java入门", "Java编程入门", "李四", ["Java"])
    
    # __str__ 和 __repr__
    print("字符串表示:")
    print(f"  str(article1): {str(article1)}")
    print(f"  repr(article1): {repr(article1)}")
    
    # __len__
    print(f"\n长度方法:")
    print(f"  len(article1): {len(article1)} 字符")
    print(f"  len(article2): {len(article2)} 字符")
    
    # __contains__
    print(f"\n包含检查:")
    print(f"  'Python' in article1: {'Python' in article1}")
    print(f"  'Java' in article1: {'Java' in article1}")
    print(f"  '基础' in article1: {'基础' in article1}")
    
    # __eq__ 和 __lt__
    print(f"\n比较操作:")
    print(f"  article1 == article2: {article1 == article2}")
    print(f"  article1 < article2: {article1 < article2}")  # 按创建时间比较
    
    # 排序
    import time
    time.sleep(0.01)  # 确保时间差异
    article3 = Article("最新文章", "最新发布的文章", "王五")
    
    articles = [article3, article1, article2]
    print(f"\n排序前: {[a.title for a in articles]}")
    articles.sort()  # 使用 __lt__ 方法排序
    print(f"排序后: {[a.title for a in articles]}")
    print()

def demonstrate_composition():
    """演示组合关系"""
    print("=== 组合关系 ===")
    
    # 创建博客管理器（组合了多个对象）
    blog_manager = BlogManager()
    
    # 添加用户
    user1 = blog_manager.add_user("张三", "zhangsan@example.com")
    user2 = blog_manager.add_user("李四", "lisi@example.com")
    
    print("创建用户:")
    print(f"  用户1: {user1}")
    print(f"  用户2: {user2}")
    
    # 用户创建文章
    article1 = user1.create_article("Python学习", "学习Python的心得", ["Python", "学习"])
    article2 = user2.create_article("Web开发", "Web开发技术栈", ["Web", "开发"])
    
    # 添加到管理器
    blog_manager.add_article(article1)
    blog_manager.add_article(article2)
    
    print(f"\n博客系统状态:")
    print(f"  {blog_manager}")
    
    # 展示对象间的关系
    print(f"\n对象关系:")
    print(f"  用户1的文章: {[a.title for a in user1.articles]}")
    print(f"  管理器中的文章: {[a.title for a in blog_manager.get_all_articles()]}")
    
    # 统计信息
    stats = blog_manager.get_statistics()
    print(f"\n统计信息: {stats}")
    print()

def demonstrate_property_decorators():
    """演示属性装饰器"""
    print("=== 属性装饰器 ===")
    
    # 创建用户对象
    user = User("测试用户", "test@example.com")
    
    print("属性访问:")
    print(f"  用户名: {user.username}")
    print(f"  邮箱: {user.email}")
    
    # 修改邮箱（通过setter）
    print(f"\n修改邮箱:")
    print(f"  原邮箱: {user.email}")
    user.email = "newemail@example.com"
    print(f"  新邮箱: {user.email}")
    
    # 尝试设置无效邮箱
    print(f"\n设置无效邮箱:")
    try:
        user.email = "invalid-email"
    except ValueError as e:
        print(f"  验证失败: {e}")
    
    # 只读属性
    print(f"\n只读属性:")
    print(f"  用户名: {user.username} (只读)")
    print(f"  注册时间: {user.created_at} (只读)")
    
    # 计算属性
    article = user.create_article("测试文章", "测试内容", ["测试"])
    article.add_view()
    article.add_view()
    
    print(f"\n计算属性:")
    print(f"  文章数量: {user.get_article_count()}")
    print(f"  总浏览量: {user.get_total_views()}")
    print()

def compare_functional_vs_oop():
    """对比函数式编程和面向对象编程"""
    print("=== 函数式 vs 面向对象对比 ===")
    
    print("函数式方式 (第1阶段):")
    print("""
    # 数据和函数分离
    article = {"title": "标题", "content": "内容", "views": 0}
    
    def add_view(article):
        article["views"] += 1
    
    def get_summary(article, max_length=50):
        return article["content"][:max_length] + "..."
    """)
    
    print("\n面向对象方式 (第2阶段):")
    print("""
    # 数据和方法封装在一起
    class Article:
        def __init__(self, title, content):
            self.title = title
            self.content = content
            self.views = 0
        
        def add_view(self):
            self.views += 1
        
        def get_summary(self, max_length=50):
            return self.content[:max_length] + "..."
    """)
    
    print("\n优势对比:")
    print("函数式编程:")
    print("  ✅ 简单直接")
    print("  ✅ 易于理解")
    print("  ❌ 数据和操作分离")
    print("  ❌ 难以维护复杂系统")
    
    print("\n面向对象编程:")
    print("  ✅ 数据和方法封装")
    print("  ✅ 代码复用性强")
    print("  ✅ 易于维护和扩展")
    print("  ✅ 更好的代码组织")
    print("  ❌ 学习曲线较陡")
    print()

def main():
    """主函数 - 运行所有示例"""
    print("🏗️ Python面向对象编程概念示例")
    print("=" * 50)
    
    demonstrate_classes_and_objects()
    demonstrate_encapsulation()
    demonstrate_inheritance()
    demonstrate_special_methods()
    demonstrate_composition()
    demonstrate_property_decorators()
    compare_functional_vs_oop()
    
    print("🎉 面向对象编程概念示例完成！")
    print("💡 提示：尝试修改代码，创建自己的类和对象")

if __name__ == "__main__":
    main()
