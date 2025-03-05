#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    :   logger.py
@Time    :   2025/03/04 12:40:16
@Desc    :   None
"""

from datetime import datetime
from time import perf_counter

from fastapi import Request
from loguru import logger as log

from core.tools.json_helper import dict_to_json

from .contextvar import logrequest
from .enums import RecordModel


def get_client_ip(request: Request):
    """
    获取客户端真实ip
    :param request:
    :return:
    """
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0]
    return request.client.host


def info(msg, event_name="logic", model=RecordModel.SCATTERED):
    """记录日志"""
    try:
        assert hasattr(logrequest.state, "traceid"), "需要先初始化日志插件对象"
        if (
            hasattr(logrequest.state, "close_record")
            and not logrequest.state.close_record
        ):
            # 分散日志记录
            traceid = logrequest.state.traceid
            # 叠加事件ID编号
            logrequest.state.traceindex = traceindex = logrequest.state.traceindex + 1
            start_time = logrequest.state.start_time
            end_time = f"{(perf_counter() - start_time):.2f}"
            # 每个打点记录的都记录一下消耗的时间
            if logrequest.state.record_model == model:
                try:
                    log.bind(
                        traceid=traceid,
                        event_name=event_name,
                        cost_time=end_time,
                        traceindex=traceindex,
                        ip=get_client_ip(request=logrequest),
                    ).info(msg)
                except Exception:
                    return None
            else:
                # 集中式日志日志记录
                logmsg = {
                    # 定义链路所以序号
                    "trace_index": traceindex,
                    # 时间类型描述描述
                    "event_name": event_name,
                    # 日志内容详情
                    "msg": msg,
                    "cost_time": end_time,
                    "ts": f"{datetime.now():%Y-%m-%d %H:%M:%S%z}",
                }
                logrequest.state.trace_logs_record.append(dict_to_json(logmsg))
                # 标记事件结尾开始记录日志
                if event_name == "response":
                    try:
                        log.bind(
                            traceid=traceid, ip=get_client_ip(request=logrequest)
                        ).info(f"[{','.join(logrequest.state.trace_logs_record)}]")
                    except Exception:
                        return None
                pass

    except Exception:
        log.bind(event_name=event_name).info(msg)
    else:
        # 忽略整个请求链路下所有其他日志的日志请求
        pass
