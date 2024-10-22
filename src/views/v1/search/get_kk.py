"""
    Created by fre123 at 2024-10-11.
    Description: 示例接口说明
    Changelog: all notable changes to this file will be documented
"""

import json

from flask import current_app, request

from src.collector import kk_spider
from src.common import (
    ResponseField,
    ResponseReply,
    UniResponse,
    response_handle,
    token_required,
)
from src.config import LOGGER, Config
from src.databases import RedisBase
from src.logic.pan_baidu_tools import get_baidu_url_by_txt
from src.logic.pan_quark_tools import get_quark_url_by_txt, get_share_url_token
from src.utils import md5_encryption


@token_required()
def get_kk():
    """
    测试接口
    """
    app_logger: LOGGER = current_app.config["app_logger"]
    # 从 req header 头获取 PROXY_MODEL
    proxy_model = request.headers.get("PROXY-MODEL", 0)
    # 默认开启缓存
    is_cache = request.headers.get("IS-CACHE", "1")
    # 默认提取夸克链接
    pan_type = request.headers.get("PAN-TYPE", "quark")
    check_pan_url = request.headers.get("CHECK-PAN-URL", "1")
    pan_type_list = pan_type.lower().strip().split(";")

    redis_base: RedisBase = current_app.config["redis_base"]
    # redis初始化
    redis_db = redis_base.get_db(db=Config.REDIS_CONFIG["db"])

    # 获取基础数据
    post_data: dict = request.json
    kw = post_data.get("kw")

    if kw:
        # 是否从缓存获取数据
        md5_key = md5_encryption(f"{kw}_{pan_type_list}_{proxy_model}")
        cache_key = f"yz_pansearch:kk:{md5_key}"
        redis_data = None
        if is_cache == "1":
            redis_data = redis_db.get(cache_key)
        if redis_data:
            result = json.loads(redis_data)
        else:
            spider_data = kk_spider.start(kw, proxy_model)
            target_data = []
            if spider_data:
                for _, res_list in spider_data.items():
                    for res in res_list:
                        # cur_res_list = res.get("answer", "").split("\n")
                        res_dict = {}
                        for each_pan_type in pan_type_list:
                            res_answer = res.get("answer", "")
                            if each_pan_type == "quark":
                                quark_url_list = get_quark_url_by_txt(res_answer)
                                c_quark_url_list = []
                                if check_pan_url == "1":
                                    for each_pan_url in quark_url_list:
                                        quark_url_check_resp = get_share_url_token(
                                            quark_url=each_pan_url["url"]
                                        )
                                        if quark_url_check_resp.get("is_valid"):
                                            c_quark_url_list.append(each_pan_url)
                                else:
                                    c_quark_url_list = quark_url_list
                                if c_quark_url_list:
                                    res_dict[each_pan_type] = c_quark_url_list
                            elif each_pan_type == "baidu":
                                baidu_url_list = get_baidu_url_by_txt(res_answer)
                                if baidu_url_list:
                                    res_dict[each_pan_type] = baidu_url_list
                            else:
                                pass
                        if res_dict:
                            target_data.append(
                                {
                                    "title": res.get("question", ""),
                                    "description": "",
                                    "res_dict": res_dict,
                                }
                            )
            else:
                # 数据抓取失败
                app_logger.error(f"数据抓取失败(kk 源，请考虑使用代理)，kw: {kw}")

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
                redis_db.set(
                    cache_key, json.dumps(result), ex=Config.REDIS_CONFIG["cache_ttl"]
                )
    return response_handle(request=request, dict_value=result)
