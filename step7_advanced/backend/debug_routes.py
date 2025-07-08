#!/usr/bin/env python3
"""
调试路由注册
"""

from app import create_app

app = create_app()

print("注册的路由:")
for rule in app.url_map.iter_rules():
    print(f"{rule.rule} -> {rule.endpoint} ({rule.methods})")
