#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    :   base.py
@Time    :   2025/03/26 09:40:01
@Desc    :   一些练习
"""


def multiply_table():
    """九九乘法表"""
    i = 1
    while i <= 9:
        j = 1
        while j <= i:
            print(f"{j}*{i}={j * i}", end=" ")
            j += 1
        print()
        i += 1


def prime_number(rangeInt: int):
    """打印 range 范围内的素数
    素数/质数：大于1的自然数中，除了1和自身之外无法被其他自然数整除的数
    """
    for i in range(2, rangeInt):
        for j in range(2, i):
            if i % j == 0:
                print(f"{i}不是素数: {i}//{j},{i}%{j}={divmod(i, j)}")
                break
        else:
            print(f"{i}是素数")
