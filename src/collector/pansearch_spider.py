"""
    Created by lrh at 2024-10-28.
    Description: https://www.pansearch.me/search?keywo 爬虫脚本
    Changelog: all notable changes to this file will be documented
"""

import re
import urllib.parse

import requests

from lxml import html

from src.collector import REQ_SESSION, data_config
from src.config import LOGGER


def fetch_page_data(url, headers, proxy: None):
    """发送 GET 请求并解析网页内容"""
    try:
        response = requests.get(url, headers=headers, timeout=5, proxies=proxy)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return {"err_msg": str(e)}


def parse_page_data(html_content):
    """使用 lxml 解析网页内容并提取所需数据"""
    tree = html.fromstring(html_content)
    items = tree.xpath('//div[@class="whitespace-pre-wrap break-all"]')
    data_list = []
    for item in items:
        title = (
            re.search(r"名称：(.*?)\n", item.text_content()).group(1).strip()
            if re.search(r"名称：(.*?)\n", item.text_content())
            else None
        )
        description = (
            re.search(r"描述：(.*?)\n", item.text_content()).group(1).strip()
            if re.search(r"描述：(.*?)\n", item.text_content())
            else None
        )
        url = item.xpath(".//a/@href")[0]
        data_list.append(
            {
                "title": title,
                "description": description,
                "res_dict": {"quark": [{"url": url, "code": ""}]},
            }
        )

    return data_list


def run_spider(kw: str, proxy_model: int = 0):
    """启动爬虫并返回数据"""
    # 将字符串转换为 URL 编码
    encoded_kw = urllib.parse.quote(kw)
    req_url = f"https://www.pansearch.me/search?keyword={kw}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Referer": f"https://www.pansearch.me/search?keyword={encoded_kw}",
        "Content-Type": "text/html",
        **data_config.SPIDER_CONFIG["REQUEST_HEADERS"],
    }

    if proxy_model:
        proxy = {
            "http": data_config.SPIDER_CONFIG["SPIDER_PROXY_CONFIG"]["PROXY_URL"],
            "https": data_config.SPIDER_CONFIG["SPIDER_PROXY_CONFIG"]["PROXY_URL"],
        }
        headers.update(
            data_config.SPIDER_CONFIG["SPIDER_PROXY_CONFIG"]["PROXY_HEADERS"]
        )
        LOGGER.info("Pansearch Spider 使用代理获取数据")
    else:
        proxy = {}

    html_content = fetch_page_data(req_url, headers, proxy)
    if isinstance(html_content, dict) and "err_msg" in html_content:
        print(f"请求失败: {html_content['err_msg']}")
        return None

    parsed_data = parse_page_data(html_content)
    return parsed_data


if __name__ == "__main__":
    from pprint import pprint

    data = run_spider("海贼王")
    if data:
        pprint(data)
