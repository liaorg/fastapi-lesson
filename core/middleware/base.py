#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    :   base.py
@Time    :   2025/03/04 14:18:10
@Desc    :   基础中间件类定义
"""

import functools
import http
import json
import typing

from fastapi.datastructures import Headers
from fastapi.requests import Request
from fastapi.responses import Response
from pydantic import BaseModel, Field
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    DispatchFunction,
    RequestResponseEndpoint,
)
from starlette.types import ASGIApp, Message, Receive, Scope, Send


class BaseMiddlewareNoResponse:
    """
    基础中间件类，不处理响应。
    如果需要在内部读取请求体内容，需要在所有中间件的最后注册，并开启 `is_proxy=True`。
    """

    def __init__(self, app: ASGIApp, is_proxy: bool = True) -> None:
        """
        初始化中间件。

        Args:
            app (ASGIApp): ASGI 应用实例。
            is_proxy (bool): 是否开启代理模式，默认为 `True`。
        """
        self.app = app
        self.is_proxy = is_proxy
        self.request: Request | None = None

    def bind_to_request_state(self, request: Request, **kwargs):
        """
        将关键字参数绑定到请求的状态中。

        Args:
            request (Request): 请求对象。
            **kwargs: 需要绑定的关键字参数。
        """
        for key, value in kwargs.items():
            setattr(request.state, key, value)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """
        处理请求和响应。

        Args:
            scope (Scope): ASGI 作用域。
            receive (Receive): 接收消息的函数。
            send (Send): 发送消息的函数。
        """
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        # 解决读取BODY问题
        if self.is_proxy:
            receive_ = await receive()

            async def receive():
                return receive_

        # 解析当前的请求体
        self.request = Request(scope, receive=receive)
        # 自动传参，如果对于send有需要重写的需求，则需要进行重写
        send = functools.partial(self.send, send=send, request=self.request)
        # 自定义回调函数，可以自己进行重写实现具体的业务逻辑
        response = await self.before_request(self.request) or self.app
        await response(self.request.scope, receive, send)
        await self.after_request(self.request)

    async def send(self, message: Message, send: Send, request: Request) -> None:
        """
        重写send方法【不重写则默认使用原来的】。

        Args:
            message (Message): 消息对象。
            send (Send): 发送消息的函数。
            request (Request): 请求对象。
        """
        return await send(message)

    async def before_request(self, request: Request) -> Response | None:
        """
        如果需要修改请求信息，可直接重写此方法。

        Args:
            request (Request): 请求对象。

        Returns:
            Response | None: 响应对象或 `None`。
        """
        return self.app

    async def after_request(self, request: Request) -> Response | None:
        """
        请求后的处理【记录请求耗时等，注意这里没办法对响应结果进行处理】。

        Args:
            request (Request): 请求对象。

        Returns:
            Response | None: 响应对象或 `None`。
        """
        return None

    async def get_body(self):
        """
        获取请求BODY，实现使用代理方式解析读，解决在中间件中读取Body的问题。

        Returns:
            bytes: 请求体内容。
        """
        body = await self.request.body()
        return body

    async def get_json(self):
        """
        获取json请求参数。

        Returns:
            dict: JSON 请求参数。
        """
        return json.loads(await self.get_body())


class BaseMiddlewareHasResponse:
    """
    基础中间件类，可以继续读取返回的响应报文。
    使用方法：
    core_app.add_middleware(BaseMiddlewareHasResponse)
    """

    def __init__(self, app: ASGIApp) -> None:
        """
        初始化中间件。

        Args:
            app (ASGIApp): ASGI 应用实例。
        """
        self.app = app
        self.request: Request | None = None

    async def before_request(self, request: Request) -> Response | None:
        """
        如果需要修改请求信息，可直接重写此方法。

        Args:
            request (Request): 请求对象。

        Returns:
            Response | None: 响应对象或 `None`。
        """
        pass

    async def after_request(
        self, request: Request, res: Response = None
    ) -> Response | None:
        """
        请求后的处理【记录请求耗时等，注意这里没办法对响应结果进行处理】。

        Args:
            request (Request): 请求对象。
            res (Response, optional): 响应对象。默认为 `None`。

        Returns:
            Response | None: 响应对象或 `None`。
        """
        return res

    async def get_body(self):
        """
        获取请求BODY，实现使用代理方式解析读，解决在中间件中读取Body的问题。

        Returns:
            bytes: 请求体内容。
        """
        body = await self.request.body()
        return body

    async def get_json(self):
        """
        获取json请求参数。

        Returns:
            dict: JSON 请求参数。
        """
        return json.loads(await self.get_body())

    async def __call__(
        self, request: Request, call_next: RequestResponseEndpoint, *args, **kwargs
    ) -> Response:
        """
        处理请求和响应。

        Args:
            request (Request): 请求对象。
            call_next (RequestResponseEndpoint): 处理下一个请求的函数。
            *args: 位置参数。
            **kwargs: 关键字参数。

        Returns:
            Response: 响应对象。
        """
        try:
            # 解析当前的请求体
            self.request = request
            await self.before_request(self.request) or self.app
            response = await call_next(request)
        except Exception:
            # 解析响应报文的body异常信息
            response_body = bytes(http.HTTPStatus.INTERNAL_SERVER_ERROR.phrase.encode())
            # 生成异常报文内容
            response = Response(
                content=response_body,
                status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR.real,
            )
        else:
            response_body = b""
            # 解析读取对应的响应报文内容
            async for chunk in response.body_iterator:
                response_body += chunk
            # 响应体最终响应报文内容
            response = Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )
            await self.after_request(self.request, response)
        return response


class BaseHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware to dispatch modified response."""

    def __init__(
        self,
        app: ASGIApp,
        dispatch: DispatchFunction = None,
        handler: typing.Callable = None,
    ) -> None:
        """
        初始化中间件。

        Args:
            app (ASGIApp): ASGI 应用实例。
            dispatch (DispatchFunction, optional): 分发函数。默认为 `None`。
            handler (typing.Callable, optional): 处理函数。默认为 `None`。
        """
        super().__init__(app, dispatch=dispatch)
        self.handler = handler

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """
        处理请求和响应。

        Args:
            request (Request): 请求对象。
            call_next (RequestResponseEndpoint): 处理下一个请求的函数。

        Returns:
            Response: 响应对象。
        """
        request.state.background = None
        response = await call_next(request)
        # 执行响应报文中的后台任务
        if request.state.background:
            response.background = request.state.background
        return response


class ResponseInfo(BaseModel):
    """响应信息模型。"""

    headers: Headers | None = Field(default=None, title="Response header")
    body: str = Field(default="", title="Response body")
    status_code: int | None = Field(default=None, title="Status code")

    class Config:
        """Pydantic 模型配置类，允许使用任意类型。"""

        arbitrary_types_allowed = True


class BaseResponseMiddleware:
    """
    基础响应中间件类，可以继续读取返回的响应报文。
    如果需要在内部读取请求体内容，需要在所有中间件的最后注册，并开启 `is_proxy=True`。
    """

    def __init__(self, app: ASGIApp, is_proxy: bool = True) -> None:
        """
        初始化中间件。

        Args:
            app (ASGIApp): ASGI 应用实例。
            is_proxy (bool): 是否开启代理模式，默认为 `True`。
        """
        self.app = app
        self.is_proxy = is_proxy
        self.request: Request | None = None

    async def get_body(self):
        """
        获取请求BODY，实现使用代理方式解析读，解决在中间件中读取Body的问题。

        Returns:
            bytes: 请求体内容。
        """
        body = await self.request.body()
        return body

    async def get_json(self):
        """
        获取json请求参数。

        Returns:
            dict: JSON 请求参数。
        """
        body = await self.get_body()
        return json.loads(body) if body else None

    async def before_request(self, request: Request) -> Response | None:
        """
        如果需要修改请求信息，可直接重写此方法。

        Args:
            request (Request): 请求对象。

        Returns:
            Response | None: 响应对象或 `None`。
        """
        pass

    async def after_request(
        self, request: Request, res: Response = None
    ) -> Response | None:
        """
        请求后的处理【记录请求耗时等，注意这里没办法对响应结果进行处理】。

        Args:
            request (Request): 请求对象。
            res (Response, optional): 响应对象。默认为 `None`。

        Returns:
            Response | None: 响应对象或 `None`。
        """
        pass

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """
        处理请求和响应。

        Args:
            scope (Scope): ASGI 作用域。
            receive (Receive): 接收消息的函数。
            send (Send): 发送消息的函数。
        """
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        # 解决读取BODY问题
        if self.is_proxy:
            receive_ = await receive()

            async def receive():
                return receive_

        # 解析当前的请求体
        self.request = Request(scope, receive=receive)
        # 解析报文体内容
        response_info = ResponseInfo()
        # 自定义回调函数，可以自己进行重写实现具体的业务逻辑
        await self.before_request(self.request) or self.app

        async def _next_send(message: Message) -> None:
            if message.get("type") == "http.response.start":
                response_info.headers = Headers(raw=message.get("headers"))
                response_info.status_code = message.get("status")
            # 解析响应体内容信息
            elif message.get("type") == "http.response.body":
                if body := message.get("body"):
                    response_info.body += body.decode("utf-8", errors="ignore")
                response = Response(
                    content=response_info.body,
                    status_code=response_info.status_code,
                    headers=dict(response_info.headers),
                )
                await self.after_request(self.request, response)
            await send(message)

        await self.app(scope, receive, _next_send)
