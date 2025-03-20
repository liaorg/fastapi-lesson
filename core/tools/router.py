#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    :   router.py
@Time    :   2025/03/19 17:41:55
@Desc    :
"""

import importlib
from pathlib import Path

from fastapi import APIRouter
from fastapi.routing import APIRoute

from core.plugins.loguru import logger


def load_controller_modules(app_router: APIRouter, module_dir: str):
    """
    加载指定目录下的所有模块，并自动注册路由
    :param app_router: APIRouter 应用实例
    :param module_dir: 模块目录相对路径
    """
    path = Path(module_dir)
    for module_file in path.glob("**/controller.py"):  # 只加载包含 controller.py 的模块
        module_name = module_file.parent.name
        module_path = f"{module_dir.replace('/', '.')}.{module_name}.controller"

        try:
            module = importlib.import_module(module_path)
            # 自动注册路由
            if hasattr(module, "router"):
                app_router.include_router(module.router)
                for r in module.router.routes:
                    if isinstance(r, APIRoute):
                        methods = ", ".join(r.methods)
                        logger.info(f"[{r.endpoint.__module__}] {methods} {r.path}")

        except ImportError as e:
            logger.info(f"Import module routing failed {module_path}: {e}")
