## 命名约定
命名要语义化，使用用英文单词，不要缩写除非是众所周知的缩写 \
本规范使用:

1. 驼峰式命名(camelCase)：单个命名中，首个词是以小写字母开头，后面每个词都是以大写字母开始
2. 帕斯卡命名(PascalCase)：单个命名中，每个词都是以大写字母开始
3. 烤串命名(kebab-case)：单个命名中，每个单词都是小写的，之间用连字符 - 连接
4. 蛇形命名(SNAKE_CASE)：单个命名中，每个单词都是大写的，之间用下划线 \_ 连接

|         命名法         | 使用场景                                                      |
| :--------------------: | :------------------------------------------------------------ |
| 帕斯卡命名 PascalCase  | 类名、接口名、枚举名、类型名             |
|  蛇形命名 SNAKE_CASE   | 常量、静态变更、普通变量、类变量、类属性、函数、函数参数              |
|  烤串命名 kebab-case   | 文件名、路由 path |
| 小驼峰式命名 camelCase |               |
| 名词复数形式           |  路由          | 


## 环境
```sh
# 安装 uv https://github.com/astral-sh/uv
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

```

## uv 常用操作
```sh
uv venv 
uv venv --python 3.12.8

# 检查虚拟环境
which python
# 激活虚拟环境
# windows bash
source .venv/Scripts/activate 
# linux
source .venv/bin/activate
# 退出虚拟环境
deactivate

# 临时指定镜像源
# 清华大学的 PyPI 镜像源
uv add --default-index https://pypi.tuna.tsinghua.edu.cn/simple requests
# 阿里云 PyPI 镜像源
uv add --default-index https://mirrors.aliyun.com/pypi/simple requests

# 在 pyproject.toml 中添加
[[tool.uv.index]]
url = "https://pypi.tuna.tsinghua.edu.cn/simple"
default = true


uv python install 3.12.8
uv python dir
uv python list
uv python list --only-installed
uv python uninstall
# 锁定当前项目 python 版本
uv python pin 3.12.8
# 切换Python版本
uv python use 3.10

# 安装 fastapi
uv add "fastapi[all]"
或
uv add "fastapi[standard]"

uv init 创建项目
uv sync 同步项目依赖
uv add 
uv add --group dev
uv add --group production

uv pip install
uv pip install -r requirements.txt

# 生成标准的 requirements.txt 文件
uv pip compile pyproject.toml -o requirements.txt

# 从多源编译依赖
uv pip compile pyproject.toml requirements-dev.in -o requirements-dev.txt

```

## 目录结构

## 组件管理：使用依赖注入
```python
from fastapi import Depends, FastAPI
from app.services.user_service import UserService

app = FastAPI()


# 通过 get_user_service 函数创建组件实例
def get_user_service():
    return UserService()

# 使用 Depends 来注入该实例 get_user_service
@app.get("/users/{user_id}")
async def read_user(user_id: int, service: UserService = Depends(get_user_service)):
    return service.get_user_by_id(user_id)
```

## 修改接⼝⽂档的资源地址
修改 fastapi 源代码 `.venv/Lib/site-packages/fastapi/openapi/docs.py`
把 `swagger_js_url` 修改为 `"/static/swagger-ui-bundle.js"`
把 `swagger_css_url` 修改为 `"/static/swagger-ui.css"`
把 `swagger_favicon_url` 修改为 `"/static/favicon.png"`
在app中注册static⽬录
```python

```

