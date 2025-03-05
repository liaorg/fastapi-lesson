#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    :   base.py
@Time    :   2025/03/04 09:53:45
@Desc    :   具体环境配置通用的配置
"""

from pydantic_settings import BaseSettings

from core.plugins.loguru.enums import RecordModel


class ISettings(BaseSettings):
    """应用基础的配置项信息"""

    project_name: str = "FastApi后台api示例"
    project_version: str = "1.0.0"
    environment: str = "production"
    debug: bool = False

    # ===========日志插件参数配置==============
    # 日志插件参数配置
    LOG_MODEL: RecordModel = RecordModel.SCATTERED
    # 配置日志相关信息
    LOG_PROJECT_SLUG: str = "info"
    # 日志文件的目录,当前插件初始化位置所在的目录
    LOG_FILE_PATH: str = "./logs"
    # 日志文件切割的日期- rotation='00:00',  # 每天 0 点创建一个新日志文件
    LOG_FILE_ROTATION: str = "00:00"
    # 日志文件的保留的天数  #  retention="7 days",  # 定时自动清理文件
    LOG_FILE_RETENTION: int | str = 8
    # 日志压缩的搁置
    LOG_FILE_COMPRESSION: str = "gz"
    # 日志记录的等等级
    LOG_FILE_LEVEL: str = "INFO"
    # 日志需要过滤的不做记录的URL请求
    FLITER_REQUEST_URL: list[str] = [
        "/favicon.ico",
        "/favicon.png",
        # "/docs",
        # "/",
        # "/openapi.json",
        # "/health_checks",
        # "/static/swagger-ui.css",
        # "/static/swagger-ui-bundle.js",
    ]

    # ===========SwaggeruiPluginClient插件参数配置==============
    swaggerui_proxy: bool = False

    # ===========SessionPluginClient插件参数配置==============
    # session_store: CookieStore | AsyncRedisStore | InMemoryStore = CookieStore(
    #     secret_key="kTd5NsCsaj52TzHb"
    # )
    # 只是只允许https读取
    session_cookie_https_only: bool = False
    # 会话生存时间
    session_lifetime: int = 3600 * 24 * 14
    # 是否自动加载
    session_is_auto_load: bool = True
    # 是否滚地会话时效续期
    session_is_rolling: bool = False

    # ===========SqlalchemyPluginForClassV2Client插件参数配置==============
    # MYSQL_SERVER_HOST: str
    # MYSQL_USER_NAME: str
    # MYSQL_PASSWORD: str
    # MYSQL_DB_NAME: str
    # # 数据库连接池
    # SQLALCHEMY_DATABASE_ECHO: bool
    # SQLALCHEMY_POOL_RECYCLE: int
    # SQLALCHEMY_POOL_PRE_PING: bool
    # SQLALCHEMY_POOL_SIZE: int
    # SQLALCHEMY_MAX_OVERFLOW: int
