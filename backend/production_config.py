"""
生产环境配置
使用 Gunicorn 或 uWSGI 等 WSGI 服务器部署
"""
import os
from app import app, init_database

# 生产环境配置
app.config['DEBUG'] = False
app.config['TESTING'] = False

# 初始化数据库
if not init_database():
    print("数据库初始化失败")
    exit(1)

if __name__ == '__main__':
    # 生产环境不应该直接运行这个文件
    # 应该使用: gunicorn production_config:app
    print("警告：这是生产环境配置文件")
    print("请使用 WSGI 服务器运行，例如：")
    print("gunicorn production_config:app")
    print("或")
    print("waitress-serve --port=5000 production_config:app")
