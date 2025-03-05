#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    :   config.py
@Time    :   2025/03/04 09:58:52
@Desc    :   配置实例入口
"""

import os
from collections.abc import MutableMapping
from typing import Any

from .base import ISettings
from .development import DevSettings
from .production import ProSettings


class DevSettingsBuilder:
    """创建开发环境的配置"""

    @classmethod
    def build(cls) -> ISettings:
        """创建配置实例对象"""
        return DevSettings()


class ProSettingsBuilder:
    """创建生产环境的配置"""

    @classmethod
    def build(cls) -> ISettings:
        """创建配置实例对象"""
        return ProSettings(environment="production")


class Environment:
    """该静态方法实现了从环境变量中读取设置，并将其转换为Settings类型，以便使用"""

    @staticmethod
    def select() -> DevSettings | ProSettings | ISettings:
        """
        定义静态方法select，它返回一个Settings类型的值；
        :return:
        """
        # 根据环境变量的来选择使用的配置
        env_vars: MutableMapping[Any, Any] = os.environ
        print(f"环境变量信息{env_vars.get('environment')}")
        # 根据不同环境变量返回不同的环境配置实例对象
        if env_vars.get("environment") == "development":
            settings_class = DevSettingsBuilder
        # 如果是正式环境则使用正式环境的配置
        elif env_vars.get("environment") == "production":
            settings_class = ProSettingsBuilder
        else:
            # 默认的是要开发环境的配置信息
            settings_class = DevSettingsBuilder
        # 创建配置实例对象
        settings = settings_class().build()
        return settings
