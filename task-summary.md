# Flask 教程项目创建完成

## 目标
按 Flask 官方教程顺序创建 flaskr 博客应用，每个文件的改动注释说明来自哪篇文章。

## 结果：✅ 全部完成

### 已创建文件结构
```
flask-tutorial/
├── flaskr/
│   ├── __init__.py       # 应用工厂 (文章2+3+4+7)
│   ├── db.py             # 数据库扩展 (文章3)
│   ├── schema.sql        # 数据库表结构 (文章3)
│   ├── auth.py           # 认证蓝图 (文章4)
│   ├── blog.py           # 博客蓝图 (文章7)
│   ├── static/style.css  # 样式表 (文章6)
│   └── templates/
│       ├── base.html     # 基础布局 (文章5)
│       ├── auth/register.html (文章4)
│       ├── auth/login.html (文章4)
│       ├── blog/index.html (文章7)
│       ├── blog/create.html (文章7)
│       └── blog/update.html (文章7)
├── tests/
│   ├── conftest.py       # 测试 fixture (文章9)
│   ├── data.sql          # 测试数据 (文章9)
│   ├── test_factory.py   # 工厂测试
│   ├── test_db.py       # 数据库测试
│   ├── test_auth.py      # 认证测试
│   └── test_blog.py      # 博客测试
├── pyproject.toml        # 项目配置 (文章9)
├── MANIFEST.in           # 打包清单 (文章9)
└── .gitignore            # Git 忽略配置

### 测试结果
- 24 个测试全部通过 ✅
- 代码覆盖率 100% ✅

### 关键决策
- schema.sql 去掉 SQL 注释（SQLite 不支持 `--` 注释），避免 executescript 报错
- 使用用户 Anaconda 环境（Python 3.13.9, Flask 3.1.2, pytest 8.4.2）
- coverage 通过 pip 安装（Anaconda 默认不含）