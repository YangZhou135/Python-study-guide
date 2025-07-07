#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单博客文章管理器
通过实际项目学习Python基础语法
"""

import datetime

# 全局变量存储文章数据 (后续阶段会改用文件/数据库)
articles = []

def create_article():
    """创建新文章"""
    print("\n📝 创建新文章")
    print("-" * 30)
    
    # 获取用户输入
    title = input("请输入文章标题: ").strip()
    if not title:
        print("❌ 标题不能为空！")
        return
    
    content = input("请输入文章内容: ").strip()
    if not content:
        print("❌ 内容不能为空！")
        return
    
    # 处理标签输入
    tags_input = input("请输入标签 (用逗号分隔，可选): ").strip()
    tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()] if tags_input else []
    
    # 创建文章字典
    article = {
        "id": len(articles) + 1,
        "title": title,
        "content": content,
        "tags": tags,
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "views": 0
    }
    
    articles.append(article)
    print(f"✅ 文章 '{title}' 创建成功！")

def list_articles():
    """显示文章列表"""
    if not articles:
        print("\n📭 暂无文章")
        return
    
    print(f"\n📚 文章列表 (共 {len(articles)} 篇)")
    print("=" * 60)
    
    for article in articles:
        # 显示文章摘要
        content_preview = article["content"][:50] + "..." if len(article["content"]) > 50 else article["content"]
        tags_str = ", ".join(article["tags"]) if article["tags"] else "无标签"
        
        print(f"📄 [{article['id']}] {article['title']}")
        print(f"   📅 {article['created_at']} | 👀 {article['views']} 次浏览")
        print(f"   🏷️  {tags_str}")
        print(f"   📝 {content_preview}")
        print("-" * 60)

def view_article():
    """查看文章详情"""
    if not articles:
        print("\n📭 暂无文章")
        return
    
    try:
        article_id = int(input("\n请输入要查看的文章ID: "))
        
        # 查找文章
        article = None
        for a in articles:
            if a["id"] == article_id:
                article = a
                break
        
        if not article:
            print("❌ 文章不存在！")
            return
        
        # 增加浏览量
        article["views"] += 1
        
        # 显示文章详情
        print(f"\n📖 {article['title']}")
        print("=" * 60)
        print(f"📅 发布时间: {article['created_at']}")
        print(f"👀 浏览次数: {article['views']}")
        print(f"🏷️  标签: {', '.join(article['tags']) if article['tags'] else '无标签'}")
        print("\n📄 内容:")
        print(article['content'])
        print("=" * 60)
        
    except ValueError:
        print("❌ 请输入有效的文章ID！")

def search_articles():
    """搜索文章"""
    if not articles:
        print("\n📭 暂无文章")
        return
    
    keyword = input("\n🔍 请输入搜索关键词 (标题或标签): ").strip().lower()
    if not keyword:
        print("❌ 搜索关键词不能为空！")
        return
    
    # 搜索匹配的文章
    found_articles = []
    for article in articles:
        # 在标题中搜索
        if keyword in article["title"].lower():
            found_articles.append(article)
            continue
        
        # 在标签中搜索
        for tag in article["tags"]:
            if keyword in tag.lower():
                found_articles.append(article)
                break
    
    if not found_articles:
        print(f"❌ 没有找到包含 '{keyword}' 的文章")
        return
    
    print(f"\n🔍 搜索结果 (找到 {len(found_articles)} 篇文章)")
    print("=" * 60)
    
    for article in found_articles:
        content_preview = article["content"][:50] + "..." if len(article["content"]) > 50 else article["content"]
        tags_str = ", ".join(article["tags"]) if article["tags"] else "无标签"
        
        print(f"📄 [{article['id']}] {article['title']}")
        print(f"   📅 {article['created_at']} | 👀 {article['views']} 次浏览")
        print(f"   🏷️  {tags_str}")
        print(f"   📝 {content_preview}")
        print("-" * 60)

def show_statistics():
    """显示统计信息"""
    if not articles:
        print("\n📭 暂无文章")
        return
    
    print(f"\n📊 博客统计信息")
    print("=" * 40)
    
    # 基础统计
    total_articles = len(articles)
    total_views = sum(article["views"] for article in articles)
    avg_views = total_views / total_articles if total_articles > 0 else 0
    
    print(f"📝 文章总数: {total_articles}")
    print(f"👀 总浏览量: {total_views}")
    print(f"📈 平均浏览量: {avg_views:.1f}")
    
    # 标签统计
    tag_count = {}
    for article in articles:
        for tag in article["tags"]:
            tag_count[tag] = tag_count.get(tag, 0) + 1
    
    if tag_count:
        print(f"\n🏷️  标签统计:")
        # 按使用次数排序
        sorted_tags = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)
        for tag, count in sorted_tags:
            print(f"   {tag}: {count} 次")
    
    # 最受欢迎的文章
    if articles:
        most_popular = max(articles, key=lambda x: x["views"])
        print(f"\n🔥 最受欢迎文章: {most_popular['title']} ({most_popular['views']} 次浏览)")

def show_menu():
    """显示菜单"""
    print("\n🐍 Python博客管理器")
    print("=" * 30)
    print("1. 📝 创建文章")
    print("2. 📚 查看文章列表")
    print("3. 📖 查看文章详情")
    print("4. 🔍 搜索文章")
    print("5. 📊 统计信息")
    print("0. 🚪 退出程序")
    print("-" * 30)

def main():
    """主程序"""
    print("🎉 欢迎使用Python博客管理器！")
    print("💡 这是一个学习Python基础语法的实践项目")
    
    # 添加一些示例数据
    sample_articles = [
        {
            "id": 1,
            "title": "Python学习第一天",
            "content": "今天开始学习Python编程语言，发现它的语法比JavaScript更简洁易懂。",
            "tags": ["Python", "学习", "编程"],
            "created_at": "2024-01-01 10:00:00",
            "views": 15
        },
        {
            "id": 2,
            "title": "前端转后端的思考",
            "content": "作为一名前端开发者，学习Python后端开发让我对全栈开发有了新的认识。",
            "tags": ["前端", "后端", "全栈"],
            "created_at": "2024-01-02 14:30:00",
            "views": 8
        }
    ]
    
    articles.extend(sample_articles)
    
    while True:
        show_menu()
        
        try:
            choice = input("请选择操作 (0-5): ").strip()
            
            if choice == "1":
                create_article()
            elif choice == "2":
                list_articles()
            elif choice == "3":
                view_article()
            elif choice == "4":
                search_articles()
            elif choice == "5":
                show_statistics()
            elif choice == "0":
                print("\n👋 感谢使用Python博客管理器！")
                print("🎓 继续学习下一阶段：面向对象编程")
                break
            else:
                print("❌ 无效选择，请输入 0-5 之间的数字")
                
        except KeyboardInterrupt:
            print("\n\n👋 程序被用户中断，再见！")
            break
        except Exception as e:
            print(f"❌ 程序出错: {e}")

if __name__ == "__main__":
    main()
