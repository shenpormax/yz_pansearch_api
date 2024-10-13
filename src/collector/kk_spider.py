"""
    Created by howie.hu at 2024-09-11.
    Description: http://z.kkkob.com/app/index.html 抓取数据
    Changelog: all notable changes to this file will be documented
"""

from src.collector import REQ_SESSION, data_config
from src.common.remote import send_get_request, send_post_request
from src.config import LOGGER


def get_token(proxy_model: int = 0) -> str:
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
        LOGGER.info("KK Spider 使用代理获取 token")
    else:
        proxy = {}
    resp = send_get_request(
        url="http://z.kkkob.com/v/api/getToken",
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


def get_kk_data(kw: str, kk_channel: str, proxy_model: int = 0) -> dict:
    """
    获取kk数据
    """
    token = get_token()
    if proxy_model:
        token = token or get_token(proxy_model=1)
    kk_channel_map = {
        "kk": "http://z.kkkob.com/v/api/search",
        "xy": "http://z.kkkob.com/v/api/getXiaoyu",
        "dj": "http://z.kkkob.com/v/api/getDJ",
        "jz": "http://z.kkkob.com/v/api/getJuzi",
    }
    headers = {
        **data_config.SPIDER_CONFIG["REQUEST_HEADERS"],
        **{
            "Origin": "http://z.kkkob.com",
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
        LOGGER.info(f"KK Spider 使用代理获取 {kk_channel} 数据")
    else:
        proxy = {}
    data = {"name": kw, "token": token}
    resp = send_post_request(
        url=kk_channel_map[kk_channel],
        headers=headers,
        data=data,
        req_session=REQ_SESSION,
        timeout=10,
        proxies=proxy,
    )
    if resp["resp_status"]:
        if resp["resp_data"].get("us", False):
            result = {kk_channel: resp["resp_data"]["list"]}
        else:
            # 抓取成功，但是目标服务器返回失败，考虑使用代理抓取
            result = {}
            LOGGER.error(
                f"KK Spider 请求 {kk_channel} 资源通道成功，但结果不对: {resp['resp_data']}"
            )
    else:
        result = {}
        LOGGER.error(f"KK Spider 请求 {kk_channel} 资源通道失败: {resp['resp_data']}")
    return result


def start(kw: str, proxy_model: int = 0) -> dict:
    """
    启动 KK 爬虫
    """
    # 抓取 kk_channel 为 kk 和 xy 的数据
    result = {}
    for kk_channel in ["kk", "xy", "jz"]:
        spider_data = get_kk_data(kw=kw, kk_channel=kk_channel)
        if proxy_model:
            spider_data = spider_data or get_kk_data(
                kw=kw, kk_channel=kk_channel, proxy_model=1
            )
        result.update(spider_data)
    return result


if __name__ == "__main__":
    res = start(kw="边水往事", proxy_model=1)
    print(res)
