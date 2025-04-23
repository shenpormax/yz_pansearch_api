"""
Created by  ssy at 2025-04-11.
Description: http://so1.l71.top 抓取数据
Changelog: all notable changes to this file will be documented
"""

import concurrent.futures

from src.collector import REQ_SESSION, data_config
from src.common.remote import send_get_request, send_post_request
from src.config import LOGGER


def get_token(token_url: str, proxy_model: int = 0) -> str:
    """
    获取token
    """
    headers = {
        **data_config.SPIDER_CONFIG["REQUEST_HEADERS"],
        **{"Content-Type": "application/json"},
    }
    if proxy_model:
        proxy = {
            "http": data_config.SPIDER_CONFIG["SPIDER_PROXY_CONFIG"]["PROXY_URL"],
            "https": data_config.SPIDER_CONFIG["SPIDER_PROXY_CONFIG"]["PROXY_URL"],
        }
        headers.update(
            data_config.SPIDER_CONFIG["SPIDER_PROXY_CONFIG"]["PROXY_HEADERS"]
        )
        LOGGER.info("XXQ Spider 使用代理获取 token")
    else:
        proxy = {}

    resp = send_get_request(
        url=f"{token_url}/v/api/gettoken",
        headers=headers,
        req_session=REQ_SESSION,
        timeout=10,
        proxies=proxy,
    )
    if resp["resp_status"]:
        token = resp["resp_data"]["token"]
    else:
        token = ""
    return token


def get_xxq_data(kw: str, xxq_url, xxq_channel: str, proxy_model: int = 0) -> dict:
    """
    获取xxq数据
    """
    token = get_token(token_url=xxq_url)
    if proxy_model:
        token = token or get_token(token_url=xxq_url, proxy_model=1)

    xxq_channel_map = {
        "tt": f"{xxq_url}/v/api/getTTZJB",
        "df": f"{xxq_url}/v/api/getDyfx",
        "jz": f"{xxq_url}/v/api/getJuzi",
    }
    headers = {
        **data_config.SPIDER_CONFIG["REQUEST_HEADERS"],
        **{
            "Origin": xxq_url,
            "Content-Type": "application/json",
        },
    }
    if proxy_model:
        proxy = {
            "http": data_config.SPIDER_CONFIG["SPIDER_PROXY_CONFIG"]["PROXY_URL"],
            "https": data_config.SPIDER_CONFIG["SPIDER_PROXY_CONFIG"]["PROXY_URL"],
        }
        headers.update(
            data_config.SPIDER_CONFIG["SPIDER_PROXY_CONFIG"]["PROXY_HEADERS"]
        )
        LOGGER.info(f"XXQ Spider 使用代理获取 {xxq_channel} 数据")
    else:
        proxy = {}
    data = {"name": kw, "token": token}
    LOGGER.info(
        f"XXQ Spider 请求 {xxq_channel} 资源通道: {xxq_channel_map[xxq_channel]}"
    )
    resp = send_post_request(
        url=xxq_channel_map[xxq_channel],
        headers=headers,
        data=data,
        req_session=REQ_SESSION,
        timeout=10,
        proxies=proxy,
    )
    if resp["resp_status"]:
        if resp["resp_data"].get("list"):
            res_list = resp["resp_data"]["list"]
            for item in res_list:
                if not item.get("question", ""):
                    item["question"] = item.get("answer", "").split("\n")[0]
            result = {xxq_channel: res_list}
        else:
            # 抓取成功，但是目标服务器返回失败，考虑使用代理抓取
            result = {}
            LOGGER.error(
                f"XXQ Spider 请求 {xxq_channel} 资源通道成功，但结果不对: {resp['resp_data']}"
            )
    else:
        result = {}
        LOGGER.error(f"XXQ Spider 请求 {xxq_channel} 资源通道失败: {resp['resp_data']}")
    return result


def start(kw: str, proxy_model: int = 0) -> dict:
    """
    启动  爬虫
    """
    result = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for xxq_channel in ["tt", "df", "jz"]:
            futures.append(
                executor.submit(
                    get_xxq_data, kw, "http://so1.l71.top", xxq_channel, proxy_model
                )
            )
        for future in concurrent.futures.as_completed(futures):
            spider_data = future.result()
            if spider_data:
                result.update(spider_data)

    return result


if __name__ == "__main__":
    from pprint import pprint

    res = start(kw="七宗罪", proxy_model=0)
    pprint(res)
