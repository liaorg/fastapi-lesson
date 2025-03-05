#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    :   __init__.py
@Time    :   2025/03/04 11:13:20
@Desc    :   应用创建器
"""

import abc
import logging

from fastapi import FastAPI


class IApplicationBuilder:
    """创建应用抽象接口"""

    @classmethod
    @abc.abstractmethod
    def with_environment_settings(cls) -> "IApplicationBuilder":
        """根据环境变量选择指定的环境配置实例"""
        raise NotImplementedError

    @abc.abstractmethod
    def _instance_app(self) -> FastAPI:
        raise NotImplementedError

    @abc.abstractmethod
    def _register_loguru_log_client(self, app: FastAPI) -> None:
        """注册日志处理"""
        raise NotImplementedError

    @abc.abstractmethod
    def _register_global_request(self, app: FastAPI) -> None:
        """注册全局请求"""
        raise NotImplementedError

    @abc.abstractmethod
    def _register_exception_handlers(self, app: FastAPI) -> None:
        """注册错误处理"""
        raise NotImplementedError

    @abc.abstractmethod
    def _register_plugins(self, app: FastAPI) -> None:
        """注册插件"""
        raise NotImplementedError

    @abc.abstractmethod
    def _register_routes(self, app: FastAPI) -> None:
        """注册路由"""
        raise NotImplementedError

    @abc.abstractmethod
    def _register_middlewares(self, app: FastAPI) -> None:
        """注册中单件"""
        raise NotImplementedError

    def build(self) -> FastAPI:
        """创建实例"""
        try:
            # 约束注册流程-避免错误
            logging.critical("约束注册流程")
            # 创建实例对象
            app = self._instance_app()
            # 执行自定义的日志配置插件放在最后执行，以便获取到上下文的实例对象
            self._register_loguru_log_client(app)
            # 执行错误注册
            self._register_exception_handlers(app)
            # 执行插件的注册----优先于路由注册，避免部分的全局对象加载问题
            self._register_plugins(app)
            # 执行中间件的注册
            self._register_middlewares(app)
            # 注册全局请求，最外层进行注册
            self._register_global_request(app)
            # 注册路由
            self._register_routes(app)
            # 健康检查路由
            self._register_health_checks(app)
            return app
        except Exception as e:
            logging.critical(f"项目启动失败:{e}")
            raise e
