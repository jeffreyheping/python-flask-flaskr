# ============================================================
# 文章9: Test Coverage - Database Tests
# 测试数据库连接和 init-db 命令
# ============================================================
import sqlite3

import pytest
from flaskr.db import get_db


def test_get_close_db(app):
    """
    测试 get_db() 在请求上下文中返回同一连接，
    上下文字后连接被关闭。
    """
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)


def test_init_db_command(runner, monkeypatch):
    """
    测试 flask init-db 命令调用 init_db() 并输出成功消息。
    使用 monkeypatch 模拟 init_db 以验证调用。
    """
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called