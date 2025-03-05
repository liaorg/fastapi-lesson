#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    :   development.py
@Time    :   2025/03/04 09:57:28
@Desc    :   开发环境下的配置（基于base覆盖配置）
"""

from .base import ISettings


class DevSettings(ISettings):
    """应用基础的配置项信息"""

    environment: str = "development"
    debug: bool = True

    # ===========SqlalchemyPluginForClassV2Client插件参数配置==============
    MYSQL_SERVER_HOST: str = "xxxxxxxx"
    MYSQL_USER_NAME: str = "xxxxxx"
    MYSQL_PASSWORD: str = "xxxxxx"
    MYSQL_DB_NAME: str = "xxxxxx"
    # 数据库连接池
    SQLALCHEMY_DATABASE_ECHO: bool = False
    SQLALCHEMY_POOL_RECYCLE: int = 7200
    SQLALCHEMY_POOL_PRE_PING: bool = True
    SQLALCHEMY_POOL_SIZE: int = 20
    SQLALCHEMY_MAX_OVERFLOW: int = 64
