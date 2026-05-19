# ============================================================
# 文章4: Blueprints and Views
# 认证蓝图：注册、登录、登出功能
# ============================================================
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# ============================================================
# 文章4: Create a Blueprint
# 创建认证蓝图，url_prefix='/auth' 挂载到 /auth 下的所有路由
# ============================================================
bp = Blueprint('auth', __name__, url_prefix='/auth')


# ============================================================
# 文章4: The First View: Register
# ============================================================
@bp.route('/register', methods=('GET', 'POST'))
def register():
    """
    用户注册视图。
    GET: 渲染注册表单
    POST: 验证输入，创建用户，重定向到登录页
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                # 使用 werkzeug 的安全哈希函数存储密码
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


# ============================================================
# 文章4: Login
# ============================================================
@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    用户登录视图。
    GET: 渲染登录表单
    POST: 验证用户名和密码，成功则写入 session
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


# ============================================================
# 文章4: 在每个请求前加载已登录用户信息到 g.user
# ============================================================
@bp.before_app_request
def load_logged_in_user():
    """
    请求开始前检查 session 中的 user_id，
    将用户信息存入 g.user，供所有视图访问。
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


# ============================================================
# 文章4: Logout
# ============================================================
@bp.route('/logout')
def logout():
    """
    清除 session 中的用户信息，实现登出。
    """
    session.clear()
    return redirect(url_for('index'))


# ============================================================
# 文章4: Require Authentication in Other Views
# 登录验证装饰器：未登录用户重定向到登录页
# ============================================================
def login_required(view):
    """
    装饰器：确保用户已登录，否则重定向到登录页。
    用于保护需要认证的视图，如创建/编辑文章。
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view