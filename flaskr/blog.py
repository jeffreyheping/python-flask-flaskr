# ============================================================
# 文章7: Blog Blueprint
# 博客蓝图：文章列表、创建、编辑、删除功能
# ============================================================
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

# ============================================================
# 文章7: The Blueprint
# 创建博客蓝图，无 url_prefix，根路由 /
# ============================================================
bp = Blueprint('blog', __name__)


# ============================================================
# 文章7: 获取文章（带作者校验）
# ============================================================
def get_post(id, check_author=True):
    """
    根据 id 获取文章（含作者信息）。
    check_author=True 时校验当前用户是否为作者。
    文章不存在返回 404，作者不匹配返回 403。
    """
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


# ============================================================
# 文章7: Index - 文章列表页
# ============================================================
@bp.route('/')
def index():
    """
    显示所有文章（最新在前），JOIN 查询作者用户名。
    登录用户显示"新建"链接；文章作者可看到"编辑"链接。
    """
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


# ============================================================
# 文章7: Create - 创建文章
# ============================================================
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """
    创建新文章。
    GET: 渲染创建表单
    POST: 验证标题，插入数据库，重定向到首页
    """
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


# ============================================================
# 文章7: Update - 编辑文章
# ============================================================
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """
    编辑已有文章。
    GET: 渲染编辑表单（预填现有内容）
    POST: 验证标题，更新数据库，重定向到首页
    """
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


# ============================================================
# 文章7: Delete - 删除文章
# ============================================================
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    """
    删除文章（仅 POST），重定向到首页。
    不需要单独模板，删除按钮在 update.html 中。
    """
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))