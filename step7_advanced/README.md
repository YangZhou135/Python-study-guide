# Stage 7: Python高级特性实践

## 🎯 学习目标

在这个阶段，您将在一个真实的Web应用背景下，学习并实践Python的一些高级但非常强大的特性。我们的目标不是引入复杂的新功能，而是在现有功能的基础上，通过应用这些高级特性来优化代码的结构、性能和可维护性。

您将学习：

1.  **装饰器 (Decorators)**: 如何创建并使用自定义装饰器来封装和重用横切关注点（如权限检查）。
2.  **生成器 (Generators)**: 如何利用生成器来高效处理大量数据，实现流式响应，显著降低服务器内存消耗。
3.  **异步编程 (Async/Await)**: 理解 `async/await` 的基本语法，并了解如何在同步的Web框架（如Flask）中执行异步任务。

## 📁 项目结构

本阶段的所有代码都包含在 `step7_advanced` 目录中，并完全独立于 `step6`。

```
step7_advanced/
├── backend/              # 一个完整、可独立运行的后端应用
│   ├── app.py            # (无修改) Flask应用主文件
│   ├── models.py         # (修改) User模型增加 is_admin 字段
│   ├── init_db.py        # (修改) 初始化时创建真正的管理员
│   ├── middleware/
│   │   └── auth.py       # (修改) 实现了 @admin_required 装饰器
│   ├── api/
│   │   └── articles.py   # (修改) 添加了使用生成器的/export接口和异步通知任务
│   │   └── users.py      # (修改) 使用 @admin_required 保护了用户列表接口
│   └── ...               # (其他文件均为step6的副本)
├── examples_advanced.py  # (新增) 纯Python的高级特性示例，用于脱离框架理解核心概念
└── README.md             # (本文件)
```

## 🚀 快速开始

本阶段的后端是一个可以独立运行的应用。

### 1. 环境设置

```bash
# 进入step7的后端目录
cd step7_advanced/backend

# (推荐) 创建并激活虚拟环境
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
# source venv/bin/activate

# 安装��赖
pip install -r requirements.txt
```

### 2. 初始化数据库

这个命令会创建数据库文件 `blog_dev.db` 并填充初始数据，包括一个真正的管理员账户。

```bash
python init_db.py
```

### 3. 启动应用

```bash
python run.py
```

应用将在 `http://localhost:5000` 上运行。您可以像之前一样，使用 `step6` 的前端或 Postman 等工具来与它交互。

## ✨ 高级特性实现详解

### 1. 装饰器: `@admin_required`

-   **是什么**: 装饰器是一个函数，它接受另一个函数作为参数，并返回一个新的函数，从而在不改变原函数代码的情况下增加新功能。
-   **为什么用**: 在Web开发中，很多接口都需要相同的检查逻辑（如用户是否登录、是否是管理员）。使用装饰器可以避免在每个路由函数里都写一遍重复的检查代码，使代码更简洁、更易维护。
-   **如何实现**:
    1.  **`models.py`**: 我们给 `User` 模型增加了一个布尔字段 `is_admin`。
    2.  **`init_db.py`**: 在创建 `admin` 用户时，我们设置 `admin.is_admin = True`。
    3.  **`middleware/auth.py`**: 我���创建了 `admin_required` 装饰器。它首先调用 `@jwt_required()` 确保用户已登录，然后从数据库中获取当前用户，并检查 `user.is_admin` 是否为 `True`。如果不是，则返回 403 Forbidden 错误。
    4.  **`api/users.py`**: 我们将 `@admin_required` 应用在 `get_users` 路由上，实现了对该接口的访问控制。

-   **如何测试**:
    1.  使用 `admin` / `admin123` 登录获取Token。
    2.  使用此Token访问 `GET http://localhost:5000/api/v1/users`，应该会成功返回用户列表。
    3.  使用普通用户（如 `demo` / `demo123`）的Token访问该接口，应该会收到 `403 Forbidden` 错误。

### 2. 生成器: 文章导出

-   **是什么**: 生成器是一种特殊的函数，它使用 `yield` 关键字返回值。每次调用它时，它会从上次离开的地方继续执行，直到遇到下一个 `yield`。它不会一次性把所有结果都生成并放在内存里。
-   **为什么用**: 假设我们的博客有100万篇文章，如果我们要导出所有文章，一次性从数据库查询100万条记录并转换成CSV字符串，可能会消耗几个G的内存，导致���务器崩溃。使用生成器，我们可以一条一条地处理数据，内存占用极低，几乎为零。
-   **如何实现**:
    1.  **`api/articles.py`**: 我们创建了一个新的接口 `GET /export`。
    2.  该接口的实现是一个**生成器函数** `generate_csv()`。它首先 `yield` CSV的表头。然后，它查询所有文章，并在一个循环中逐一 `yield` 每一篇文章转换成的CSV行。
    3.  路由函数返回一个Flask的 `Response` 对象，将生成器作为流式传输的内容，并设置正确的HTTP头，告诉浏览器这是一个需要下载的CSV文件。

-   **如何测试**:
    1.  使用任意用户的Token（需要登录）。
    2.  在浏览器或Postman中访问 `GET http://localhost:5000/api/v1/articles/export` (需要带上Authorization头)。
    3.  浏览器会自动下载一个名为 `articles_export.csv` 的文件，其中包含了所有的文章数据。

### 3. 异步编程: 模拟通知

-   **是什么**: 使用 `async` 和 `await` 关键字来定义的协程。当程序遇到一个耗时的I/O操作（如网络请求、数据库查询）时，`await` 可以“暂停”当前函��，让CPU去执行其他任务，等I/O操作完成后再回来继续。
-   **为什么用**: 它可以极大地提高应用的并发处理能力。在一个Web服务器中，如果一个请求需要等待2秒来调用外部API，同步模型下，处理这个请求的进程会完全卡住2秒。而异步模型下，这个进程可以利用这2秒去处理几十个其他请求。
-   **如何实现**:
    1.  **`api/articles.py`**: 我们导入了 `asyncio` 库。
    2.  我们定义了一个 `async def send_notification(article_title)` 函数，它使用 `await asyncio.sleep(2)` 来模拟一个耗时2秒的网络调用。
    3.  在 `create_article` 函数中，当文章成功保存到数据库后，我们使用 `asyncio.run(send_notification(article.title))` 来调用这个异步函数。

-   **重要说明**: 在Flask这样的传统WSGI（同步）框架中直接使用 `asyncio.run()` 会**阻塞**当前请求，直到异步任务完成。因此，在这里它并不能体现出高并发的优势，**其主要目的是为了演示 `async/await` 的语法和如何在同步代码中调用异步代码**。在生产级的异步应用中，通常会使用ASGI框架（如FastAPI, Quart）或将耗时任务交给后台任务队列（如Celery, RQ）来处理，以实现真正的非阻塞。

-   **如何测试**:
    1.  登录并创建一个新文章。
    2.  观察运行 `run.py` 的**后端控制台**。在收到创建成功的HTTP响应后，您会看到控制台打印出 "开始为文章...发送通知..."，等待2秒后，再打印出 "...通知发送完成"。

## 📚 独立示例

为了更纯粹地理解这些概念，请务必查看 `examples_advanced.py` 文件。它包含了不依赖任何Web框架的、最简单的装饰器、生成器和异步代码示例。

---

现在，您已经准备好探索Python的这些高级特性了！
