# ============================================================
# 文章3: Define and Access the Database
# 数据库连接、初始化及 CLI 命令
# ============================================================
import sqlite3
from datetime import datetime

import click
from flask import current_app, g


# ============================================================
# 文章3: Connect to the Database
# ============================================================

def get_db():
    """
    获取当前请求的数据库连接。
    文章3: 使用 g 对象存储连接，同一请求内复用。
    """
    if 'db' not in g:
        # 连接数据库，detect_types 使 sqlite3 自动识别 Python 类型
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Row 使结果像字典一样按列名访问
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """
    请求结束后关闭数据库连接。
    文章3: 通过 teardown_appcontext 注册，在响应结束后自动调用。
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()


# ============================================================
# 文章3: Register timestamp converter
# ============================================================
# 将数据库 timestamp 字符串转换为 Python datetime 对象
sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)


# ============================================================
# 文章3: Create the Tables
# ============================================================

def init_db():
    """
    初始化数据库，执行 schema.sql 创建表。
    文章3: 从 flaskr 包内读取 schema.sql 并执行。
    """
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """
    Flask CLI 命令：flask init-db
    文章3: 创建可调用命令用于初始化数据库。
    """
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


# ============================================================
# 文章3: Register with the Application
# ============================================================

def init_app(app):
    """
    将数据库函数注册到 Flask 应用。
    文章3: 注册 teardown 和 CLI 命令，使工厂函数可调用。
    """
    # 请求结束后自动关闭数据库连接
    app.teardown_appcontext(close_db)
    # 添加 flask init-db 命令
    app.cli.add_command(init_db_command)