#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    :   json_helper.py
@Time    :   2025/03/04 12:47:10
@Desc    :   JSON 辅助工具模块
"""

import datetime
import decimal
import json


class CJsonEncoder(json.JSONEncoder):
    """自定义 JSON 编码器，支持对 datetime、date、decimal 和 bytes 类型进行编码"""

    def default(self, obj):
        """
        处理特殊类型的对象，使其可以被 JSON 序列化。

        Args:
            obj: 需要序列化的对象。

        Returns:
            序列化后的对象表示。
        """
        if hasattr(obj, "keys") and hasattr(obj, "__getitem__"):
            return dict(obj)
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, bytes):
            return str(obj, encoding="utf-8")
        return super().default(obj)


def dict_to_json(data=None):
    """
    将字典转换为 JSON 字符串。

    Args:
        data (dict, optional): 要转换的字典，默认为空字典。

    Returns:
        str: JSON 字符串。
    """
    data = {} if data is None else data
    return json.dumps(data, cls=CJsonEncoder)


def dict_to_json_ensure_ascii(data=None, ensure_ascii=False):
    """
    不格式化的输出 JSON 字符串，保持中文字符不转义。

    Args:
        data (dict, optional): 要转换的字典，默认为空字典。
        ensure_ascii (bool, optional): 是否确保 ASCII，默认为 False。

    Returns:
        str: JSON 字符串。
    """
    data = {} if data is None else data
    return json.dumps(data, cls=CJsonEncoder, ensure_ascii=ensure_ascii)


def dict_to_json_ensure_ascii_indent(data=None, ensure_ascii=False):
    """
    格式化排版缩进输出 JSON 字符串，保持中文字符不转义。

    Args:
        data (dict, optional): 要转换的字典，默认为空字典。
        ensure_ascii (bool, optional): 是否确保 ASCII，默认为 False。

    Returns:
        str: JSON 字符串。
    """
    data = {} if data is None else data
    return json.dumps(data, cls=CJsonEncoder, ensure_ascii=ensure_ascii, indent=4)


def json_to_dict(json_msg):
    """
    将 JSON 字符串转换为字典。

    Args:
        json_msg (str): JSON 字符串。

    Returns:
        dict: 解析后的字典。
    """
    return json.loads(json_msg)


def obj_to_json(obj, ensure_ascii=False):
    """
    将对象转换为 JSON 字符串。

    Args:
        obj: 要转换的对象。
        ensure_ascii (bool, optional): 是否确保 ASCII，默认为 False。

    Returns:
        str: JSON 字符串。
    """
    data = obj.__dict__
    return json.dumps(data, cls=CJsonEncoder, ensure_ascii=ensure_ascii, indent=4)


def class_to_dict(obj):
    """
    将类实例转换为字典。

    Args:
        obj: 类实例。

    Returns:
        dict: 转换后的字典。
    """
    if not obj:
        return None

    if isinstance(obj, list | set):
        return [class_to_dict(item) for item in obj]

    result = {}
    for key, value in obj.__dict__.items():
        if isinstance(
            value, datetime.datetime | datetime.date | decimal.Decimal | bytes
        ):
            result[key] = CJsonEncoder().default(value)
        elif isinstance(value, list | set):
            result[key] = [class_to_dict(item) for item in value]
        elif hasattr(value, "__dict__"):
            result[key] = class_to_dict(value)
        else:
            result[key] = value

    return result
