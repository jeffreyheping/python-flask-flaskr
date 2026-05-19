# ============================================================
# 文章9: Test Coverage - Factory Tests
# 测试应用工厂和 /hello 路由
# ============================================================
from flaskr import create_app


def test_config():
    """
    测试配置传递：
    - 无配置时 testing=False
    - 传入 TESTING=True 时为 True
    """
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    """
    测试 /hello 路由返回 "Hello, World!"
    """
    response = client.get('/hello')
    assert response.data == b'Hello, World!'