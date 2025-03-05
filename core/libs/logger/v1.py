#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    :   v1.py
@Time    :   2025/03/04 13:51:18
@Desc    :   None
"""

import logging
import os
import platform
import sys
from datetime import UTC, datetime
from pathlib import Path
from pprint import pformat

from loguru import logger


def set_log_extras(record):
    """set_log_extras [summary].

    [extended_summary]

    Args:
        record ([type]): [description]
    """
    record["extra"]["datetime"] = datetime.now(
        UTC
    )  # Log datetime in UTC time zone, even if server is using another timezone
    record["extra"]["host"] = os.getenv(
        "HOSTNAME", os.getenv("COMPUTERNAME", platform.node())
    ).split(".")[0]
    record["extra"]["pid"] = os.getpid()
    # record["extra"]["traceid"] = correlation_id.get()


class InterceptHandler(logging.Handler):
    """
    Default infirmary_controller from examples in loguru documentaion.
    See https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record: logging.LogRecord):
        """
        Emit a log record.

        This method is called by the logging system to output the log message.
        It converts the logging record into a Loguru log entry and logs it using Loguru's logger.

        Args:
            record (logging.LogRecord): The log record to be emitted.
        """
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(
            depth=depth,
            exception=record.exc_info,
        ).log(level, record.getMessage())


def format_record_v2(record: dict) -> str:
    """Return an custom format for loguru loggers.

    Uses pformat for log any data like request/response body
    >>> [   {   'count': 2,
    >>>         'users': [   {'age': 87, 'is_active': True, 'name': 'Nick'},
    >>>                      {'age': 27, 'is_active': True, 'name': 'Alex'}]}]
    """
    format_string = "<green>{extra[datetime]}</green> | "
    format_string += "<green>{extra[app_name]}</green> | "
    format_string += "<green>{extra[host]}</green> | "
    format_string += "<green>{extra[pid]}</green> | "
    format_string += "<green>{extra[traceid]}</green> | "
    format_string += "<level>{level: <8}</level> | "
    format_string += "<cyan>{name}</cyan>:"
    format_string += "<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    format_string += "<level>{message}</level>"

    # This is to nice print data, like:
    # logger.bind(payload=dataobject).info("Received data")
    if record["extra"].get("payload") is not None:
        record["extra"]["payload"] = pformat(
            record["extra"]["payload"], indent=4, compact=True, width=88
        )
        format_string += "\n<level>{extra[payload]}</level>"

    format_string += "{exception}\n"

    return format_string


def format_record(record: dict) -> str:
    """
    Custom format for loguru loggers.
    Uses pformat for log any data like request/response body during debug.
    Works with logging if loguru handles it.

    Example:
    >>> payload = [{"users":[{"name": "Nick", "age": 87, "is_active": True}, {"name": "Alex", "age": 27, "is_active": True}], "count": 2}]
    >>> logger.bind(payload=).debug("users payload")
    >>> [   {   'count': 2,
    >>>         'users': [   {'age': 87, 'is_active': True, 'name': 'Nick'},
    >>>                      {'age': 27, 'is_active': True, 'name': 'Alex'}]}]
    """
    # 等级
    format_string = "<level>{level: <5}</level> |"
    # 时间
    format_string += "<green>{time:YYYY-MM-DD HH:mm:ss}</green> |"
    # IP
    if record["extra"].get("ip") is not None:
        format_string += " <cyan>ip:{extra[ip]} </cyan>|"
        # 记录进程和线程信息
    format_string += "<green>P:{process.name}</green> |"
    format_string += "<green>T:{thread.id}:{thread.name}</green> |"

    # format_string += "<cyan>{module}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>  |"

    # 扩展自定义字段--需要使用 logger.bind(ip=get_client_ip(request))来设置扩展字段信息的值
    # 日志时间
    #  format = " {time:YYYY-MM-DD HH:mm:ss:SSS} | process_id:{process.id} process_name:{process.name} | thread_id:{thread.id} thread_name:{thread.name} | {level} |\n {message}"

    #       serializable = {
    #             "text": text,
    #             "record": {
    #                 "elapsed": {
    #                     "repr": record["elapsed"],
    #                     "seconds": record["elapsed"].total_seconds(),
    #                 },
    #                 "exception": exception,
    #                 "extra": record["extra"],
    #                 "file": {"name": record["file"].name, "path": record["file"].path},
    #                 "function": record["function"],
    #                 "level": {
    #                     "icon": record["level"].icon,
    #                     "name": record["level"].name,
    #                     "no": record["level"].no,
    #                 },
    #                 "line": record["line"],
    #                 "message": record["message"],
    #                 "module": record["module"],
    #                 "name": record["name"],
    #                 "process": {"id": record["process"].id, "name": record["process"].name},
    #                 "thread": {"id": record["thread"].id, "name": record["thread"].name},
    #                 "time": {"repr": record["time"], "timestamp": record["time"].timestamp()},
    #             },
    #         }

    # 日志中客户端来源IP信息

    # 忽略这个
    # format_string += (
    #     # name 项目app
    #     # function 函数名称
    #     # line 发生日志记录在第几行
    #     "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    # )

    #      request.state.traceid = str(shortuuid.uuid())
    #             request.state.traceindex = 0
    if record["extra"].get("traceid") is not None:
        if record["extra"].get("traceindex") is not None:
            format_string += " reqId:{extra[traceid]} index:{extra[traceindex]} |"
        else:
            format_string += " reqId:{extra[traceid]} |"

    if record["extra"].get("event_name") is not None:
        format_string += " event:{extra[event_name]} |"

    if record["extra"].get("cost_time") is not None:
        format_string += " cost_time:{extra[cost_time]} |"

    # 正式的日志内容
    format_string += " - <level>{message}</level>"

    # 绑定时候是否包含有payload，有的话则换行
    if record["extra"].get("payload") is not None:
        record["extra"]["payload"] = pformat(
            record["extra"]["payload"], indent=4, compact=True, width=88
        )
        format_string += "\n<level>{extra[payload]}</level>"

    format_string += "{exception}\n"

    return format_string


def init_logging(app_config):
    """
    Replaces logging infirmary_controller with a infirmary_controller for using the custom infirmary_controller.

    WARNING!
    if you call the init_logging in startup event function,
    then the first logs before the application start will be in the old format
    >>> core_app.add_event_handler("startup", init_logging)
    stdout:
    INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
    INFO:     Started reloader process [11528] using statreload
    INFO:     Started server process [6036]
    INFO:     Waiting for application startup.
    2020-07-25 02:19:21.357 | INFO     | uvicorn.lifespan.on:startup:34 - Application startup complete.

    """
    # disable infirmary_controller for specific uvicorn loggers
    # to redirect their output to the default uvicorn logger
    # infirmary_tasks with uvicorn==0.11.6
    loggers = (
        logging.getLogger(name)
        for name in logging.root.manager.loggerDict
        if name.startswith("uvicorn.")
    )

    for uvicorn_logger in loggers:
        uvicorn_logger.handlers = []

    # change infirmary_controller for default uvicorn logger
    # 加上这段会导致日志输出断层或只是偶尔记录
    intercept_handler = InterceptHandler()
    logging.getLogger("uvicorn").handlers = [intercept_handler]
    # logging.getLogger("uvicorn").infirmary_controller = []
    logging.getLogger("rocketry").handlers = []
    # set logs output, level and format
    logger.configure(
        handlers=[{"sink": sys.stdout, "level": logging.DEBUG, "format": format_record}]
    )
    #   logger.add参数：
    #
    # sink：要添加的日志记录器的句柄。它可以是一个函数，一个可调用的对象，或者一个字符串（用于表示内置的日志记录器）。
    #
    # backtrace：是一个布尔值，用于指定是否应在每条日志消息中包含执行跟踪。默认情况下，它被设置为False。
    #
    # colorize：是一个布尔值，用于指定是否应将日志消息中的消息类型颜色化。默认情况下，它被设置为True。
    #
    # format：表示将要用于格式化日志消息的字符串。默认情况下，它被设置为"{time} | {level} | {message}（{file}：{line}）"。
    #
    # enqueue：是一个布尔值，用于指定是否应将日志消息发送到内部消息队列，以便异步处理。默认情况下，它被设置为False。
    #
    # level：表示要记录的最低日志级别的字符串。默认情况下，它被设置为"INFO"。
    #
    # filter：表示要过滤的日志消息的字符串，只有包含该字符串的日志消息才会被记录。默认情况下，它被设置为None。
    #
    # close_atexit：是一个布尔值，用于指定是否应在程序退出时关闭日志记录器。默认情况下，它被设置为True。
    logger.add(
        Path(app_config.LOG_FILE_PATH) / f"{app_config.PROJECT_SLUG}.log",
        rotation=app_config.LOG_FILE_ROTATION,
        retention=app_config.LOG_FILE_RETENTION,
        compression=app_config.LOG_FILE_COMPRESSION,
        enqueue=True,
        backtrace=True,
        # serialize=True, # the record is provided as a JSON string to the infirmary_controller
        level=app_config.LOG_FILE_LEVEL,
        format=format_record,
    )

    return logger.bind(traceid=None, method=None)
