#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stage 7: Python高级特性独立示例
本文件用于脱离Web框架，纯粹地学习和理解装饰器、生成器和异步编程的核心概念。
"""

import time
import asyncio
from functools import wraps

# --- 1. 装饰器 (Decorators) ---

print("--- 1. 装饰器示例 ---")

def timing_decorator(func):
    """
    一个简单的计时装饰器。
    它会打印出被它装饰的函数的执行时间。
    """
    @wraps(func)  # @wraps(func) 是一个好习惯，它能保留原函数的元信息（如函数名、文档字符串）
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)  # 调用原始函数
        end_time = time.time()
        print(f"函数 '{func.__name__}' 执行耗时: {end_time - start_time:.4f} 秒")
        return result
    return wrapper

@timing_decorator
def slow_function(delay):
    """一个模拟耗时操作的函数"""
    print(f"正在执行耗时 {delay} 秒的操作...")
    time.sleep(delay)
    print("操作完成。")
    return "操作成功返回"

# 调用被装饰的函数
result = slow_function(1)
print(f"slow_function的返回值: {result}\n")


# --- 2. 生成器 (Generators) ---

print("--- 2. 生成器示例 ---")

def fibonacci_generator(limit):
    """
    一个斐波那契数列的生成器。
    它使用 yield 关键字来逐个“生成”数字，而不是一次性创建一个巨大的列表。
    """
    a, b = 0, 1
    count = 0
    while count < limit:
        yield a
        a, b = b, a + b
        count += 1

print("使用生成器逐个打印斐波那契数列前10个数字:")
# 生成器只有在被迭代时才会执行
fib_gen = fibonacci_generator(10)
for number in fib_gen:
    print(number, end=' ')
print("\n")

def large_file_reader_generator(file_path):
    """
    一个模拟逐行读取大文件的生成器。
    这在处理G级别的大文件时能极大地节省内存。
    """
    print(f"开始逐行读取文件 '{file_path}'...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # yield会暂停函数，返回这一行的内容，并记住当前位置
                yield line.strip()
    except FileNotFoundError:
        print(f"错误: 文件 '{file_path}' 未找到。")

# 创建一个临时文件用于演示
temp_file_path = "temp_large_file.txt"
with open(temp_file_path, "w", encoding='utf-8') as f:
    f.write("这是第一行。\n")
    f.write("这是第二行，包含一些数据。\n")
    f.write("这是最后一行。\n")

# 使用生成器读取文件
file_reader_gen = large_file_reader_generator(temp_file_path)
print("使用生成器读取文件内容:")
for file_line in file_reader_gen:
    print(f"  - {file_line}")

# 清理临时文件
import os
os.remove(temp_file_path)
print("\n")


# --- 3. 异步编程 (Async/Await) ---

print("--- 3. 异步编程示例 ---")

async def fetch_data(source, delay):
    """
    一个模拟的异步函数，用于从某个来源获取数据。
    `async def` 定义了一个协程。
    """
    print(f"开始从 {source} 获取数据...")
    # `await` 会“暂停”当前协程的执行，让事件循环可以去运行其他任务。
    # `asyncio.sleep` 是 `time.sleep` 的异步版本。
    await asyncio.sleep(delay)
    print(f"✅ 成功从 {source} 获取数据！")
    return {"source": source, "data": f"来自{source}的数据包"}

async def main():
    """
    主异步函数，用于协调和运行其他异步任务。
    """
    print("开始执行主异步任务...")
    start_time = time.time()

    # 使用 asyncio.gather 并发运行多个异步任务
    # 这两个任务会“同时”开始，而不是一个接一个。
    task1 = asyncio.create_task(fetch_data("API服务器", 2))
    task2 = asyncio.create_task(fetch_data("数据库", 3))

    # 等待所有任务完成
    results = await asyncio.gather(task1, task2)

    end_time = time.time()
    print(f"\n所有异步任务完成，总耗时: {end_time - start_time:.4f} 秒")
    print("获取到的结果:")
    for res in results:
        print(f"  - {res}")

# 在Python脚本的顶层，我们使用 asyncio.run() 来启动并运行一个异步函数。
# 它会创建一个事件循环，运行指定的协程，直到它完成，然后关闭循环。
asyncio.run(main())
