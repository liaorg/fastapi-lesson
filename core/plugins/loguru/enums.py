#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    :   enums.py
@Time    :   2025/03/04 12:29:22
@Desc    :   None
"""

from enum import Enum


class RecordModel(Enum):
    """日志记录模式"""

    # 分散式记录
    SCATTERED = "scattered"
    # 集中式记录
    CENTRALIZED = "centralized"
