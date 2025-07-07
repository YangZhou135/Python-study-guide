#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件管理器
学习文件I/O操作、JSON处理和异常处理
"""

import json
import os
import shutil
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

class FileManager:
    """文件管理器类"""
    
    def __init__(self, data_dir: str = "data"):
        """
        初始化文件管理器
        
        Args:
            data_dir: 数据目录路径
        """
        self.data_dir = Path(data_dir)
        self.backup_dir = self.data_dir / "backups"
        self._ensure_directories()
    
    def _ensure_directories(self):
        """确保必要的目录存在"""
        try:
            self.data_dir.mkdir(exist_ok=True)
            self.backup_dir.mkdir(exist_ok=True)
            print(f"✅ 数据目录已准备: {self.data_dir}")
        except OSError as e:
            print(f"❌ 创建目录失败: {e}")
            raise
    
    def save_json(self, filename: str, data: Any, backup: bool = True) -> bool:
        """
        保存数据到JSON文件
        
        Args:
            filename: 文件名
            data: 要保存的数据
            backup: 是否创建备份
            
        Returns:
            bool: 保存是否成功
        """
        file_path = self.data_dir / filename
        
        try:
            # 如果文件存在且需要备份，先创建备份
            if backup and file_path.exists():
                self._create_backup(filename)
            
            # 保存数据
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=self._json_serializer)
            
            print(f"✅ 数据已保存到: {file_path}")
            return True
            
        except (IOError, json.JSONEncodeError) as e:
            print(f"❌ 保存文件失败: {e}")
            return False
    
    def load_json(self, filename: str, default: Any = None) -> Any:
        """
        从JSON文件加载数据
        
        Args:
            filename: 文件名
            default: 文件不存在时的默认值
            
        Returns:
            加载的数据或默认值
        """
        file_path = self.data_dir / filename
        
        try:
            if not file_path.exists():
                print(f"📄 文件不存在，使用默认值: {filename}")
                return default
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"✅ 数据已加载: {file_path}")
            return data
            
        except (IOError, json.JSONDecodeError) as e:
            print(f"❌ 加载文件失败: {e}")
            return default
    
    def _create_backup(self, filename: str) -> bool:
        """
        创建文件备份
        
        Args:
            filename: 要备份的文件名
            
        Returns:
            bool: 备份是否成功
        """
        try:
            source_path = self.data_dir / filename
            if not source_path.exists():
                return False
            
            # 生成备份文件名（包含时间戳）
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{source_path.stem}_backup_{timestamp}{source_path.suffix}"
            backup_path = self.backup_dir / backup_filename
            
            # 复制文件
            shutil.copy2(source_path, backup_path)
            print(f"📦 备份已创建: {backup_path}")
            return True
            
        except (IOError, OSError) as e:
            print(f"❌ 创建备份失败: {e}")
            return False
    
    def list_backups(self, filename: str) -> List[Path]:
        """
        列出指定文件的所有备份
        
        Args:
            filename: 原文件名
            
        Returns:
            备份文件路径列表
        """
        try:
            file_stem = Path(filename).stem
            pattern = f"{file_stem}_backup_*"
            backups = list(self.backup_dir.glob(pattern))
            backups.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            return backups
        except OSError:
            return []
    
    def restore_backup(self, filename: str, backup_path: Path) -> bool:
        """
        从备份恢复文件
        
        Args:
            filename: 目标文件名
            backup_path: 备份文件路径
            
        Returns:
            bool: 恢复是否成功
        """
        try:
            target_path = self.data_dir / filename
            shutil.copy2(backup_path, target_path)
            print(f"🔄 已从备份恢复: {backup_path} -> {target_path}")
            return True
        except (IOError, OSError) as e:
            print(f"❌ 恢复备份失败: {e}")
            return False
    
    def export_data(self, export_path: str) -> bool:
        """
        导出所有数据到指定目录
        
        Args:
            export_path: 导出目录路径
            
        Returns:
            bool: 导出是否成功
        """
        try:
            export_dir = Path(export_path)
            export_dir.mkdir(exist_ok=True)
            
            # 复制所有JSON文件
            json_files = list(self.data_dir.glob("*.json"))
            for json_file in json_files:
                target_file = export_dir / json_file.name
                shutil.copy2(json_file, target_file)
            
            print(f"📤 数据已导出到: {export_dir}")
            print(f"   导出文件数: {len(json_files)}")
            return True
            
        except (IOError, OSError) as e:
            print(f"❌ 导出数据失败: {e}")
            return False
    
    def import_data(self, import_path: str, overwrite: bool = False) -> bool:
        """
        从指定目录导入数据
        
        Args:
            import_path: 导入目录路径
            overwrite: 是否覆盖现有文件
            
        Returns:
            bool: 导入是否成功
        """
        try:
            import_dir = Path(import_path)
            if not import_dir.exists():
                print(f"❌ 导入目录不存在: {import_dir}")
                return False
            
            json_files = list(import_dir.glob("*.json"))
            imported_count = 0
            
            for json_file in json_files:
                target_file = self.data_dir / json_file.name
                
                if target_file.exists() and not overwrite:
                    print(f"⚠️ 文件已存在，跳过: {json_file.name}")
                    continue
                
                # 验证JSON格式
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        json.load(f)
                except json.JSONDecodeError:
                    print(f"❌ 无效的JSON文件，跳过: {json_file.name}")
                    continue
                
                shutil.copy2(json_file, target_file)
                imported_count += 1
            
            print(f"📥 数据导入完成: {imported_count} 个文件")
            return True
            
        except (IOError, OSError) as e:
            print(f"❌ 导入数据失败: {e}")
            return False
    
    def get_file_info(self, filename: str) -> Optional[Dict[str, Any]]:
        """
        获取文件信息
        
        Args:
            filename: 文件名
            
        Returns:
            文件信息字典或None
        """
        try:
            file_path = self.data_dir / filename
            if not file_path.exists():
                return None
            
            stat = file_path.stat()
            return {
                "filename": filename,
                "size": stat.st_size,
                "created": datetime.datetime.fromtimestamp(stat.st_ctime),
                "modified": datetime.datetime.fromtimestamp(stat.st_mtime),
                "size_human": self._format_size(stat.st_size)
            }
        except OSError:
            return None
    
    def cleanup_old_backups(self, days: int = 30) -> int:
        """
        清理旧备份文件
        
        Args:
            days: 保留天数
            
        Returns:
            删除的文件数量
        """
        try:
            cutoff_time = datetime.datetime.now() - datetime.timedelta(days=days)
            deleted_count = 0
            
            for backup_file in self.backup_dir.glob("*_backup_*"):
                if datetime.datetime.fromtimestamp(backup_file.stat().st_mtime) < cutoff_time:
                    backup_file.unlink()
                    deleted_count += 1
            
            print(f"🧹 已清理 {deleted_count} 个旧备份文件")
            return deleted_count
            
        except OSError as e:
            print(f"❌ 清理备份失败: {e}")
            return 0
    
    @staticmethod
    def _json_serializer(obj):
        """JSON序列化器，处理特殊对象"""
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        else:
            return str(obj)
    
    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """格式化文件大小"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"

class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: str = "config.json"):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件名
        """
        self.file_manager = FileManager()
        self.config_file = config_file
        self.config = self._load_default_config()
        self.load_config()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """加载默认配置"""
        return {
            "app_name": "Python博客管理器",
            "version": "3.0.0",
            "auto_save": True,
            "auto_backup": True,
            "backup_interval_days": 7,
            "max_backups": 10,
            "data_format": "json",
            "encoding": "utf-8",
            "theme": "default",
            "language": "zh-CN"
        }
    
    def load_config(self) -> bool:
        """加载配置文件"""
        try:
            loaded_config = self.file_manager.load_json(self.config_file, {})
            if loaded_config:
                self.config.update(loaded_config)
                print("✅ 配置文件已加载")
            else:
                print("📄 使用默认配置")
            return True
        except Exception as e:
            print(f"❌ 加载配置失败: {e}")
            return False
    
    def save_config(self) -> bool:
        """保存配置文件"""
        return self.file_manager.save_json(self.config_file, self.config, backup=False)
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """设置配置值"""
        self.config[key] = value
    
    def reset_to_default(self) -> None:
        """重置为默认配置"""
        self.config = self._load_default_config()
        print("🔄 配置已重置为默认值")
