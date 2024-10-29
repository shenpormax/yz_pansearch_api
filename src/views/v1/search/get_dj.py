"""
    Created by fre123 at 2024-10-28.
    Description: 获取短剧资源
    Changelog: all notable changes to this file will be documented
"""


from flask import current_app, request

from src.collector import dj_spider
from src.common import ResponseField, UniResponse, response_handle, token_required
from src.config import LOGGER, Config
from src.logic.cache_tools import get_cache, set_cache
from src.utils import md5_encryption


@token_required()
def get_dj():
    """
    测试接口
    """
    app_logger: LOGGER = current_app.config["app_logger"]
    app_config: Config = current_app.config["app_config"]
    # 从 req header 头获取 PROXY_MODEL
    proxy_model = request.headers.get("PROXY-MODEL", 0)
    # 默认开启缓存
    is_cache = request.headers.get("IS-CACHE", "1")

    # 获取基础数据
    post_data: dict = request.json
    kw = post_data.get("kw")

    if kw:
        # 是否从缓存获取数据
        md5_key = md5_encryption(f"{kw}_{proxy_model}")
        cache_key = f"yz_pansearch:dj:{md5_key}"
        redis_data = None
        if is_cache == "1":
            redis_data = get_cache(cache_key)
        if redis_data:
            result = redis_data
        else:
            spider_data = dj_spider.get_dj_data(kw, proxy_model)
            target_data = []
            if spider_data:
                for res in spider_data:
                    target_data.append(
                        {
                            "title": res["title"],
                            "description": "",
                            "res_dict": {
                                "quark": [
                                    {
                                        "url": res["url"],
                                        "code": "",
                                    }
                                ]
                            },
                        }
                    )
            else:
                # 数据抓取失败
                app_logger.error(f"数据抓取失败(dj 源，请考虑使用代理)，kw: {kw}")

            result = {
                **UniResponse.SUCCESS,
                **{
                    ResponseField.DATA: {
                        "total": len(target_data),
                        "data": target_data,
                    }
                },
            }
            if target_data and is_cache == "1":
                set_cache(cache_key, result, expire=app_config.CACHE_TTL)
    else:
        result = UniResponse.PARAM_ERR
    return response_handle(request=request, dict_value=result)
