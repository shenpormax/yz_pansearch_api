"""
Created by fre123 at 2024-10-11.
Description: 项目整体配置文件
Changelog: all notable changes to this file will be documented
"""

import os

from src.utils.tools import read_file


class Config:
    """
    Basic config
    """

    # Application config
    DEBUG = True
    TIMEZONE = "Asia/Shanghai"
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    ROOT_DIR = os.path.join(os.path.dirname(BASE_DIR))
    PROJECT_NAME = "yz_pansearch_api"
    API_DIR = os.path.join(BASE_DIR, "views")
    HOST = os.getenv("HOST", "0.0.0.0")
    HTTP_PORT = os.getenv("HTTP_PORT", 8067)
    WORKERS = os.getenv("WORKERS", 1)

    APP_ID_CONFIG = {"yz_pansearch_api": os.getenv("APP_TOKEN", "yz_ai_cms")}
    DOMAIN_NAME_MAP = {
        "quark": "夸克",
        "baidu": "百度",
        "xunlei": "迅雷",
        "alipan": "阿里",
        "aliyundrive": "阿里",
    }
    ALLOWED_CORS_DOMAINS = (
        str(os.getenv("ALLOWED_CORS_DOMAINS", "")).split(";")
        if str(os.getenv("ALLOWED_CORS_DOMAINS", ""))
        else []
    )
    SOURCE_CONFIG = {
        "kk": os.getenv(
            "SOURCE_KK",
            "http://mmkk3.cn",
        ).split(";"),
    }
    CACHE_DATA = {}
    CACHE_TTL = int(os.getenv("CACHE_TTL", 360))

    TAG = {
        "info": f"{PROJECT_NAME.replace('_', '-')}-info",
        "warn": f"{PROJECT_NAME.replace('_', '-')}-warn",
        "error": f"{PROJECT_NAME.replace('_', '-')}-error",
    }

    @staticmethod
    def get_version() -> str:
        """获取当前服务版本, 需要自定义 version 文件"""
        version_list = read_file(os.path.join(Config.ROOT_DIR, "version"))
        return version_list[0] if version_list else "undefined"


if __name__ == "__main__":
    print(Config.API_DIR)
