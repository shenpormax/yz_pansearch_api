"""
    Created by lrh at 2024-10-28.
    Description: https://www.pansearch.me/search?keywo 爬虫脚本
    Changelog: all notable changes to this file will be documented
"""

import re
import urllib.parse

from lxml import html

from src.collector import REQ_SESSION, data_config
from src.config import LOGGER


def fetch_page_data(url, headers, proxy: None):
    """发送 GET 请求并解析网页内容"""
    try:
        response = REQ_SESSION.get(url, headers=headers, timeout=5, proxies=proxy)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return {"err_msg": str(e)}


def parse_page_data(kw, html_content):
    """使用 lxml 解析网页内容并提取所需数据"""
    tree = html.fromstring(html_content)
    items = tree.xpath('//div[@class="whitespace-pre-wrap break-all"]')
    data_list = []
    url_list = []
    for item in items:
        url = item.xpath(".//a/@href")
        if len(url) == 1 and url[0] not in url_list:
            url = url[0]
            title = (
                re.search(r"名称：(.*?)\n", item.text_content()).group(1).strip()
                if re.search(r"名称：(.*?)\n", item.text_content())
                else ""
            )
            description = (
                re.search(r"描述：(.*?)\n", item.text_content()).group(1).strip()
                if re.search(r"描述：(.*?)\n", item.text_content())
                else ""
            )

            data_list.append(
                {
                    "title": title,
                    "description": description,
                    "url": url,
                }
            )
            url_list.append(url)
        else:
            text = item.text_content().strip()
            # 正则表达式匹配以数字开头并以分号结束的每一项
            pattern = re.compile(r"(\d+、.*?):(https://.*?);")

            # 查找所有匹配项
            matches = pattern.findall(text)

            keyword_ = kw

            # 构建字典并过滤出包含关键字的项
            result = [
                {"title": re.sub(r"^\d+、", "", title), "link": link}
                for title, link in matches
                if keyword_ in title and link not in url_list
            ]

            for item in result:
                url = item["link"]
                data_list.append(
                    {"title": item["title"], "description": "", "url": url}
                )
                url_list.append(url)

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

    parsed_data = parse_page_data(kw, html_content)
    return parsed_data


if __name__ == "__main__":
    from pprint import pprint

    data = run_spider(kw="奥特曼", proxy_model=0)
    if data:
        pprint(data)
