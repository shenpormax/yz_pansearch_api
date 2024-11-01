"""
    Created by howie.hu at 2024-09-11.
    Description: http://z.kkkob.com/app/index.html 抓取数据
    Changelog: all notable changes to this file will be documented
"""

from src.collector import REQ_SESSION, data_config
from src.common.remote import send_get_request
from src.config import LOGGER


def get_dj_data(kw: str, proxy_model: int = 0) -> str:
    """
    获取token
    """
    LOGGER.info(f"DJ Spider 请求 soju.ee 资源通道")
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
        LOGGER.info("DJ Spider 使用代理获取数据")
    else:
        proxy = {}
    resp = send_get_request(
        url=f"https://soju.ee/api/search?page_no=1&page_size=50&title={kw}",
        headers=headers,
        req_session=REQ_SESSION,
        timeout=10,
        proxies=proxy,
    )
    get_res = resp["resp_data"]
    if resp["resp_status"]:
        if get_res["code"] == 200:
            resp_data = get_res["data"]["items"]
        else:
            resp_data = []
    else:
        resp_data = []
    return resp_data


if __name__ == "__main__":
    from pprint import pprint

    res = get_dj_data(kw="机", proxy_model=0)
    pprint(res)
