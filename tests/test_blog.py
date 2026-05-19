# ============================================================
# 文章9: Test Coverage - Blog Tests
# 测试博客文章列表、创建、编辑、删除功能
# ============================================================
import pytest
from flaskr.db import get_db


def test_index(client, auth):
    """
    测试首页：
    - 未登录：显示登录/注册链接
    - 已登录：显示登出链接、文章标题和编辑链接
    """
    response = client.get('/')
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'test title' in response.data
    assert b'by test on 2018-01-01' in response.data
    assert b'test\nbody' in response.data
    assert b'href="/1/update"' in response.data


@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
    '/1/delete',
))
def test_login_required(client, path):
    """
    测试需登录视图：未登录时 POST 重定向到登录页
    """
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"


def test_author_required(app, client, auth):
    """
    测试作者权限：非作者不能编辑/删除他人文章，
    也看不到编辑链接
    """
    # 将第一篇文章的作者改为 other 用户
    with app.app_context():
        db = get_db()
        db.execute('UPDATE post SET author_id = 2 WHERE id = 1')
        db.commit()

    auth.login()
    # 当前用户不能修改其他用户的文章
    assert client.post('/1/update').status_code == 403
    assert client.post('/1/delete').status_code == 403
    # 当前用户看不到编辑链接
    assert b'href="/1/update"' not in client.get('/').data


@pytest.mark.parametrize('path', (
    '/2/update',
    '/2/delete',
))
def test_exists_required(client, auth, path):
    """
    测试文章存在性：不存在返回 404
    """
    auth.login()
    assert client.post(path).status_code == 404


def test_create(client, auth, app):
    """
    测试创建文章：
    - GET 返回 200
    - POST 成功则在数据库插入新文章
    """
    auth.login()
    assert client.get('/create').status_code == 200
    client.post('/create', data={'title': 'created', 'body': ''})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM post').fetchone()[0]
        assert count == 2


def test_update(client, auth, app):
    """
    测试编辑文章：
    - GET 返回 200
    - POST 成功则更新文章标题
    """
    auth.login()
    assert client.get('/1/update').status_code == 200
    client.post('/1/update', data={'title': 'updated', 'body': ''})

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post['title'] == 'updated'


@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
))
def test_create_update_validate(client, auth, path):
    """
    测试创建/编辑验证：标题为空时显示错误消息
    """
    auth.login()
    response = client.post(path, data={'title': '', 'body': ''})
    assert b'Title is required.' in response.data


def test_delete(client, auth, app):
    """
    测试删除文章：
    - POST 成功重定向到首页
    - 文章从数据库中删除
    """
    auth.login()
    response = client.post('/1/delete')
    assert response.headers["Location"] == "/"

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post is None