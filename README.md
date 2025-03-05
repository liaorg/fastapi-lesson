## 命名约定
命名要语义化，使用用英文单词，不要缩写除非是众所周知的缩写 \
本规范使用:

1. 驼峰式命名(camelCase)：单个命名中，首个词是以小写字母开头，后面每个词都是以大写字母开始
2. 帕斯卡命名(PascalCase)：单个命名中，每个词都是以大写字母开始
3. 烤串命名(kebab-case)：单个命名中，每个单词都是小写的，之间用连字符 - 连接
4. 大蛇形命名(UPPER_SNAKE_CASE)：单个命名中，每个单词都是大写的，之间用下划线 \_ 连接
4. 小蛇形命名(lower_snak_case)：单个命名中，每个单词都是小写的，之间用下划线 \_ 连接

|         命名法         | 使用场景                                                      |
| :--------------------: | :------------------------------------------------------------ |
| 帕斯卡命名 PascalCase  | 类名、枚举名、类型名、对象、项目名           |
|  大蛇形命名 UPPER_SNAKE_CASE   | 常量、静态变更              |
|  小蛇形命名 lower_snak_case   | 普通变量、类变量、类属性、函数、函数参数、数据库字段、文件名              |
|  烤串命名 kebab-case   | 路由 path |
| 小驼峰式命名 camelCase |               |
| 名词复数形式           |  路由          | 

### 一些约定
每个python文件头部增加以下两行：
```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

```
局部变量：_lower_snak_case \
类内私有变量：__lower_snak_case \
系统变量：__lower_snak_case__ 应该放在模块文档之后， 其他模块导入之前 \
函数：lower_snak_case 动词+名词 get_user \
使用f-string进行字符串格式化
```python
message = f"Processing {param1} and {param2}"
print(message)

```
使用logging模块进行日志记录
```python
# 日志记录示例
logging.info("Processing value: %s", self.value)
```

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


# 启动项目
source .venv/Scripts/activate 
# 开发
fastapi dev
fastapi dev --host 0.0.0.0
# 生产
fastapi run
```

## 目录结构

## 组件管理：使用依赖注入
```python
from fastapi import Depends, FastAPI
from app.services.user_service import UserService

# openapi_url=None, docs_url=None, redoc_url=None 禁用接口文档
app = FastAPI()

# path_param 为路由参数
# 通过 Path 函数的 description 参数，可以给路由参数添加描述信息
# 通过 Query 函数的 description 参数，可以给URL参数添加描述信息
# 通过 Body 函数的 description 参数，可以给BODY参数添加描述信息
@app.get(
    "/{path_param}",
    tags=["接口分组标签"],
    summary="接口概述",
    description="接口详细描述",
    response_description="接口返回描述",
)
async def root(
    path_param: ParamEnum = Path(description="路由参数枚举"),
    query_param: QueryEnum = Query(default=None, description="URL参数枚举"),
):
    """返回根路由的响应消息

    Returns:
        dict: 包含 "message" 键的字典，值为 "Hello World"
    """
    return {
        "message": "Hello World",
        "path_param": path_param,
        "query_param": query_param,
    }

# 通过 get_user_service 函数创建组件实例
def get_user_service():
    return UserService()

# 使用 Depends 来注入该实例 get_user_service
@app.get("/users/{user_id}")
async def read_user(user_id: int, service: UserService = Depends(get_user_service)):
    return service.get_user_by_id(user_id)


# 启动服务的一种试，可以不要
# uvicorn main:app --host 0.0.0.0 --port 80
# if __name__ == "__main__":
#     使用 python main.py 启动服务
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)

```

## 修改接⼝⽂档的资源地址
修改 fastapi 源代码 `.venv/Lib/site-packages/fastapi/openapi/docs.py`
把 `swagger_js_url` 修改为 `"/static/swagger-ui-bundle.js"`
把 `swagger_css_url` 修改为 `"/static/swagger-ui.css"`
把 `swagger_favicon_url` 修改为 `"/static/favicon.png"`
在app中注册static⽬录
```python
# 把项目下的 static 日录作为访问路径
app.mount("/static", StaticFiles(directory="static"), name="static")
```

