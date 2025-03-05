#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    :   request_response.py
@Time    :   2025/03/04 14:19:33
@Desc    :   None
"""

from fastapi.requests import Request
from fastapi.responses import Response

from .base import BaseResponseMiddleware


class RequestResponseMiddleware(BaseResponseMiddleware):
    """
    # from afast_core.core_middleware.request_response import RequestResponseMiddleware
    # core_app.add_middleware(RequestResponseMiddleware)
    """

    pass

    async def before_request(self, request: Request) -> Response | None:
        """如果需要修改请求信息，可直接重写此方法"""
        # print("你是谁？")
        await self.get_body()
        return self.app

    async def after_request(
        self, request: Request, res: Response = None
    ) -> Response | None:
        """请求后的处理【记录请求耗时等，注意这里没办法对响应结果进行处理】"""
        pass
