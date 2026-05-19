# ============================================================
# 文章9: Test Coverage - Authentication Tests
# 测试注册、登录、登出视图
# ============================================================
import pytest
from flask import g, session
from flaskr.db import get_db


def test_register(client, app):
    """
    测试注册：
    - GET 请求返回 200
    - POST 有效数据重定向到登录页，用户写入数据库
    """
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    """
    测试注册验证：各种无效输入显示对应错误消息
    """
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    """
    测试登录：
    - GET 请求返回 200
    - POST 成功重定向到首页，session 存储 user_id
    """
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    """
    测试登录验证：用户名或密码错误时显示对应消息
    """
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    """
    测试登出：session 中 user_id 被清除
    """
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session