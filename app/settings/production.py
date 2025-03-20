#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    :   production.py
@Time    :   2025/03/04 09:57:55
@Desc    :   生产环境下的配置（基于base覆盖配置）
"""

from .base import ISettings


class ProSettings(ISettings):
    """应用基础的配置项信息"""

    environment: str = "production"
    debug: bool = False

    # ===========日志插件参数配置==============
    # 日志插件参数配置
    # 日志记录的等等级
    LOG_FILE_LEVEL: str = "WARNING"

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
