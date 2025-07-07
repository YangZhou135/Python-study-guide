#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python基础语法示例
对比JavaScript，学习Python基础概念
"""

def demonstrate_variables():
    """变量和数据类型示例"""
    print("=== 变量和数据类型 ===")
    
    # Python vs JavaScript变量声明
    # JavaScript: let name = "张三"; const age = 25;
    # Python: 直接赋值，动态类型
    name = "张三"
    age = 25
    is_student = True
    height = 175.5
    
    print(f"姓名: {name} (类型: {type(name).__name__})")
    print(f"年龄: {age} (类型: {type(age).__name__})")
    print(f"是学生: {is_student} (类型: {type(is_student).__name__})")
    print(f"身高: {height} (类型: {type(height).__name__})")
    print()

def demonstrate_strings():
    """字符串操作示例"""
    print("=== 字符串操作 ===")
    
    title = "我的第一篇博客"
    content = "今天学习了Python基础语法"
    
    # 字符串格式化 (类似JavaScript的模板字符串)
    # JavaScript: `标题: ${title}`
    # Python: f-string
    formatted = f"标题: {title}\n内容: {content}"
    print(formatted)
    
    # 字符串方法
    print(f"标题长度: {len(title)}")
    print(f"转大写: {title.upper()}")
    print(f"是否包含'博客': {'博客' in title}")
    
    # 字符串分割和连接
    tags = "Python,编程,学习"
    tag_list = tags.split(",")
    print(f"标签列表: {tag_list}")
    print(f"重新连接: {' | '.join(tag_list)}")
    print()

def demonstrate_lists():
    """列表操作示例"""
    print("=== 列表操作 ===")
    
    # 创建列表 (类似JavaScript数组)
    articles = ["Python入门", "Web开发", "数据分析"]
    print(f"文章列表: {articles}")
    
    # 添加元素
    articles.append("机器学习")  # JavaScript: articles.push()
    print(f"添加后: {articles}")
    
    # 访问元素
    print(f"第一篇文章: {articles[0]}")
    print(f"最后一篇文章: {articles[-1]}")  # Python特色：负索引
    
    # 切片操作 (JavaScript没有的便利功能)
    print(f"前两篇文章: {articles[:2]}")
    print(f"后两篇文章: {articles[-2:]}")
    
    # 列表推导式 (类似JavaScript的map)
    # JavaScript: articles.map(article => article.length)
    # Python: 列表推导式
    lengths = [len(article) for article in articles]
    print(f"文章标题长度: {lengths}")
    print()

def demonstrate_dictionaries():
    """字典操作示例"""
    print("=== 字典操作 ===")
    
    # 创建字典 (类似JavaScript对象)
    article = {
        "title": "Python学习笔记",
        "author": "张三",
        "tags": ["Python", "编程"],
        "views": 100,
        "published": True
    }
    
    print("文章信息:")
    for key, value in article.items():
        print(f"  {key}: {value}")
    
    # 访问和修改
    print(f"\n标题: {article['title']}")
    print(f"作者: {article.get('author', '未知')}")  # 安全访问
    
    article["views"] += 1  # 增加浏览量
    print(f"更新后浏览量: {article['views']}")
    
    # 检查键是否存在
    if "tags" in article:
        print(f"标签: {', '.join(article['tags'])}")
    print()

def demonstrate_control_flow():
    """控制流程示例"""
    print("=== 控制流程 ===")
    
    articles = [
        {"title": "Python基础", "views": 150},
        {"title": "Web开发", "views": 89},
        {"title": "数据分析", "views": 200},
        {"title": "机器学习", "views": 45}
    ]
    
    # if条件判断
    print("热门文章 (浏览量>100):")
    for article in articles:
        if article["views"] > 100:
            print(f"  📈 {article['title']} ({article['views']} 次浏览)")
        elif article["views"] > 50:
            print(f"  📊 {article['title']} ({article['views']} 次浏览)")
        else:
            print(f"  📉 {article['title']} ({article['views']} 次浏览)")
    
    # 统计信息
    total_views = sum(article["views"] for article in articles)
    avg_views = total_views / len(articles)
    print(f"\n总浏览量: {total_views}")
    print(f"平均浏览量: {avg_views:.1f}")
    print()

def demonstrate_functions():
    """函数定义和使用示例"""
    print("=== 函数使用 ===")
    
    def create_article(title, content, tags=None):
        """创建文章函数"""
        if tags is None:
            tags = []
        
        return {
            "title": title,
            "content": content,
            "tags": tags,
            "created_at": "2024-01-01",
            "views": 0
        }
    
    def format_article(article):
        """格式化文章显示"""
        tags_str = ", ".join(article["tags"]) if article["tags"] else "无标签"
        return f"""
📝 {article['title']}
📅 {article['created_at']}
🏷️  {tags_str}
👀 {article['views']} 次浏览
📄 {article['content'][:50]}{'...' if len(article['content']) > 50 else ''}
        """.strip()
    
    # 使用函数
    new_article = create_article(
        "Python函数学习",
        "今天学习了如何定义和使用Python函数，包括参数传递、默认值等概念。",
        ["Python", "函数", "编程"]
    )
    
    print("新创建的文章:")
    print(format_article(new_article))
    print()

def main():
    """主函数 - 运行所有示例"""
    print("🐍 Python基础语法示例")
    print("=" * 50)
    
    demonstrate_variables()
    demonstrate_strings()
    demonstrate_lists()
    demonstrate_dictionaries()
    demonstrate_control_flow()
    demonstrate_functions()
    
    print("🎉 基础语法示例完成！")
    print("💡 提示：尝试修改代码，观察运行结果的变化")

if __name__ == "__main__":
    main()
