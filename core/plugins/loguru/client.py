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
from pydantic_settings import BaseSettings
from starlette.requests import Request
from user_agents import parse

from core.libs.logger.v1 import init_logging

from ..pluginbase import IBasePlugin
from .enums import RecordModel
from .middleware import LoguruPluginClientMiddleware


class LoguruPluginClient(IBasePlugin):
    """
    Loguru Plugin Client for FastAPI

    This plugin integrates Loguru logging into a FastAPI application.
    It provides middleware to log request and response details.

    Usage Example:
    log = LoguruPluginClient(core_app=core_app, settings=LoguruPluginClient.LoguruConfig(
        MODEL=RecordModel.CENTRALIZED
    ))
    from afast_core.core_plugins.log import logger

    @core_app.get("/stream12")
    def stream():
        logger.info('日志记录信息')
        return {
            "dasd": 2323
        }
    """

    name = "日志记录插件"

    def __init__(self, core_app: FastAPI, settings: BaseSettings):
        """
        Initialize the LoguruPluginClient.

        Args:
            core_app (FastAPI): The FastAPI application instance.
            settings (Settings): Configuration settings for the plugin.
        """
        self.core_app = core_app
        self.settings = settings

    def filter_request_url(self, request: Request) -> bool:
        """
        Filter request URLs that should not be logged.

        Args:
            request (Request): The request object.

        Returns:
            bool: True if the request URL should be filtered, False otherwise.
        """
        path_info = request.url.path
        if request.method == "OPTIONS":
            return True
        if "websocket" in path_info:
            return True
        return path_info in self.settings.FLITER_REQUEST_URL

    class LoguruConfig(BaseSettings):
        """
        Configuration settings for the Loguru Plugin.

        Attributes:
            MODEL (RecordModel): The logging model (CENTRALIZED or SCATTERED).
            PROJECT_SLUG (str): The project slug for logging.
            LOG_FILE_PATH (str): The directory for log files.
            LOG_FILE_ROTATION (str): The rotation schedule for log files.
            LOG_FILE_RETENTION (int | str): The retention period for log files.
            LOG_FILE_COMPRESSION (str): The compression method for log files.
            LOG_FILE_LEVEL (str): The logging level.
            NESS_ACCESS_HEADS_KEYS (list): List of necessary access header keys to log.
            IS_RECORD_RESPONSE (bool): Whether to record response content.
            IS_RECORD_HEADERS (bool): Whether to record request headers.
            IS_RECORD_UA (bool): Whether to record user agent information.
            FLITER_REQUEST_URL (list): List of URLs to filter out from logging.
        """

        MODEL: RecordModel = RecordModel.CENTRALIZED
        PROJECT_SLUG: str = "info"
        LOG_FILE_PATH: str = "."
        LOG_FILE_ROTATION: str = "00:00"
        LOG_FILE_RETENTION: int | str = 8
        LOG_FILE_COMPRESSION: str = "gz"
        LOG_FILE_LEVEL: str = "INFO"
        NESS_ACCESS_HEADS_KEYS: list = []
        IS_RECORD_RESPONSE: bool = True
        IS_RECORD_HEADERS: bool = True
        IS_RECORD_UA: bool = True
        FLITER_REQUEST_URL: list = [
            "/favicon.ico",
            "/docs",
            "/",
            "/openapi.json",
            "/health_checks",
        ]

    async def make_request_log_msg(self, request: Request) -> dict:
        """
        Create a log message for the request.

        Args:
            request (Request): The request object.

        Returns:
            dict: The log message dictionary.
        """
        log_msg = None
        if self.filter_request_url(request):
            request.state.close_record = True
        else:
            _ip, method, url = request.client.host, request.method, request.url.path

            try:
                body_form = await request.form()
            except Exception:
                body_form = None

            body = None
            try:
                body_bytes = await request.body()
                if body_bytes:
                    try:
                        body = await request.json()
                    except ValueError:
                        # print(f"Error parsing JSON body: {e}")
                        body = body_bytes.decode("utf-8", errors="replace")
            except Exception as e:
                raise e

            request.state.body = body

            try:
                user_agent = parse(request.headers["user-agent"])
                # browser = user_agent.browser.version
                # browser_major, browser_minor = (
                #     browser[0],
                #     browser[1] if len(browser) >= 2 else (0, 0),
                # )
                # user_os = user_agent.os.version
                # os_major, os_minor = (
                #     user_os[0],
                #     user_os[1] if len(user_os) >= 2 else (0, 0),
                # )

                log_msg = {
                    "headers": None
                    if not self.settings.IS_RECORD_HEADERS
                    else [
                        request.headers.get(i, "")
                        for i in self.settings.NESS_ACCESS_HEADS_KEYS
                    ]
                    if self.settings.NESS_ACCESS_HEADS_KEYS
                    else None,
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
                    "method": method,
                    "params": {
                        "query_params": parse_qs(str(request.query_params)),
                        "form": body_form,
                        "body": body,
                    },
                    "ts": f"{datetime.now():%Y-%m-%d %H:%M:%S%z}",
                }

                if not log_msg["headers"]:
                    log_msg.pop("headers")
                if not log_msg["params"]["query_params"]:
                    log_msg["params"].pop("query_params")
                if not log_msg["params"]["form"]:
                    log_msg["params"].pop("form")
                if not log_msg["params"]["body"]:
                    log_msg["params"].pop("body")

            except Exception as e:
                log_msg = {
                    "headers": None
                    if not self.settings.IS_RECORD_HEADERS
                    else [
                        request.headers.get(i, "")
                        for i in self.settings.NESS_ACCESS_HEADS_KEYS
                    ]
                    if self.settings.NESS_ACCESS_HEADS_KEYS
                    else None,
                    "url": url,
                    "method": method,
                    "params": {
                        "query_params": parse_qs(str(request.query_params)),
                        "form": body_form,
                        "body": body,
                    },
                    "ts": f"{datetime.now():%Y-%m-%d %H:%M:%S%z}",
                }
                raise e

        return log_msg

    def setup(
        self,
        app: FastAPI,
        name: str = None,
        settings: BaseSettings = None,
        *args,
        **kwargs,
    ):
        """
        Setup the Loguru Plugin for the FastAPI application.

        Args:
            app (FastAPI): The FastAPI application instance.
            name (str, optional): The name of the plugin.
            settings (Settings, optional): Configuration settings for the plugin.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        if settings is None:
            settings = self.LoguruConfig()

        init_logging(settings)
        app.add_middleware(LoguruPluginClientMiddleware, is_proxy=True, client=self)
