# ============================================================
# 文章1: Project Layout
# 新建 flaskr 目录，作为 Python 包
# ============================================================

# ============================================================
# 文章2: Application Setup
# 创建 Flask 应用工厂 create_app()
# ============================================================
import os

from flask import Flask


def create_app(test_config=None):
    """
    应用工厂函数。
    文章2: Application Setup - 取代全局 Flask 实例，
    在函数内创建和配置应用，便于测试和扩展。
    """
    # 创建 Flask 实例
    # __name__ 告诉 Flask 当前模块路径，instance_relative_config=True
    # 使配置文件相对于 instance 文件夹（存放本地敏感数据如数据库）
    app = Flask(__name__, instance_relative_config=True)

    # 设置默认配置：密钥（开发用）和数据库路径
    # SECRET_KEY 用于安全签名会话数据等
    # DATABASE 指向 instance 目录下的 SQLite 数据库文件
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # 如果没有传入测试配置，加载 instance/config.py（若存在）
    # 若有测试配置则覆盖默认配置
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # 确保 instance 文件夹存在（Flask 不会自动创建）
    os.makedirs(app.instance_path, exist_ok=True)

    # ----------------------------------------
    # 文章2: 添加 /hello 路由用于验证应用运行
    # ----------------------------------------
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # ============================================================
    # 文章3: Define and Access the Database
    # 注册数据库扩展（db.init_app 在 db.py 中定义）
    # ============================================================
    from . import db
    db.init_app(app)

    # ============================================================
    # 文章4: Blueprints and Views
    # 注册 auth 蓝图（登录/注册/登出功能）
    # ============================================================
    from . import auth
    app.register_blueprint(auth.bp)

    # ============================================================
    # 文章7: Blog Blueprint
    # 注册 blog 蓝图，并将 index 端点映射到 /
    # ============================================================
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app