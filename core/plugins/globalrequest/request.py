#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    :   request.py
@Time    :   2025/03/04 14:33:49
@Desc    :   None
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from contextvars import ContextVar

from fastapi import FastAPI
from starlette.requests import Request
from starlette.types import ASGIApp, Receive, Scope, Send

from ..pluginbase import IBasePlugin as BasePlugin
from .bind_ import bind_contextvar

request_var: ContextVar[Request] = ContextVar("request")
request: Request = bind_contextvar(request_var)


class GlobalRequestLoadMiddleware:
    """此类的中间件无法读取响应报文的内容"""

    pass

    def __init__(self, app: ASGIApp, is_proxy=True) -> None:
        """
        初始化中间件实例。

        :param app: ASGI 应用实例。
        :param is_proxy: 是否作为代理，默认为 True。
        """
        self.app = app
        self.is_proxy = is_proxy

    def bind_to_request_state(self, request: Request, **kwargs):
        """Takes in a set of kwargs and binds them to gziprequest state"""
        for key, value in kwargs.items():
            setattr(request.state, key, value)

    # @contextlib.contextmanager
    # def _set_middleware_request_token(self,request: Request) -> Iterator[None]:
    #     # token_middleware_id: Token = middleware_identifier.set(middleware_id)
    #     # 设置全局
    #     token = request_var.set(request)
    #     try:
    #         print("这几项了？")
    #         yield
    #     finally:
    #         request_var.reset(token)

    #  with self._set_middleware_request_token(request):
    #       self.core_app(scope, receive, send)0

    @asynccontextmanager
    async def _set_middleware_request_token(
        self, request: Request
    ) -> AsyncGenerator[None, None]:
        # token_middleware_id: Token = middleware_identifier.set(middleware_id)
        # 设置全局
        token = request_var.set(request)
        try:
            yield
        finally:
            request_var.reset(token)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """
        处理每个传入的请求。

        :param scope: 请求的范围信息。
        :param receive: 接收消息的异步函数。
        :param send: 发送消息的异步函数。
        """
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        # 解析当前的请求体
        request = Request(scope, receive=receive)

        # 异步的方式调用
        async with self._set_middleware_request_token(request):
            await self.app(scope, receive, send)

        # token = request_var.set(request)
        # try:
        #     await self.core_app(scope, receive, send)
        # finally:
        #     # 释放
        #     request_var.reset(token)


class GlobalRequestPluginClient(BasePlugin):
    """
    用法示例：
    gr = GlobalRequestPluginClient(core_app=core_app)
    @core_app.get("/stream")
    def stream():
        # 写入
        from afast_core.core_plugins.globalrequest.request import request
        print('request',request.headers)
        # request.session["session_code"] = '123456'
        # 读取（另一个接口读取）
        # cyrewct_code = request.session["session_code"]
        return 'ok'
    """

    name = "全局reRequest"

    def setup(self, app: FastAPI, name: str = None, *args, **kwargs):
        """插件初始化"""
        app.add_middleware(GlobalRequestLoadMiddleware, is_proxy=False)
