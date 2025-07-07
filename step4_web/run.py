#!/usr/bin/env python3
"""
Flask应用启动脚本
提供便捷的启动选项和环境配置
"""

import os
import sys
import argparse
from app import create_app

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='启动Flask博客应用')
    parser.add_argument('--env', choices=['development', 'production', 'testing'], 
                       default='development', help='运行环境')
    parser.add_argument('--host', default='127.0.0.1', help='主机地址')
    parser.add_argument('--port', type=int, default=5000, help='端口号')
    parser.add_argument('--debug', action='store_true', help='启用调试模式')
    parser.add_argument('--init-data', action='store_true', help='初始化演示数据')
    
    args = parser.parse_args()
    
    # 设置环境变量
    os.environ['FLASK_ENV'] = args.env
    if args.debug:
        os.environ['FLASK_DEBUG'] = '1'
    
    # 初始化演示数据
    if args.init_data:
        print("🚀 初始化演示数据...")
        try:
            from init_demo_data import main as init_data
            if init_data():
                print("✅ 演示数据初始化成功！")
            else:
                print("❌ 演示数据初始化失败！")
                return
        except ImportError:
            print("❌ 找不到演示数据初始化脚本")
            return
        except Exception as e:
            print(f"❌ 初始化演示数据时出错: {e}")
            return
    
    # 创建应用
    try:
        app = create_app(args.env)
    except Exception as e:
        print(f"❌ 创建应用失败: {e}")
        return
    
    # 显示启动信息
    print(f"""
🌐 Flask博客应用启动中...

📋 配置信息:
   环境: {args.env}
   主机: {args.host}
   端口: {args.port}
   调试: {'开启' if args.debug else '关闭'}

🔗 访问地址:
   本地: http://{args.host}:{args.port}
   网络: http://localhost:{args.port}

🔑 演示账户:
   管理员: admin / admin123
   演示用户: demo / demo123

💡 提示:
   - 按 Ctrl+C 停止服务器
   - 修改代码后会自动重载 (调试模式)
   - 查看 README.md 了解更多功能

🚀 启动完成！
""")
    
    # 启动应用
    try:
        app.run(
            host=args.host,
            port=args.port,
            debug=args.debug,
            use_reloader=args.debug,
            use_debugger=args.debug
        )
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 运行时错误: {e}")

if __name__ == '__main__':
    main()
