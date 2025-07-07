#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python基础语法练习题
通过实际编程练习巩固所学知识
"""

def exercise_1():
    """
    练习1: 字符串操作
    任务: 实现一个函数，将博客标题转换为URL友好的格式
    例如: "我的第一篇Python博客!" -> "my-first-python-blog"
    """
    print("=== 练习1: 字符串操作 ===")
    
    def title_to_url(title):
        """
        将中文标题转换为URL格式
        提示: 可以使用字符串的replace()方法和lower()方法
        """
        # TODO: 在这里实现你的代码
        # 1. 移除标点符号
        # 2. 将空格替换为连字符
        # 3. 转换为小写
        pass
    
    # 测试用例
    test_titles = [
        "我的第一篇Python博客!",
        "Web开发 学习笔记",
        "数据分析与可视化"
    ]
    
    print("测试标题转URL:")
    for title in test_titles:
        url = title_to_url(title)
        print(f"'{title}' -> '{url}'")
    
    print("\n💡 提示: 这个练习帮助你熟悉字符串方法")
    print()

def exercise_2():
    """
    练习2: 列表操作
    任务: 实现博客文章的标签管理功能
    """
    print("=== 练习2: 列表操作 ===")
    
    def manage_tags(articles):
        """
        分析文章标签，返回统计信息
        参数: articles - 文章列表
        返回: 字典包含标签统计信息
        """
        # TODO: 在这里实现你的代码
        # 1. 统计每个标签出现的次数
        # 2. 找出最受欢迎的标签
        # 3. 计算平均每篇文章的标签数量
        pass
    
    # 测试数据
    test_articles = [
        {"title": "Python基础", "tags": ["Python", "编程", "基础"]},
        {"title": "Web开发", "tags": ["Python", "Web", "Flask"]},
        {"title": "数据分析", "tags": ["Python", "数据", "分析"]},
        {"title": "前端技术", "tags": ["JavaScript", "前端", "Vue"]}
    ]
    
    result = manage_tags(test_articles)
    print("标签统计结果:")
    print(result)
    
    print("\n💡 提示: 使用字典来统计标签出现次数")
    print()

def exercise_3():
    """
    练习3: 函数和控制流
    任务: 实现文章推荐系统
    """
    print("=== 练习3: 函数和控制流 ===")
    
    def recommend_articles(articles, user_interests, max_recommendations=3):
        """
        根据用户兴趣推荐文章
        参数:
            articles - 文章列表
            user_interests - 用户兴趣标签列表
            max_recommendations - 最大推荐数量
        返回: 推荐文章列表
        """
        # TODO: 在这里实现你的代码
        # 1. 计算每篇文章与用户兴趣的匹配度
        # 2. 按匹配度排序
        # 3. 返回前N篇文章
        pass
    
    # 测试数据
    test_articles = [
        {"title": "Python入门教程", "tags": ["Python", "编程", "入门"], "views": 100},
        {"title": "JavaScript高级特性", "tags": ["JavaScript", "前端", "高级"], "views": 80},
        {"title": "数据库设计原理", "tags": ["数据库", "设计", "SQL"], "views": 60},
        {"title": "Python Web开发", "tags": ["Python", "Web", "Flask"], "views": 120},
        {"title": "前端框架对比", "tags": ["前端", "Vue", "React"], "views": 90}
    ]
    
    user_interests = ["Python", "Web", "编程"]
    
    recommendations = recommend_articles(test_articles, user_interests)
    print(f"基于兴趣 {user_interests} 的推荐文章:")
    for i, article in enumerate(recommendations, 1):
        print(f"{i}. {article['title']}")
    
    print("\n💡 提示: 可以通过计算共同标签数量来确定匹配度")
    print()

def exercise_4():
    """
    练习4: 综合应用
    任务: 实现简单的博客搜索引擎
    """
    print("=== 练习4: 综合应用 ===")
    
    def search_engine(articles, query, search_fields=["title", "content", "tags"]):
        """
        搜索引擎实现
        参数:
            articles - 文章列表
            query - 搜索查询
            search_fields - 搜索字段
        返回: 搜索结果列表，按相关性排序
        """
        # TODO: 在这里实现你的代码
        # 1. 在指定字段中搜索关键词
        # 2. 计算相关性得分
        # 3. 按得分排序返回结果
        pass
    
    # 测试数据
    test_articles = [
        {
            "title": "Python编程入门",
            "content": "Python是一种简单易学的编程语言，适合初学者学习。",
            "tags": ["Python", "编程", "入门"]
        },
        {
            "title": "Web开发技术栈",
            "content": "现代Web开发需要掌握前端和后端技术，Python是很好的后端选择。",
            "tags": ["Web", "开发", "技术栈"]
        },
        {
            "title": "数据科学与Python",
            "content": "Python在数据科学领域应用广泛，有丰富的数据处理库。",
            "tags": ["Python", "数据科学", "分析"]
        }
    ]
    
    search_queries = ["Python", "Web开发", "数据"]
    
    for query in search_queries:
        results = search_engine(test_articles, query)
        print(f"搜索 '{query}' 的结果:")
        for i, article in enumerate(results, 1):
            print(f"  {i}. {article['title']}")
        print()
    
    print("💡 提示: 可以通过关键词在不同字段中出现的次数来计算相关性")
    print()

def show_solutions():
    """显示练习题的参考答案"""
    print("=== 参考答案 ===")
    print("💡 建议先自己尝试完成练习，再查看答案")
    
    show_answer = input("是否显示参考答案? (y/n): ").lower().strip()
    if show_answer != 'y':
        return
    
    print("\n--- 练习1参考答案 ---")
    print("""
def title_to_url(title):
    # 简化版本：移除常见标点符号，替换空格
    import re
    # 移除标点符号
    clean_title = re.sub(r'[^\w\s]', '', title)
    # 替换空格为连字符，转小写
    url = clean_title.replace(' ', '-').lower()
    return url
    """)
    
    print("\n--- 练习2参考答案 ---")
    print("""
def manage_tags(articles):
    tag_count = {}
    total_tags = 0
    
    for article in articles:
        total_tags += len(article['tags'])
        for tag in article['tags']:
            tag_count[tag] = tag_count.get(tag, 0) + 1
    
    most_popular = max(tag_count.items(), key=lambda x: x[1]) if tag_count else None
    avg_tags = total_tags / len(articles) if articles else 0
    
    return {
        'tag_count': tag_count,
        'most_popular': most_popular,
        'average_tags_per_article': avg_tags
    }
    """)
    
    print("\n💡 完整答案请参考项目文档或询问导师")

def main():
    """主函数"""
    print("🎯 Python基础语法练习题")
    print("=" * 40)
    print("通过实际编程练习巩固所学知识")
    print()
    
    exercises = [
        ("字符串操作", exercise_1),
        ("列表操作", exercise_2),
        ("函数和控制流", exercise_3),
        ("综合应用", exercise_4)
    ]
    
    while True:
        print("选择练习题:")
        for i, (name, _) in enumerate(exercises, 1):
            print(f"{i}. {name}")
        print("5. 查看参考答案")
        print("0. 退出")
        
        try:
            choice = int(input("\n请选择 (0-5): "))
            
            if choice == 0:
                print("👋 练习结束，继续学习下一阶段！")
                break
            elif 1 <= choice <= 4:
                exercises[choice-1][1]()
            elif choice == 5:
                show_solutions()
            else:
                print("❌ 无效选择")
                
        except ValueError:
            print("❌ 请输入有效数字")
        except KeyboardInterrupt:
            print("\n👋 练习被中断")
            break

if __name__ == "__main__":
    main()
