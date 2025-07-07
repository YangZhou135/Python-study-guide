#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件操作和异常处理示例
学习Python的文件I/O、JSON处理和异常处理
"""

import json
import os
import datetime
from pathlib import Path
from typing import Dict, List, Any

def demonstrate_file_basics():
    """演示文件操作基础"""
    print("📁 文件操作基础示例")
    print("=" * 40)
    
    # 1. 创建和写入文件
    print("\n1. 创建和写入文件:")
    
    # 使用with语句确保文件正确关闭
    filename = "demo.txt"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Hello, Python文件操作！\n")
            f.write("这是第二行内容。\n")
            f.write("文件操作很重要！\n")
        print(f"✅ 文件 {filename} 创建成功")
    except IOError as e:
        print(f"❌ 文件写入失败: {e}")
    
    # 2. 读取文件
    print("\n2. 读取文件内容:")
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"📄 文件内容:\n{content}")
    except IOError as e:
        print(f"❌ 文件读取失败: {e}")
    
    # 3. 按行读取
    print("3. 按行读取文件:")
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                print(f"   第{line_num}行: {line.strip()}")
    except IOError as e:
        print(f"❌ 文件读取失败: {e}")
    
    # 4. 追加内容
    print("\n4. 追加文件内容:")
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(f"追加时间: {datetime.datetime.now()}\n")
        print("✅ 内容追加成功")
    except IOError as e:
        print(f"❌ 文件追加失败: {e}")
    
    # 5. 文件信息
    print("\n5. 文件信息:")
    try:
        file_path = Path(filename)
        if file_path.exists():
            stat = file_path.stat()
            print(f"   文件大小: {stat.st_size} 字节")
            print(f"   创建时间: {datetime.datetime.fromtimestamp(stat.st_ctime)}")
            print(f"   修改时间: {datetime.datetime.fromtimestamp(stat.st_mtime)}")
        else:
            print("❌ 文件不存在")
    except OSError as e:
        print(f"❌ 获取文件信息失败: {e}")
    
    # 清理演示文件
    try:
        os.remove(filename)
        print(f"🧹 演示文件 {filename} 已清理")
    except OSError:
        pass

def demonstrate_json_operations():
    """演示JSON操作"""
    print("\n\n📄 JSON操作示例")
    print("=" * 40)
    
    # 1. Python对象转JSON
    print("\n1. Python对象转JSON:")
    
    # 创建示例数据
    blog_data = {
        "title": "Python学习笔记",
        "author": "张三",
        "content": "今天学习了文件操作...",
        "tags": ["Python", "文件操作", "JSON"],
        "created_at": datetime.datetime.now().isoformat(),
        "views": 0,
        "published": True,
        "metadata": {
            "word_count": 150,
            "reading_time": 2
        }
    }
    
    # 转换为JSON字符串
    json_string = json.dumps(blog_data, ensure_ascii=False, indent=2)
    print("📝 Python字典:")
    print(blog_data)
    print("\n📄 JSON字符串:")
    print(json_string)
    
    # 2. JSON转Python对象
    print("\n2. JSON转Python对象:")
    parsed_data = json.loads(json_string)
    print("✅ 解析后的数据:")
    print(f"   标题: {parsed_data['title']}")
    print(f"   作者: {parsed_data['author']}")
    print(f"   标签: {', '.join(parsed_data['tags'])}")
    
    # 3. 保存到JSON文件
    print("\n3. 保存到JSON文件:")
    json_filename = "blog_data.json"
    try:
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(blog_data, f, ensure_ascii=False, indent=2)
        print(f"✅ 数据已保存到 {json_filename}")
    except (IOError, json.JSONEncodeError) as e:
        print(f"❌ 保存JSON失败: {e}")
    
    # 4. 从JSON文件加载
    print("\n4. 从JSON文件加载:")
    try:
        with open(json_filename, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        print("✅ 数据加载成功:")
        print(f"   文章标题: {loaded_data['title']}")
        print(f"   字数统计: {loaded_data['metadata']['word_count']}")
    except (IOError, json.JSONDecodeError) as e:
        print(f"❌ 加载JSON失败: {e}")
    
    # 5. 处理复杂数据结构
    print("\n5. 处理复杂数据结构:")
    
    # 多篇文章的数据
    articles_data = {
        "blog_info": {
            "name": "我的技术博客",
            "description": "分享编程学习心得",
            "created": datetime.datetime.now().isoformat()
        },
        "articles": [
            {
                "id": 1,
                "title": "Python基础",
                "tags": ["Python", "基础"],
                "stats": {"views": 100, "likes": 5}
            },
            {
                "id": 2,
                "title": "文件操作",
                "tags": ["Python", "文件"],
                "stats": {"views": 80, "likes": 3}
            }
        ],
        "total_articles": 2
    }
    
    complex_filename = "complex_blog.json"
    try:
        # 保存复杂数据
        with open(complex_filename, 'w', encoding='utf-8') as f:
            json.dump(articles_data, f, ensure_ascii=False, indent=2)
        
        # 加载并处理
        with open(complex_filename, 'r', encoding='utf-8') as f:
            loaded_complex = json.load(f)
        
        print("✅ 复杂数据处理成功:")
        print(f"   博客名称: {loaded_complex['blog_info']['name']}")
        print(f"   文章数量: {loaded_complex['total_articles']}")
        
        total_views = sum(article['stats']['views'] for article in loaded_complex['articles'])
        print(f"   总浏览量: {total_views}")
        
    except (IOError, json.JSONDecodeError) as e:
        print(f"❌ 处理复杂数据失败: {e}")
    
    # 清理演示文件
    for filename in [json_filename, complex_filename]:
        try:
            os.remove(filename)
        except OSError:
            pass

def demonstrate_exception_handling():
    """演示异常处理"""
    print("\n\n⚠️ 异常处理示例")
    print("=" * 40)
    
    # 1. 基本异常处理
    print("\n1. 基本异常处理:")
    
    def safe_divide(a, b):
        """安全除法函数"""
        try:
            result = a / b
            print(f"✅ {a} ÷ {b} = {result}")
            return result
        except ZeroDivisionError:
            print(f"❌ 错误: 不能除以零")
            return None
        except TypeError:
            print(f"❌ 错误: 参数类型不正确")
            return None
    
    # 测试不同情况
    safe_divide(10, 2)      # 正常情况
    safe_divide(10, 0)      # 除零错误
    safe_divide(10, "2")    # 类型错误
    
    # 2. 文件操作异常处理
    print("\n2. 文件操作异常处理:")
    
    def safe_read_file(filename):
        """安全读取文件"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"✅ 文件 {filename} 读取成功")
            return content
        except FileNotFoundError:
            print(f"❌ 错误: 文件 {filename} 不存在")
            return None
        except PermissionError:
            print(f"❌ 错误: 没有权限访问文件 {filename}")
            return None
        except IOError as e:
            print(f"❌ 错误: 文件操作失败 - {e}")
            return None
    
    # 测试文件读取
    safe_read_file("existing_file.txt")     # 不存在的文件
    safe_read_file("examples_files.py")     # 当前文件
    
    # 3. JSON异常处理
    print("\n3. JSON异常处理:")
    
    def safe_parse_json(json_string):
        """安全解析JSON"""
        try:
            data = json.loads(json_string)
            print("✅ JSON解析成功")
            return data
        except json.JSONDecodeError as e:
            print(f"❌ JSON格式错误: {e}")
            return None
        except TypeError:
            print("❌ 错误: 输入不是字符串")
            return None
    
    # 测试JSON解析
    safe_parse_json('{"name": "张三", "age": 25}')  # 正确JSON
    safe_parse_json('{"name": "张三", "age":}')     # 错误JSON
    safe_parse_json(123)                           # 非字符串
    
    # 4. 多重异常处理
    print("\n4. 多重异常处理:")
    
    def process_user_data(data_string):
        """处理用户数据"""
        try:
            # 解析JSON
            data = json.loads(data_string)
            
            # 验证必需字段
            if 'name' not in data:
                raise ValueError("缺少必需字段: name")
            if 'age' not in data:
                raise ValueError("缺少必需字段: age")
            
            # 验证数据类型
            if not isinstance(data['age'], int):
                raise TypeError("年龄必须是整数")
            
            if data['age'] < 0:
                raise ValueError("年龄不能为负数")
            
            print(f"✅ 用户数据处理成功: {data['name']}, {data['age']}岁")
            return data
            
        except json.JSONDecodeError:
            print("❌ JSON格式错误")
        except ValueError as e:
            print(f"❌ 数据验证错误: {e}")
        except TypeError as e:
            print(f"❌ 类型错误: {e}")
        except Exception as e:
            print(f"❌ 未知错误: {e}")
        
        return None
    
    # 测试不同情况
    process_user_data('{"name": "张三", "age": 25}')      # 正确数据
    process_user_data('{"name": "李四"}')                 # 缺少字段
    process_user_data('{"name": "王五", "age": "25"}')    # 类型错误
    process_user_data('{"name": "赵六", "age": -5}')      # 值错误
    
    # 5. finally子句
    print("\n5. finally子句示例:")
    
    def demo_finally():
        """演示finally子句"""
        file_handle = None
        try:
            print("   尝试打开文件...")
            file_handle = open("temp_demo.txt", 'w')
            print("   文件打开成功")
            
            # 模拟可能的错误
            # raise ValueError("模拟错误")
            
            file_handle.write("测试内容")
            print("   文件写入成功")
            
        except IOError:
            print("   ❌ 文件操作失败")
        except ValueError as e:
            print(f"   ❌ 值错误: {e}")
        finally:
            print("   🧹 执行清理操作...")
            if file_handle:
                file_handle.close()
                print("   文件已关闭")
            
            # 清理临时文件
            try:
                os.remove("temp_demo.txt")
                print("   临时文件已删除")
            except OSError:
                pass
    
    demo_finally()

def demonstrate_pathlib():
    """演示pathlib路径处理"""
    print("\n\n🛤️ 路径处理示例 (pathlib)")
    print("=" * 40)
    
    # 1. 创建路径对象
    print("\n1. 路径对象操作:")
    
    current_file = Path(__file__)
    print(f"当前文件: {current_file}")
    print(f"文件名: {current_file.name}")
    print(f"文件扩展名: {current_file.suffix}")
    print(f"文件名(无扩展名): {current_file.stem}")
    print(f"父目录: {current_file.parent}")
    print(f"绝对路径: {current_file.absolute()}")
    
    # 2. 路径拼接
    print("\n2. 路径拼接:")
    
    data_dir = Path("data")
    config_file = data_dir / "config.json"
    backup_dir = data_dir / "backups" / "2024"
    
    print(f"数据目录: {data_dir}")
    print(f"配置文件: {config_file}")
    print(f"备份目录: {backup_dir}")
    
    # 3. 路径检查
    print("\n3. 路径检查:")
    
    paths_to_check = [current_file, data_dir, config_file]
    
    for path in paths_to_check:
        print(f"\n路径: {path}")
        print(f"  存在: {path.exists()}")
        print(f"  是文件: {path.is_file()}")
        print(f"  是目录: {path.is_dir()}")
        
        if path.exists():
            stat = path.stat()
            print(f"  大小: {stat.st_size} 字节")
    
    # 4. 目录操作
    print("\n4. 目录操作:")
    
    demo_dir = Path("demo_directory")
    try:
        # 创建目录
        demo_dir.mkdir(exist_ok=True)
        print(f"✅ 目录创建: {demo_dir}")
        
        # 创建子目录
        sub_dir = demo_dir / "subdirectory"
        sub_dir.mkdir(exist_ok=True)
        print(f"✅ 子目录创建: {sub_dir}")
        
        # 创建文件
        demo_file = demo_dir / "demo.txt"
        demo_file.write_text("演示内容", encoding='utf-8')
        print(f"✅ 文件创建: {demo_file}")
        
        # 列出目录内容
        print(f"\n目录内容:")
        for item in demo_dir.iterdir():
            if item.is_file():
                print(f"  📄 {item.name}")
            elif item.is_dir():
                print(f"  📁 {item.name}/")
        
        # 查找文件
        print(f"\n查找.txt文件:")
        for txt_file in demo_dir.glob("*.txt"):
            print(f"  📄 {txt_file}")
        
    except OSError as e:
        print(f"❌ 目录操作失败: {e}")
    finally:
        # 清理演示目录
        import shutil
        try:
            shutil.rmtree(demo_dir)
            print(f"🧹 演示目录已清理: {demo_dir}")
        except OSError:
            pass

def demonstrate_context_managers():
    """演示上下文管理器"""
    print("\n\n🔧 上下文管理器示例")
    print("=" * 40)
    
    # 1. with语句的优势
    print("\n1. with语句 vs 手动管理:")
    
    # 不推荐的方式（手动管理）
    print("\n❌ 手动管理文件（不推荐）:")
    try:
        f = open("manual_demo.txt", 'w')
        f.write("手动管理的文件")
        # 如果这里出现异常，文件可能不会被正确关闭
        f.close()
        print("   文件操作完成")
    except Exception as e:
        print(f"   错误: {e}")
    finally:
        try:
            os.remove("manual_demo.txt")
        except OSError:
            pass
    
    # 推荐的方式（with语句）
    print("\n✅ with语句管理（推荐）:")
    try:
        with open("with_demo.txt", 'w') as f:
            f.write("with语句管理的文件")
            # 即使出现异常，文件也会被正确关闭
        print("   文件操作完成，自动关闭")
    except Exception as e:
        print(f"   错误: {e}")
    finally:
        try:
            os.remove("with_demo.txt")
        except OSError:
            pass
    
    # 2. 自定义上下文管理器
    print("\n2. 自定义上下文管理器:")
    
    class TimerContext:
        """计时上下文管理器"""
        
        def __init__(self, name):
            self.name = name
            self.start_time = None
        
        def __enter__(self):
            print(f"   ⏱️ 开始计时: {self.name}")
            self.start_time = datetime.datetime.now()
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            end_time = datetime.datetime.now()
            duration = end_time - self.start_time
            print(f"   ⏱️ 结束计时: {self.name}")
            print(f"   ⏱️ 耗时: {duration.total_seconds():.4f} 秒")
            
            # 返回False表示不抑制异常
            return False
    
    # 使用自定义上下文管理器
    with TimerContext("文件操作测试"):
        # 模拟一些操作
        import time
        time.sleep(0.1)
        
        with open("timer_demo.txt", 'w') as f:
            f.write("计时测试文件")
        
        with open("timer_demo.txt", 'r') as f:
            content = f.read()
            print(f"   📄 读取内容: {content}")
    
    # 清理
    try:
        os.remove("timer_demo.txt")
    except OSError:
        pass

def main():
    """主函数"""
    print("🐍 Python文件操作和异常处理示例")
    print("=" * 50)
    
    # 运行所有示例
    demonstrate_file_basics()
    demonstrate_json_operations()
    demonstrate_exception_handling()
    demonstrate_pathlib()
    demonstrate_context_managers()
    
    print("\n\n🎉 文件操作示例完成！")
    print("💡 关键要点:")
    print("   1. 总是使用with语句处理文件")
    print("   2. 适当处理异常，让程序更健壮")
    print("   3. JSON是数据交换的好格式")
    print("   4. pathlib让路径操作更简单")
    print("   5. 上下文管理器确保资源正确释放")

if __name__ == "__main__":
    main()
