# ============================================================
# 文章9: Test Coverage - Setup and Fixtures
# 测试配置：临时数据库、应用/客户端 fixture、认证辅助类
# ============================================================
import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    """
    应用 fixture：创建临时数据库并填充测试数据。
    """
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """
    测试客户端 fixture：模拟浏览器请求。
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    CLI 测试 runner：可调用 Click 命令。
    """
    return app.test_cli_runner()


# ============================================================
# 文章9: AuthActions 辅助类 - 登录/登出
# ============================================================
class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)