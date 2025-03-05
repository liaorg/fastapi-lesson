#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    :   bind_.py
@Time    :   2025/03/04 12:43:01
@Desc    :   None
"""


def bind_contextvar(contextvar):
    """绑定上下文"""

    class ContextVarBind:
        __slots__ = ()

        def __getattr__(self, name):
            return getattr(contextvar.get(), name)

        def __setattr__(self, name, value):
            setattr(contextvar.get(), name, value)

        def __delattr__(self, name):
            delattr(contextvar.get(), name)

        def __getitem__(self, index):
            return contextvar.get()[index]

        def __setitem__(self, index, value):
            contextvar.get()[index] = value

        def __delitem__(self, index):
            del contextvar.get()[index]

    return ContextVarBind()


def bind_contextvar_fun(FUN):
    """绑定上下文函数"""
    return FUN()
