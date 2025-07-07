# 第2阶段：面向对象编程实践

## 🎯 学习目标
通过重构博客管理系统，学习Python的面向对象编程概念。

## 📝 本阶段内容

### 1. 类和对象基础
- 类的定义和实例化
- 构造函数 `__init__`
- 实例属性和方法
- 类属性和类方法

### 2. 封装和属性
- 私有属性和方法
- 属性装饰器 `@property`
- getter和setter方法
- 数据验证

### 3. 继承和多态
- 类的继承
- 方法重写
- super()函数使用
- 多态性实现

### 4. 特殊方法
- `__str__` 和 `__repr__`
- `__len__` 和 `__contains__`
- 运算符重载

## 🏗️ 项目重构：面向对象的博客系统

我们将把第一阶段的函数式代码重构为面向对象的设计：

### 核心类设计：

1. **Article类** - 博客文章
   - 属性：标题、内容、标签、创建时间、浏览量
   - 方法：增加浏览量、添加标签、格式化显示

2. **User类** - 用户
   - 属性：用户名、邮箱、注册时间
   - 方法：创建文章、获取文章列表

3. **BlogManager类** - 博客管理器
   - 属性：文章列表、用户列表
   - 方法：搜索、统计、推荐

4. **Tag类** - 标签系统
   - 属性：标签名、使用次数
   - 方法：统计、排序

## 📁 文件说明

- `blog_oop.py` - 面向对象版本的博客管理器
- `models.py` - 数据模型类定义
- `examples_oop.py` - OOP概念示例
- `exercises_oop.py` - 面向对象练习题

## 🎮 运行方式

```bash
# 运行面向对象版本的博客管理器
python step2_oop/blog_oop.py

# 查看OOP概念示例
python step2_oop/examples_oop.py

# 完成面向对象练习题
python step2_oop/exercises_oop.py
```

## 💡 学习提示

### 对比函数式 vs 面向对象：

**函数式方式 (第1阶段):**
```python
def create_article(title, content, tags):
    return {"title": title, "content": content, "tags": tags}

def add_view(article):
    article["views"] += 1
```

**面向对象方式 (第2阶段):**
```python
class Article:
    def __init__(self, title, content, tags):
        self.title = title
        self.content = content
        self.tags = tags
    
    def add_view(self):
        self.views += 1
```

### 优势：
- 🏗️ **更好的代码组织**：相关数据和方法组合在一起
- 🔒 **数据封装**：控制数据访问和修改
- 🔄 **代码复用**：通过继承减少重复代码
- 🎯 **更易维护**：修改更局部化，影响范围小

开始学习面向对象编程吧！🏗️
