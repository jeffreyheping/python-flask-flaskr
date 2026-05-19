# Flaskr - The Flask Tutorial Blog

## 前世今生

### 起源
这是一个"从零开始学 Flask"的练手项目。

教程来自 [Flask 官方文档](https://flask.palletsprojects.com/en/stable/tutorial/)，共 12 篇文章，涵盖：

1. **Project Layout** — 项目目录结构
2. **Application Setup** — 应用工厂模式
3. **Define and Access the Database** — SQLite 数据库 + CLI 命令
4. **Blueprints and Views** — 认证蓝图（注册/登录/登出）
5. **Templates** — Jinja2 模板继承
6. **Static Files** — CSS 样式
7. **Blog Blueprint** — 博客蓝图（增删改查）
8. **Make the Project Installable** — 可安装为包
9. **Test Coverage** — 单元测试 + 覆盖率
10. **Keep Developing** — 开发中注意事项
11. **Deploy to Production** — 生产环境部署
12. **What's Next** — 下一步

### 过程
整个项目由 AI 助手（QClaw）根据官方教程按顺序创建，过程中踩了几个坑：

- **SQL 注释问题**：schema.sql 里写了 `--` 注释，SQLite 的 `executescript` 把 `--` 当作无效 token → 去掉所有 SQL 注释
- **URL 摸索**：一开始用错了 Flask 文档 URL 格式（`/stable/layout/`），404 了好几次才找到正确的 `/stable/tutorial/` 格式
- **环境复用**：没有新建虚拟环境，直接用了用户已有的 Anaconda（Python 3.13.9），Flask 和 pytest 都是现成的，只额外装了 coverage

### 结果
- 24 个单元测试全部通过
- 代码覆盖率 100%
- 项目已 push 到 GitHub

### 技术栈

| 组件 | 技术 |
|------|------|
| Web 框架 | Flask 3.1 |
| 数据库 | SQLite |
| 前端模板 | Jinja2 |
| 测试 | pytest + coverage |
| 打包 | pyproject.toml + flit |

### 快速上手

```bash
# 初始化数据库
flask --app flaskr init-db

# 启动开发服务器
flask --app flaskr run --debug

# 运行测试
pytest -v

# 查看覆盖率
coverage run -m pytest
coverage report
```

> 博客运行在 http://127.0.0.1:5000，注册账号后即可发帖。
