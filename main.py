#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""这是一个使用 FastAPI 框架创建的简单 Web 应用程序

Returns:
_type_: _description_
"""

# from enum import Enum

# from fastapi import FastAPI, Path, Query
# from fastapi.staticfiles import StaticFiles

# # openapi_url=None, docs_url=None, redoc_url=None 禁用接口文档
# app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)

# # 把项目下的 static 日录作为访问路径
# app.mount("/static", StaticFiles(directory="static"), name="static")


# class ParamEnum(Enum):
#     """参数枚举类"""

#     param1 = "param1"
#     param2 = "param2"


# class QueryEnum(Enum):
#     """URL参数枚举类"""

#     query1 = "query1"
#     query2 = "query2"


# # path_param 为路由参数
# # 通过 Path 函数的 description 参数，可以给路由参数添加描述信息
# # 通过 Query 函数的 description 参数，可以给URL参数添加描述信息
# # 通过 Body 函数的 description 参数，可以给BODY参数添加描述信息
# @app.get(
#     "/{path_param}",
#     tags=["接口分组标签"],
#     summary="接口概述",
#     description="接口详细描述",
#     response_description="接口返回描述",
# )
# async def root(
#     path_param: ParamEnum = Path(description="路由参数枚举"),
#     query_param: QueryEnum = Query(default=None, description="URL参数枚举"),
# ):
#     """返回根路由的响应消息

#     Returns:
#         dict: 包含 "message" 键的字典，值为 "Hello World"
#     """
#     return {
#         "message": "Hello World",
#         "path_param": path_param,
#         "query_param": query_param,
#     }

# 必须在外部载入app对象
from app.application import app  # noqa: F401, I001

# if __name__ == "__main__":
#     # 使用os.path.basename函数获取了当前文件的名称，并将.py文件扩展名替换为空字符串\
#     # import os
#     # app_modeel_name = os.path.basename(__file__).replace(".py", "")
#     import inspect
#     from pathlib import Path

#     # 使用Path函数获取了当前文件的名称，并将.py文件扩展名替换为空字符串\
#     # app_modeel_name = Path(__file__).name.replace(".py", "")
#     import uvicorn

#     # 根据文件路径返回模块名
#     # print("app_modeel_name：",inspect.getmodulename(Path(__file__).name))
#     # 使用uvicorn.run函数运行了一个应用程序。它指定了应用程序的主机和端口，并且设置了reload参数为True。
#     print("路径", inspect.getmodulename(Path(__file__).name))
#     uvicorn.run(
#         f"{inspect.getmodulename(Path(__file__).name)}:app",
#         host="127.0.0.1",
#         port=32671,
#         workers=2,
#     )
