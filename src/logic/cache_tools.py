"""
    Created by fre123 at 2024-10-24.
    Description: 内存缓存逻辑
    Changelog: all notable changes to this file will be documented
"""

import time

from src.config import LOGGER, Config


def get_cache(key: str):
    """
    获取缓存数据
    :param key:
    :return:
    """
    cache_res_data = Config.CACHE_DATA.get(key, {})
    cache_value = None
    if cache_res_data:
        if cache_res_data["expire"] > int(time.time()):
            cache_value = cache_res_data["data"]
    return cache_value


def set_cache(key: str, value: dict, expire: int = 0):
    """
    设置缓存数据
    :param key:
    :param value:
    :param expire:
    :return:
    """
    exec_status = False
    try:
        if expire == 0:
            expire = 365 * 24 * 60 * 60
        Config.CACHE_DATA[key] = {"data": value, "expire": int(time.time()) + expire}
        exec_status = True
    except Exception as e:
        LOGGER.error(f"set_cache {key}-{value}-{expire} error: {e}")
    return exec_status
