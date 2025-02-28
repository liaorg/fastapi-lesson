#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""这是一个使用 FastAPI 框架创建的简单 Web 应用程序

Returns:
    _type_: _description_
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 把项目下的 static 日录作为访问路径
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    """返回根路由的响应消息

    Returns:
        dict: 包含 "message" 键的字典，值为 "Hello World"
    """
    return {"message": "Hello World"}


# 可以不要
# if __name__ == "__main__":
# 使用 python main.py 启动服务
# uvicorn.run(server, host=appSettings.app_host, port=appSettings.app_port)
