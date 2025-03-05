#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    :   middleware.py
@Time    :   2025/03/04 12:53:52
@Desc    :   Loguru Middleware for FastAPI
"""

import json
from contextvars import ContextVar
from time import perf_counter
from uuid import uuid4

from pydantic import BaseModel, Field
from starlette.datastructures import Headers
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from . import logger
from .contextvar import log_request_var, logrequest
from .enums import RecordModel


class ResponseInfo(BaseModel):
    """用于存储响应信息的数据模型，包括响应头、响应体和状态码。"""

    headers: Headers | None = Field(default=None, title="Response header")
    body: str = Field(default="", title="Response body")
    status_code: int | None = Field(default=None, title="Status code")

    class Config:
        """Pydantic 模型配置类，允许使用任意类型。"""

        arbitrary_types_allowed = True


# 存储日志内容的上下文信息
log_msg_var: ContextVar[dict] = ContextVar("log_msg_var", default=None)


class LoguruPluginClientMiddleware:
    """
    FastAPI 中间件，用于集成 Loguru 日志库。
    该中间件负责在请求前后记录日志，并处理响应内容的记录。
    """

    def __init__(self, *, app: ASGIApp, is_proxy: bool = True, client) -> None:
        """
        初始化中间件。

        Args:
            app (ASGIApp): ASGI 应用实例。
            is_proxy (bool): 是否使用代理方式解析请求体。
            client: 客户端对象。
        """
        self.app = app
        self.is_proxy = is_proxy
        self.client = client
        self.request: Request | None = None

    async def get_body(self) -> bytes:
        """
        获取请求体内容。

        Returns:
            bytes: 请求体内容。
        """
        body = await self.request.body()
        return body

    async def get_json(self) -> dict:
        """
        获取 JSON 请求参数。

        Returns:
            dict: JSON 请求参数。
        """
        return json.loads(await self.get_body())

    async def before_request(self, request: Request) -> None:
        """
        请求前的处理，设置追踪 ID 和开始时间。

        Args:
            request (Request): 请求对象。
        """
        request.state.traceid = str(uuid4())
        request.state.start_time = perf_counter()

    async def after_request(self, request: Request, token, response: Response) -> None:
        """
        请求后的处理，记录响应内容。

        Args:
            request (Request): 请求对象。
            token: 上下文变量的令牌。
            response (Response): 响应对象。
        """
        log_msg = log_msg_var.get()
        if log_msg is None:
            log_msg = {}
            log_msg_var.set(log_msg)

        if (
            self.client.settings.IS_RECORD_RESPONSE
            and log_msg
            and response.status_code != 404
        ):
            logger.info(response.body.decode("utf-8"), event_name="response")

        try:
            request.state.traceid = None
            log_request_var.reset(token)
        except Exception as e:
            logger.error(f"Error resetting context var: {e}")

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """
        中间件的主要调用方法。

        Args:
            scope (Scope): ASGI 作用域。
            receive (Receive): 接收消息的回调函数。
            send (Send): 发送消息的回调函数。
        """
        if scope["type"] not in ["http", "websocket"]:
            return await self.app(scope, receive, send)

        if self.is_proxy:
            receive_ = await receive()

            async def receive():
                return receive_

        self.request = Request(scope, receive=receive)
        if self.client.filter_request_url(request=self.request):
            return await self.app(scope, receive, send)

        response_info = ResponseInfo()

        await self.before_request(self.request)
        token = log_request_var.set(self.request)

        if self.client.settings.MODEL == RecordModel.SCATTERED:
            logrequest.state.record_model = RecordModel.SCATTERED
            log_msg = await self.client.make_request_log_msg(self.request)
            log_msg_var.set(log_msg or {})
            if log_msg:
                logger.info(log_msg, event_name="request")
        else:
            logrequest.state.record_model = RecordModel.CENTRALIZED
            log_msg = await self.client.make_request_log_msg(self.request)
            log_msg_var.set(log_msg or {})
            logger.info(log_msg, event_name="request")

        async def _next_send(message: Message) -> None:
            """
            处理响应消息。

            Args:
                message (Message): 响应消息。
            """
            if message["type"] == "http.response.start":
                response_info.headers = Headers(raw=message["headers"])
                response_info.status_code = message["status"]
            elif message["type"] == "http.response.body":
                if body := message.get("body"):
                    response_info.body += body.decode("utf-8")
                response = Response(
                    content=response_info.body,
                    status_code=response_info.status_code,
                    headers=dict(response_info.headers),
                )
                await self.after_request(
                    request=self.request, token=token, response=response
                )

            await send(message)

        try:
            await self.app(scope, receive, _next_send)
        finally:
            pass
