#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    :   contextvar.py
@Time    :   2025/03/04 12:41:36
@Desc    :   None
"""

from contextvars import ContextVar

from starlette.requests import Request

from .bind_ import bind_contextvar

# 如果 context_var 在 get 之前没有先 set，那么会抛出一个 LookupError
# 可以通过设置 contextvar.ContextVar 默认值：
log_request_var: ContextVar[Request] = ContextVar("logrequest")
logrequest: Request = bind_contextvar(log_request_var)
