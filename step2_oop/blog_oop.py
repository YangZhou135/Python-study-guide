#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
面向对象版本的博客管理器
学习Python面向对象编程实践
"""

from models import Article, User, BlogManager
from typing import Optional

class BlogApp:
    """博客应用程序类"""
    
    def __init__(self):
        """初始化应用程序"""
        self.blog_manager = BlogManager()
        self.current_user: Optional[User] = None
        self._setup_sample_data()
    
    def _setup_sample_data(self):
        """设置示例数据"""
        # 创建示例用户
        try:
            user1 = self.blog_manager.add_user("张三", "zhangsan@example.com")
            user2 = self.blog_manager.add_user("李四", "lisi@example.com")
            
            # 创建示例文章
            article1 = user1.create_article(
                "Python面向对象编程入门",
                "今天学习了Python的类和对象概念，发现OOP能让代码更加组织化和可维护。",
                ["Python", "OOP", "编程"]
            )
            
            article2 = user1.create_article(
                "从函数式到面向对象的转变",
                "通过重构博客管理系统，深刻理解了面向对象编程的优势。",
                ["Python", "重构", "设计模式"]
            )
            
            article3 = user2.create_article(
                "前端开发者学习Python后端",
                "作为前端开发者，学习Python后端开发让我对全栈开发有了新的认识。",
                ["Python", "前端", "后端", "全栈"]
            )
            
            # 添加文章到管理器
            for user in [user1, user2]:
                for article in user.articles:
                    self.blog_manager.add_article(article)
            
            # 模拟一些浏览量
            article1.add_view()
            article1.add_view()
            article1.add_like()
            article2.add_view()
            article3.add_view()
            article3.add_view()
            article3.add_view()
            
        except Exception as e:
            print(f"设置示例数据时出错: {e}")
    
    def show_menu(self):
        """显示主菜单"""
        print("\n🐍 Python面向对象博客管理器")
        print("=" * 40)
        if self.current_user:
            print(f"👤 当前用户: {self.current_user.username}")
        else:
            print("👤 未登录")
        print("-" * 40)
        print("1. 👤 用户管理")
        print("2. 📝 文章管理")
        print("3. 🔍 搜索功能")
        print("4. 📊 统计信息")
        print("5. 🏷️  标签管理")
        print("0. 🚪 退出程序")
        print("-" * 40)
    
    def user_menu(self):
        """用户管理菜单"""
        while True:
            print("\n👤 用户管理")
            print("-" * 20)
            print("1. 登录用户")
            print("2. 注册用户")
            print("3. 查看用户信息")
            print("4. 用户列表")
            print("0. 返回主菜单")
            
            choice = input("请选择操作: ").strip()
            
            if choice == "1":
                self._login_user()
            elif choice == "2":
                self._register_user()
            elif choice == "3":
                self._show_user_info()
            elif choice == "4":
                self._list_users()
            elif choice == "0":
                break
            else:
                print("❌ 无效选择")
    
    def _login_user(self):
        """用户登录"""
        username = input("请输入用户名: ").strip()
        user = self.blog_manager.get_user(username)
        
        if user:
            self.current_user = user
            print(f"✅ 登录成功！欢迎 {user.username}")
        else:
            print("❌ 用户不存在")
    
    def _register_user(self):
        """用户注册"""
        try:
            username = input("请输入用户名: ").strip()
            email = input("请输入邮箱: ").strip()
            
            user = self.blog_manager.add_user(username, email)
            print(f"✅ 用户 {username} 注册成功！")
            
            login_choice = input("是否立即登录? (y/n): ").lower().strip()
            if login_choice == 'y':
                self.current_user = user
                print(f"✅ 已登录为 {username}")
                
        except ValueError as e:
            print(f"❌ 注册失败: {e}")
    
    def _show_user_info(self):
        """显示用户信息"""
        if not self.current_user:
            print("❌ 请先登录")
            return
        
        user = self.current_user
        print(f"\n👤 用户信息")
        print("=" * 30)
        print(f"用户名: {user.username}")
        print(f"邮箱: {user.email}")
        print(f"注册时间: {user.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"文章数量: {user.get_article_count()}")
        print(f"总浏览量: {user.get_total_views()}")
        
        if user.articles:
            print(f"\n📝 最新文章:")
            for article in user.articles[-3:]:  # 显示最新3篇
                print(f"  • {article.title} (👀 {article.views})")
    
    def _list_users(self):
        """显示用户列表"""
        users = self.blog_manager._users
        if not users:
            print("📭 暂无用户")
            return
        
        print(f"\n👥 用户列表 (共 {len(users)} 个用户)")
        print("=" * 50)
        for user in users:
            print(f"{user} | 📧 {user.email}")
    
    def article_menu(self):
        """文章管理菜单"""
        while True:
            print("\n📝 文章管理")
            print("-" * 20)
            print("1. 创建文章")
            print("2. 查看文章列表")
            print("3. 查看文章详情")
            print("4. 我的文章")
            print("0. 返回主菜单")
            
            choice = input("请选择操作: ").strip()
            
            if choice == "1":
                self._create_article()
            elif choice == "2":
                self._list_articles()
            elif choice == "3":
                self._view_article()
            elif choice == "4":
                self._my_articles()
            elif choice == "0":
                break
            else:
                print("❌ 无效选择")
    
    def _create_article(self):
        """创建文章"""
        if not self.current_user:
            print("❌ 请先登录")
            return
        
        try:
            title = input("请输入文章标题: ").strip()
            content = input("请输入文章内容: ").strip()
            tags_input = input("请输入标签 (用逗号分隔): ").strip()
            
            tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()] if tags_input else []
            
            article = self.current_user.create_article(title, content, tags)
            self.blog_manager.add_article(article)
            
            print(f"✅ 文章 '{title}' 创建成功！")
            
        except ValueError as e:
            print(f"❌ 创建失败: {e}")
    
    def _list_articles(self):
        """显示文章列表"""
        articles = self.blog_manager.get_all_articles()
        if not articles:
            print("📭 暂无文章")
            return
        
        print(f"\n📚 文章列表 (共 {len(articles)} 篇)")
        print("=" * 60)
        
        for article in sorted(articles, key=lambda x: x.created_at, reverse=True):
            tags_str = ", ".join(article.tags) if article.tags else "无标签"
            print(f"📄 [{article.id}] {article.title}")
            print(f"   👤 {article.author} | 📅 {article.created_at.strftime('%Y-%m-%d %H:%M')}")
            print(f"   👀 {article.views} 浏览 | ❤️ {article.likes} 点赞 | 🏷️ {tags_str}")
            print(f"   📝 {article.get_summary(80)}")
            print("-" * 60)
    
    def _view_article(self):
        """查看文章详情"""
        articles = self.blog_manager.get_all_articles()
        if not articles:
            print("📭 暂无文章")
            return
        
        try:
            article_id = int(input("请输入文章ID: "))
            
            article = None
            for a in articles:
                if a.id == article_id:
                    article = a
                    break
            
            if not article:
                print("❌ 文章不存在")
                return
            
            # 增加浏览量
            article.add_view()
            
            # 显示文章详情
            print(f"\n📖 {article.title}")
            print("=" * 60)
            print(f"👤 作者: {article.author}")
            print(f"📅 发布时间: {article.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"👀 浏览次数: {article.views}")
            print(f"❤️ 点赞数: {article.likes}")
            print(f"🏷️ 标签: {', '.join(article.tags) if article.tags else '无标签'}")
            print(f"📏 字数: {len(article)} 字")
            print("\n📄 内容:")
            print(article.content)
            print("=" * 60)
            
            # 询问是否点赞
            like_choice = input("是否为这篇文章点赞? (y/n): ").lower().strip()
            if like_choice == 'y':
                article.add_like()
                print("❤️ 点赞成功！")
                
        except ValueError:
            print("❌ 请输入有效的文章ID")
    
    def _my_articles(self):
        """我的文章"""
        if not self.current_user:
            print("❌ 请先登录")
            return
        
        articles = self.current_user.articles
        if not articles:
            print("📭 您还没有发布文章")
            return
        
        print(f"\n📝 我的文章 (共 {len(articles)} 篇)")
        print("=" * 50)
        
        for article in sorted(articles, key=lambda x: x.created_at, reverse=True):
            tags_str = ", ".join(article.tags) if article.tags else "无标签"
            print(f"📄 [{article.id}] {article.title}")
            print(f"   📅 {article.created_at.strftime('%Y-%m-%d %H:%M')}")
            print(f"   👀 {article.views} 浏览 | ❤️ {article.likes} 点赞 | 🏷️ {tags_str}")
            print("-" * 50)
    
    def search_menu(self):
        """搜索功能菜单"""
        while True:
            print("\n🔍 搜索功能")
            print("-" * 20)
            print("1. 关键词搜索")
            print("2. 按标签搜索")
            print("3. 按作者搜索")
            print("0. 返回主菜单")
            
            choice = input("请选择操作: ").strip()
            
            if choice == "1":
                self._keyword_search()
            elif choice == "2":
                self._tag_search()
            elif choice == "3":
                self._author_search()
            elif choice == "0":
                break
            else:
                print("❌ 无效选择")
    
    def _keyword_search(self):
        """关键词搜索"""
        keyword = input("请输入搜索关键词: ").strip()
        if not keyword:
            print("❌ 关键词不能为空")
            return
        
        results = self.blog_manager.search_articles(keyword)
        
        if not results:
            print(f"❌ 没有找到包含 '{keyword}' 的文章")
            return
        
        print(f"\n🔍 搜索结果 (找到 {len(results)} 篇文章)")
        print("=" * 60)
        
        for article in results:
            tags_str = ", ".join(article.tags) if article.tags else "无标签"
            print(f"📄 [{article.id}] {article.title}")
            print(f"   👤 {article.author} | 👀 {article.views} | 🏷️ {tags_str}")
            print(f"   📝 {article.get_summary(80)}")
            print("-" * 60)
    
    def _tag_search(self):
        """按标签搜索"""
        tag = input("请输入标签名: ").strip()
        if not tag:
            print("❌ 标签名不能为空")
            return
        
        results = self.blog_manager.get_articles_by_tag(tag)
        
        if not results:
            print(f"❌ 没有找到标签为 '{tag}' 的文章")
            return
        
        print(f"\n🏷️ 标签 '{tag}' 的文章 (共 {len(results)} 篇)")
        print("=" * 60)
        
        for article in results:
            print(f"📄 [{article.id}] {article.title}")
            print(f"   👤 {article.author} | 👀 {article.views}")
            print(f"   📝 {article.get_summary(80)}")
            print("-" * 60)
    
    def _author_search(self):
        """按作者搜索"""
        author = input("请输入作者名: ").strip()
        if not author:
            print("❌ 作者名不能为空")
            return
        
        articles = self.blog_manager.get_all_articles()
        results = [article for article in articles if article.author == author]
        
        if not results:
            print(f"❌ 没有找到作者为 '{author}' 的文章")
            return
        
        print(f"\n👤 作者 '{author}' 的文章 (共 {len(results)} 篇)")
        print("=" * 60)
        
        for article in sorted(results, key=lambda x: x.created_at, reverse=True):
            tags_str = ", ".join(article.tags) if article.tags else "无标签"
            print(f"📄 [{article.id}] {article.title}")
            print(f"   📅 {article.created_at.strftime('%Y-%m-%d %H:%M')} | 👀 {article.views} | 🏷️ {tags_str}")
            print(f"   📝 {article.get_summary(80)}")
            print("-" * 60)
    
    def show_statistics(self):
        """显示统计信息"""
        stats = self.blog_manager.get_statistics()
        
        print(f"\n📊 博客统计信息")
        print("=" * 40)
        print(f"📝 文章总数: {stats['total_articles']}")
        print(f"👤 用户总数: {stats['total_users']}")
        print(f"👀 总浏览量: {stats['total_views']}")
        print(f"📈 平均浏览量: {stats['average_views']:.1f}")
        print(f"🏷️ 标签总数: {stats['total_tags']}")
        
        # 热门标签
        popular_tags = self.blog_manager.get_popular_tags(5)
        if popular_tags:
            print(f"\n🔥 热门标签 (前5名):")
            for i, tag in enumerate(popular_tags, 1):
                print(f"  {i}. {tag}")
        
        # 热门文章
        articles = self.blog_manager.get_all_articles()
        if articles:
            popular_articles = sorted(articles, key=lambda x: x.views, reverse=True)[:3]
            print(f"\n📈 热门文章 (前3名):")
            for i, article in enumerate(popular_articles, 1):
                print(f"  {i}. {article.title} (👀 {article.views})")
    
    def tag_menu(self):
        """标签管理菜单"""
        print(f"\n🏷️ 标签管理")
        print("=" * 30)
        
        tags = self.blog_manager.get_popular_tags()
        if not tags:
            print("📭 暂无标签")
            return
        
        print(f"所有标签 (共 {len(tags)} 个):")
        for tag in tags:
            articles_count = len(self.blog_manager.get_articles_by_tag(tag.name))
            print(f"  {tag} | 📄 {articles_count} 篇文章")
    
    def run(self):
        """运行应用程序"""
        print("🎉 欢迎使用Python面向对象博客管理器！")
        print("💡 这是一个学习Python OOP概念的实践项目")
        
        while True:
            try:
                self.show_menu()
                choice = input("请选择操作 (0-5): ").strip()
                
                if choice == "1":
                    self.user_menu()
                elif choice == "2":
                    self.article_menu()
                elif choice == "3":
                    self.search_menu()
                elif choice == "4":
                    self.show_statistics()
                elif choice == "5":
                    self.tag_menu()
                elif choice == "0":
                    print("\n👋 感谢使用Python面向对象博客管理器！")
                    print("🎓 继续学习下一阶段：文件操作和数据持久化")
                    break
                else:
                    print("❌ 无效选择，请输入 0-5 之间的数字")
                    
            except KeyboardInterrupt:
                print("\n\n👋 程序被用户中断，再见！")
                break
            except Exception as e:
                print(f"❌ 程序出错: {e}")

def main():
    """主函数"""
    app = BlogApp()
    app.run()

if __name__ == "__main__":
    main()
