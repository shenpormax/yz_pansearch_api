"""
    Created by fre123 at 2024-10-11.
    Description: 数据抓取配置类
        eg: pipenv run python ./src/collector/data_config.py
    Changelog: all notable changes to this file will be documented
"""

import os

import requests


class DataConfig:
    """
    数据抓取配置类
    """

    # 数据抓取配置
    BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "collector")
    DATA_DIR = os.path.join(BASE_DIR, "data")

    SPIDER_CONFIG = {
        "REQUEST_CONFIG": {"RETRIES": 5, "DELAY": 10, "TIMEOUT": 30},
        "REQUEST_HEADERS": {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        },
        "SPIDER_STATUS": os.getenv("SPIDER_STATUS", "0"),
        "SPIDER_PROXY": os.getenv("SPIDER_PROXY", ""),
        "SPIDER_PJS": os.getenv("SPIDER_PJS", "").split(";"),
        "SPIDER_PROXY_CONFIG": {
            "PROXY_URL": os.getenv("PROXY_URL", ""),
            "PROXY_HEADERS": (
                dict(
                    item.split(":")
                    for item in os.getenv("PROXY_HEADERS", "").split("@")
                    if ":" in item
                )
                if all(
                    ":" in item for item in os.getenv("PROXY_HEADERS", "").split("@")
                )
                else {}
            ),
        },
    }


data_config = DataConfig()
REQ_SESSION = requests.session()
adapter = requests.adapters.HTTPAdapter(pool_connections=200, pool_maxsize=200)
REQ_SESSION.mount("http://", adapter)
REQ_SESSION.mount("https://", adapter)
