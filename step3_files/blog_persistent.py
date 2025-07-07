#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
带持久化功能的博客管理器
学习文件I/O、JSON处理和异常处理的实际应用
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from step2_oop.models import Article, User, BlogManager
from file_manager import FileManager, ConfigManager
import datetime
from typing import Dict, List, Any

class PersistentBlogManager(BlogManager):
    """带持久化功能的博客管理器"""
    
    def __init__(self):
        """初始化持久化博客管理器"""
        super().__init__()
        self.file_manager = FileManager()
        self.config_manager = ConfigManager()
        self._load_all_data()
    
    def _load_all_data(self):
        """加载所有数据"""
        try:
            print("📂 正在加载数据...")
            
            # 加载用户数据
            users_data = self.file_manager.load_json("users.json", [])
            for user_data in users_data:
                try:
                    user = User(user_data["username"], user_data["email"])
                    user._created_at = datetime.datetime.fromisoformat(user_data["created_at"])
                    self._users.append(user)
                except (KeyError, ValueError) as e:
                    print(f"⚠️ 跳过无效用户数据: {e}")
            
            # 加载文章数据
            articles_data = self.file_manager.load_json("articles.json", [])
            for article_data in articles_data:
                try:
                    # 找到对应的用户
                    author_user = self.get_user(article_data["author"])
                    if not author_user:
                        # 如果用户不存在，创建一个临时用户
                        author_user = User(article_data["author"], f"{article_data['author']}@temp.com")
                        self._users.append(author_user)
                    
                    # 创建文章
                    article = Article(
                        article_data["title"],
                        article_data["content"],
                        article_data["author"],
                        article_data.get("tags", [])
                    )
                    
                    # 恢复文章状态
                    article._id = article_data["id"]
                    article._created_at = datetime.datetime.fromisoformat(article_data["created_at"])
                    article._views = article_data.get("views", 0)
                    article._likes = article_data.get("likes", 0)
                    
                    # 添加到用户和管理器
                    author_user._articles.append(article)
                    self._articles.append(article)
                    
                    # 更新标签统计
                    for tag_name in article.tags:
                        if tag_name not in self._tags:
                            from step2_oop.models import Tag
                            self._tags[tag_name] = Tag(tag_name)
                        self._tags[tag_name].increment_usage()
                    
                except (KeyError, ValueError) as e:
                    print(f"⚠️ 跳过无效文章数据: {e}")
            
            # 更新文章计数器
            if self._articles:
                Article._article_count = max(article.id for article in self._articles)
            
            print(f"✅ 数据加载完成: {len(self._users)} 个用户, {len(self._articles)} 篇文章")
            
        except Exception as e:
            print(f"❌ 加载数据时出错: {e}")
    
    def _save_all_data(self):
        """保存所有数据"""
        try:
            if not self.config_manager.get("auto_save", True):
                return
            
            print("💾 正在保存数据...")
            
            # 保存用户数据
            users_data = []
            for user in self._users:
                users_data.append({
                    "username": user.username,
                    "email": user.email,
                    "created_at": user.created_at.isoformat()
                })
            
            # 保存文章数据
            articles_data = []
            for article in self._articles:
                articles_data.append({
                    "id": article.id,
                    "title": article.title,
                    "content": article.content,
                    "author": article.author,
                    "tags": article.tags,
                    "created_at": article.created_at.isoformat(),
                    "views": article.views,
                    "likes": article.likes
                })
            
            # 执行保存
            users_saved = self.file_manager.save_json("users.json", users_data)
            articles_saved = self.file_manager.save_json("articles.json", articles_data)
            
            if users_saved and articles_saved:
                print("✅ 数据保存成功")
            else:
                print("⚠️ 部分数据保存失败")
                
        except Exception as e:
            print(f"❌ 保存数据时出错: {e}")
    
    def add_user(self, username: str, email: str) -> User:
        """添加用户（重写以支持自动保存）"""
        user = super().add_user(username, email)
        self._save_all_data()
        return user
    
    def add_article(self, article: Article) -> None:
        """添加文章（重写以支持自动保存）"""
        super().add_article(article)
        self._save_all_data()
    
    def backup_data(self) -> bool:
        """手动备份数据"""
        try:
            print("📦 正在创建数据备份...")
            
            users_backup = self.file_manager._create_backup("users.json")
            articles_backup = self.file_manager._create_backup("articles.json")
            
            if users_backup and articles_backup:
                print("✅ 数据备份完成")
                return True
            else:
                print("⚠️ 部分数据备份失败")
                return False
                
        except Exception as e:
            print(f"❌ 备份数据时出错: {e}")
            return False
    
    def restore_from_backup(self, backup_date: str = None) -> bool:
        """从备份恢复数据"""
        try:
            print("🔄 正在从备份恢复数据...")
            
            # 列出可用备份
            users_backups = self.file_manager.list_backups("users.json")
            articles_backups = self.file_manager.list_backups("articles.json")
            
            if not users_backups or not articles_backups:
                print("❌ 没有找到可用的备份文件")
                return False
            
            # 如果没有指定日期，使用最新的备份
            if backup_date is None:
                users_backup = users_backups[0]
                articles_backup = articles_backups[0]
            else:
                # 查找指定日期的备份
                users_backup = None
                articles_backup = None
                for backup in users_backups:
                    if backup_date in backup.name:
                        users_backup = backup
                        break
                for backup in articles_backups:
                    if backup_date in backup.name:
                        articles_backup = backup
                        break
                
                if not users_backup or not articles_backup:
                    print(f"❌ 没有找到日期为 {backup_date} 的备份")
                    return False
            
            # 执行恢复
            users_restored = self.file_manager.restore_backup("users.json", users_backup)
            articles_restored = self.file_manager.restore_backup("articles.json", articles_backup)
            
            if users_restored and articles_restored:
                # 重新加载数据
                self._users.clear()
                self._articles.clear()
                self._tags.clear()
                self._load_all_data()
                print("✅ 数据恢复完成")
                return True
            else:
                print("❌ 数据恢复失败")
                return False
                
        except Exception as e:
            print(f"❌ 恢复数据时出错: {e}")
            return False
    
    def export_blog_data(self, export_path: str) -> bool:
        """导出博客数据"""
        try:
            # 先保存当前数据
            self._save_all_data()
            
            # 导出数据
            return self.file_manager.export_data(export_path)
            
        except Exception as e:
            print(f"❌ 导出数据时出错: {e}")
            return False
    
    def import_blog_data(self, import_path: str, merge: bool = False) -> bool:
        """导入博客数据"""
        try:
            if not merge:
                # 备份当前数据
                self.backup_data()
                
                # 清空当前数据
                self._users.clear()
                self._articles.clear()
                self._tags.clear()
            
            # 导入数据
            if self.file_manager.import_data(import_path, overwrite=not merge):
                # 重新加载数据
                self._load_all_data()
                print("✅ 数据导入完成")
                return True
            else:
                print("❌ 数据导入失败")
                return False
                
        except Exception as e:
            print(f"❌ 导入数据时出错: {e}")
            return False
    
    def get_data_statistics(self) -> Dict[str, Any]:
        """获取数据统计信息"""
        try:
            stats = super().get_statistics()
            
            # 添加文件信息
            users_info = self.file_manager.get_file_info("users.json")
            articles_info = self.file_manager.get_file_info("articles.json")
            
            stats.update({
                "users_file_size": users_info["size_human"] if users_info else "N/A",
                "articles_file_size": articles_info["size_human"] if articles_info else "N/A",
                "last_saved": articles_info["modified"] if articles_info else None,
                "backup_count": len(self.file_manager.list_backups("articles.json"))
            })
            
            return stats
            
        except Exception as e:
            print(f"❌ 获取统计信息时出错: {e}")
            return {}
    
    def cleanup_old_data(self, days: int = 30) -> int:
        """清理旧数据"""
        return self.file_manager.cleanup_old_backups(days)

class PersistentBlogApp:
    """带持久化功能的博客应用"""
    
    def __init__(self):
        """初始化应用"""
        self.blog_manager = PersistentBlogManager()
        self.current_user = None
    
    def show_main_menu(self):
        """显示主菜单"""
        print("\n🐍 Python持久化博客管理器")
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
        print("5. 💾 数据管理")
        print("6. ⚙️ 系统设置")
        print("0. 🚪 退出程序")
        print("-" * 40)
    
    def data_management_menu(self):
        """数据管理菜单"""
        while True:
            print("\n💾 数据管理")
            print("-" * 20)
            print("1. 📦 创建备份")
            print("2. 🔄 从备份恢复")
            print("3. 📤 导出数据")
            print("4. 📥 导入数据")
            print("5. 📋 查看备份列表")
            print("6. 🧹 清理旧备份")
            print("7. 📊 数据统计")
            print("0. 返回主菜单")
            
            choice = input("请选择操作: ").strip()
            
            if choice == "1":
                self._create_backup()
            elif choice == "2":
                self._restore_backup()
            elif choice == "3":
                self._export_data()
            elif choice == "4":
                self._import_data()
            elif choice == "5":
                self._list_backups()
            elif choice == "6":
                self._cleanup_backups()
            elif choice == "7":
                self._show_data_stats()
            elif choice == "0":
                break
            else:
                print("❌ 无效选择")
    
    def _create_backup(self):
        """创建备份"""
        if self.blog_manager.backup_data():
            print("✅ 备份创建成功")
        else:
            print("❌ 备份创建失败")
    
    def _restore_backup(self):
        """从备份恢复"""
        backups = self.blog_manager.file_manager.list_backups("articles.json")
        if not backups:
            print("❌ 没有可用的备份")
            return
        
        print("\n📋 可用备份:")
        for i, backup in enumerate(backups[:10], 1):  # 只显示最近10个
            print(f"  {i}. {backup.name}")
        
        try:
            choice = input("\n选择备份编号 (回车使用最新备份): ").strip()
            if choice:
                backup_index = int(choice) - 1
                if 0 <= backup_index < len(backups):
                    backup_date = backups[backup_index].name.split("_backup_")[1].split(".")[0]
                    if self.blog_manager.restore_from_backup(backup_date):
                        print("✅ 数据恢复成功")
                    else:
                        print("❌ 数据恢复失败")
                else:
                    print("❌ 无效的备份编号")
            else:
                if self.blog_manager.restore_from_backup():
                    print("✅ 数据恢复成功")
                else:
                    print("❌ 数据恢复失败")
        except ValueError:
            print("❌ 请输入有效的数字")
    
    def _export_data(self):
        """导出数据"""
        export_path = input("请输入导出目录路径: ").strip()
        if not export_path:
            export_path = f"export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if self.blog_manager.export_blog_data(export_path):
            print(f"✅ 数据已导出到: {export_path}")
        else:
            print("❌ 数据导出失败")
    
    def _import_data(self):
        """导入数据"""
        import_path = input("请输入导入目录路径: ").strip()
        if not import_path:
            print("❌ 路径不能为空")
            return
        
        merge_choice = input("是否与现有数据合并? (y/n): ").lower().strip()
        merge = merge_choice == 'y'
        
        if self.blog_manager.import_blog_data(import_path, merge):
            print("✅ 数据导入成功")
        else:
            print("❌ 数据导入失败")
    
    def _list_backups(self):
        """列出备份"""
        backups = self.blog_manager.file_manager.list_backups("articles.json")
        if not backups:
            print("📭 没有备份文件")
            return
        
        print(f"\n📋 备份文件列表 (共 {len(backups)} 个):")
        for backup in backups:
            stat = backup.stat()
            size = self.blog_manager.file_manager._format_size(stat.st_size)
            modified = datetime.datetime.fromtimestamp(stat.st_mtime)
            print(f"  📦 {backup.name}")
            print(f"     大小: {size} | 时间: {modified.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def _cleanup_backups(self):
        """清理备份"""
        try:
            days = int(input("请输入保留天数 (默认30天): ").strip() or "30")
            deleted_count = self.blog_manager.cleanup_old_data(days)
            print(f"✅ 已清理 {deleted_count} 个旧备份")
        except ValueError:
            print("❌ 请输入有效的天数")
    
    def _show_data_stats(self):
        """显示数据统计"""
        stats = self.blog_manager.get_data_statistics()
        
        print(f"\n📊 数据统计信息")
        print("=" * 30)
        print(f"📝 文章总数: {stats.get('total_articles', 0)}")
        print(f"👤 用户总数: {stats.get('total_users', 0)}")
        print(f"🏷️ 标签总数: {stats.get('total_tags', 0)}")
        print(f"👀 总浏览量: {stats.get('total_views', 0)}")
        print(f"📦 备份数量: {stats.get('backup_count', 0)}")
        print(f"📄 用户文件大小: {stats.get('users_file_size', 'N/A')}")
        print(f"📄 文章文件大小: {stats.get('articles_file_size', 'N/A')}")
        
        if stats.get('last_saved'):
            print(f"💾 最后保存: {stats['last_saved'].strftime('%Y-%m-%d %H:%M:%S')}")
    
    def run(self):
        """运行应用"""
        print("🎉 欢迎使用Python持久化博客管理器！")
        print("💡 您的数据将自动保存到文件中")
        
        while True:
            try:
                self.show_main_menu()
                choice = input("请选择操作 (0-6): ").strip()
                
                if choice == "1":
                    # 用户管理 (复用之前的代码)
                    pass
                elif choice == "2":
                    # 文章管理 (复用之前的代码)
                    pass
                elif choice == "3":
                    # 搜索功能 (复用之前的代码)
                    pass
                elif choice == "4":
                    # 统计信息
                    self._show_data_stats()
                elif choice == "5":
                    self.data_management_menu()
                elif choice == "6":
                    # 系统设置
                    self._system_settings()
                elif choice == "0":
                    print("\n💾 正在保存数据...")
                    self.blog_manager._save_all_data()
                    print("👋 感谢使用Python持久化博客管理器！")
                    print("🎓 继续学习下一阶段：Web开发基础")
                    break
                else:
                    print("❌ 无效选择，请输入 0-6 之间的数字")
                    
            except KeyboardInterrupt:
                print("\n\n💾 正在保存数据...")
                self.blog_manager._save_all_data()
                print("👋 程序被用户中断，数据已保存！")
                break
            except Exception as e:
                print(f"❌ 程序出错: {e}")
    
    def _system_settings(self):
        """系统设置"""
        config = self.blog_manager.config_manager
        
        print(f"\n⚙️ 系统设置")
        print("=" * 20)
        print(f"应用名称: {config.get('app_name')}")
        print(f"版本: {config.get('version')}")
        print(f"自动保存: {'开启' if config.get('auto_save') else '关闭'}")
        print(f"自动备份: {'开启' if config.get('auto_backup') else '关闭'}")
        print(f"备份间隔: {config.get('backup_interval_days')} 天")
        print(f"最大备份数: {config.get('max_backups')}")
        
        modify = input("\n是否修改设置? (y/n): ").lower().strip()
        if modify == 'y':
            try:
                auto_save = input(f"自动保存 (当前: {config.get('auto_save')}) [y/n]: ").lower().strip()
                if auto_save in ['y', 'n']:
                    config.set('auto_save', auto_save == 'y')
                
                config.save_config()
                print("✅ 设置已保存")
            except Exception as e:
                print(f"❌ 保存设置失败: {e}")

def main():
    """主函数"""
    app = PersistentBlogApp()
    app.run()

if __name__ == "__main__":
    main()
