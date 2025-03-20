#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    :   client.py
@Time    :   2025/03/04 12:53:39
@Desc    :   Loguru Plugin Client for FastAPI
"""

from datetime import datetime
from urllib.parse import parse_qs

from fastapi import FastAPI
from pydantic_settings import BaseSettings as Settings
from starlette.requests import Request
from user_agents import parse

from core.libs.logger.v1 import init_logging

from ..pluginbase import IBasePlugin as BasePlugin
from .enums import RecordModel
from .middleware import LoguruPluginClientMiddleware


class LoguruPluginClient(BasePlugin):
    """
    注意事项：
    因为是日志作用，所以一般使用的时候最后再执行注册
    ------------------
    用法示例：
    log = LoguruPluginClient(core_app=core_app,settings=LoguruPluginClient.LoguruConfig(
     MODEL = RecordModel.CENTRALIZED
    ))
    from core.plugins.loguru import logger
    @core_app.get("/stream12")
    def stream():
        # 写入
        # print("dddddddddf",logrequest.state.background)
        # infirmary_tasks = BackgroundTask(logger.info, 'aaaaa22222222222222---1')
        # logrequest.state.background = infirmary_tasks
        # infirmary_tasks.add_task(logger.info,'aaaaa22222222222222---1')
        # log.bind(ip=get_client_ip(request)).info('aaaaa')
        logger.info('日志记录信息')
        # 读取（另一个接口读取）
        # cyrewct_code = request.session["session_code"]
        return {
            "dasd":2323
        }
    """

    name = "日志记录插件"

    # 再静态的里面使用self来查询也可以，遵循从内到外的查询

    def filter_request_url(self, request: Request):
        """过滤不需要记录日志请求地址URL"""
        path_info = request.url.path
        if request.method == "OPTIONS":
            return True
        if "websocket" in path_info:
            return True
        return path_info in self.settings.FLITER_REQUEST_URL

    class LoguruConfig(Settings):
        """默认配置"""

        # =========================记录模式
        MODEL: RecordModel = RecordModel.CENTRALIZED

        # =========================
        # 配置日志相关信息
        PROJECT_SLUG: str = "info"
        # 日志文件的目录,当前插件初始化位置所在的目录
        LOG_FILE_PATH: str = "."
        # 日志文件切割的日期- rotation='00:00',  # 每天 0 点创建一个新日志文件
        LOG_FILE_ROTATION: str = "00:00"
        # 日志文件的保留的天数  #  retention="7 days",  # 定时自动清理文件
        LOG_FILE_RETENTION: int | str = 8
        # 日志压缩的格式
        LOG_FILE_COMPRESSION: str = "gz"
        # 日志记录的等等级
        LOG_FILE_LEVEL: str = "INFO"
        # =========================
        # 日志记录相关配置-
        NESS_ACCESS_HEADS_KEYS: list = []
        # 是否记录响应报文内容，如果包含内容过多，不建议记录
        IS_RECORD_RESPONSE: bool = True
        # 是否记录用户提交请求头信息
        IS_RECORD_HEADERS: bool = True
        # 是否记录用户UA信息
        IS_RECORD_UA: bool = False
        # 需要过来的请求URL路径信息
        FLITER_REQUEST_URL: list = [
            "/",
            "/favicon.ico",
            "/favicon.png",
            "/docs",
            "/openapi.json",
            "/static/swagger-ui.css",
            "/static/swagger-ui-bundle.js",
            "/static/redoc.standalone.js",
        ]

    async def make_request_log_msg(self, request: Request):
        """格式化日志"""
        log_msg = None
        if self.filter_request_url(request):
            request.state.close_record = True
        else:
            _ip, method, url = request.client.host, request.method, request.url.path
            # 解析请求提交的表单信息
            try:
                body_form = await request.form()
            except Exception:
                body_form = None

            # 解析请求提交的body信息
            body = None
            try:
                pass
                body_bytes = await request.body()
                if body_bytes:
                    try:
                        body = await request.json()
                    except Exception:
                        pass
                        if body_bytes:
                            try:
                                body = body_bytes.decode("utf-8")
                            except Exception:
                                body = body_bytes.decode("gb2312")
            except Exception as e:
                raise e
            # 在这里记录下当前提交的body的数据，用于下文的提取
            request.state.body = body
            # 从头部里面获取出对应的请求头信息，用户用户机型等信息获取
            try:
                user_agent = parse(request.headers["user-agent"])
                browser = user_agent.browser.version
                if len(browser) >= 2:
                    _browser_major, _browser_minor = browser[0], browser[1]
                else:
                    _browser_major, _browser_minor = 0, 0
                # 用户当前系统OS信息提取
                user_os = user_agent.os.version
                if len(user_os) >= 2:
                    _os_major, _os_minor = user_os[0], user_os[1]
                else:
                    _os_major, _os_minor = 0, 0

                log_msg = {
                    # 'headers': str(gziprequest.headers),
                    # 'user_agent': str(gziprequest.user_agent),
                    # 记录请求头信息----如果需要特殊的获取某些请求的记录则做相关的配置即可
                    "headers": None
                    if not self.settings.IS_RECORD_HEADERS
                    else [
                        request.headers.get(i, "")
                        for i in self.settings.NESS_ACCESS_HEADS_KEYS
                    ]
                    if self.settings.NESS_ACCESS_HEADS_KEYS
                    else None,
                    # 记录请求URL信息
                    "useragent": None
                    if not self.settings.IS_RECORD_UA
                    else {
                        "os": f"{user_agent.os.family} {user_agent.os.version_string}",
                        "browser": f"{user_agent.browser.family} {user_agent.browser.version_string}",
                        "device": {
                            "family": user_agent.device.family,
                            "brand": user_agent.device.brand,
                            "model": user_agent.device.model,
                        },
                    },
                    "url": url,
                    # 记录请求方法
                    "method": method,
                    # 记录请求来源IP
                    # 'ip': ip,
                    # 'path': gziprequest.path,
                    # 记录请求提交的参数信息
                    "params": {
                        "query_params": parse_qs(str(request.query_params)),
                        "from": body_form,
                        "body": body,
                    },
                    # 记录请求的开始时间
                    "ts": f"{datetime.now():%Y-%m-%d %H:%M:%S%z}",
                    # 'start_time':  f'{(start_time)}',
                }
            except Exception as e:
                log_msg = {
                    # 'headers': str(gziprequest.headers),
                    # 'user_agent': str(gziprequest.user_agent),
                    # 记录请求头信息----如果需要特殊的获取某些请求的记录则做相关的配置即可
                    "headers": None
                    if not self.settings.IS_RECORD_HEADERS
                    else [
                        request.headers.get(i, "")
                        for i in self.settings.NESS_ACCESS_HEADS_KEYS
                    ]
                    if self.settings.NESS_ACCESS_HEADS_KEYS
                    else None,
                    "url": url,
                    # 记录请求方法
                    "method": method,
                    # 记录请求来源IP
                    # 'ip': ip,
                    # 'path': gziprequest.path,
                    # 记录请求提交的参数信息
                    "params": {
                        "query_params": parse_qs(str(request.query_params)),
                        "from": body_form,
                        "body": body,
                    },
                    # 记录请求的开始时间
                    "ts": f"{datetime.now():%Y-%m-%d %H:%M:%S%z}",
                    # 'start_time':  f'{(start_time)}',
                }
                raise e

            # 对于没有的数据清除
            if not log_msg["headers"]:
                log_msg.pop("headers")
            if not log_msg["params"]["query_params"]:
                log_msg["params"].pop("query_params")
            if not log_msg["params"]["from"]:
                log_msg["params"].pop("from")
            if not log_msg["params"]["body"]:
                log_msg["params"].pop("body")
        return log_msg

    def setup(self, app: FastAPI, name: str = None, settings=None, *args, **kwargs):
        """插件初始化"""
        # init_logging_ex = init_logging(app_config)
        # def init_logging_ex():
        # return init_logging(settings)

        # 开始初始化
        # core_app.add_event_handler("startup", init_logging_ex)
        init_logging(settings)
        app.add_middleware(LoguruPluginClientMiddleware, is_proxy=True, client=self)
