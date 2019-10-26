#! /usr/bin/python

"""
@author: yan.zhao
@contact: yan.zhao@idiaoyan.com
@time: 2019/10/26 11:04
"""
import hashlib


def md5(value: str):
    """
    计算md5值

    https://blog.csdn.net/qq_878799579/article/details/74324869
    :param value:
    :return:
    """
    return hashlib.md5(value.encode('utf-8')).hexdigest()
