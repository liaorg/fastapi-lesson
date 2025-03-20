#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    :   controller.py
@Time    :   2025/03/20 09:25:57
@Desc    :   None
"""

from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.modules.user.service import UserService

# 建立路由
router = InferringRouter(prefix="/users", tags=["用户管理"])


@cbv(router)
class UserController:
    """用户控制器"""

    service: UserService = Depends(UserService)

    @router.get("/list", summary="用户列表")
    def list(self):
        return "self.service.list()"

    @router.post("/login", summary="登入系统")
    def login(self):
        return self.service.login()

    @router.post("/register", summary="用户注册")
    def register(self):
        return self.service.register()
