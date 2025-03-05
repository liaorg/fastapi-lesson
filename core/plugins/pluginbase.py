#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    :   pluginbase.py
@Time    :   2025/03/04 12:58:15
@Desc    :   None
"""

import abc

from fastapi import FastAPI


class PluginException(Exception):
    """查询异常的定义"""


class IBasePlugin(metaclass=abc.ABCMeta):
    """插件基础定义"""

    # 插件名称
    name: str
    describe: str  # 描述
    # 依赖FastAPI主应用对象
    app: FastAPI | None = None

    def __init__(self, app: FastAPI = None, name=None, settings=None, **options):
        """创建应用的插件"""
        if getattr(self, "name", None) is None:
            # raise TypeError("Plugin.name is required")
            raise PluginException("Plugin.name is required")
        # 安装插件
        if app is not None:
            self.name = name or self.name
            self.app = app
            self.settings = settings
            self.setup(app, name, settings, **options)
        else:
            pass

    def __repr__(self) -> str:
        """输出插件信息"""
        return f"<FastAPI.Exts.Plugin: {self.name}>"

    @property
    def installed(self):
        """检测插件是否已安装"""
        return bool(self.app)

    @abc.abstractmethod
    def setup(self, app: FastAPI, name: str = None, settings=None, **options):
        """插件初始化"""
        # 插件对象保存
        # self.core_app.state.core_plugins={}
        # self.core_app.state.core_plugins[self.name] = self
