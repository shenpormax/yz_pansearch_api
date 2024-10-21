"""
    Created by fre123 at 2024-10-11.
    Description: 数据处理模块
    PIPENV_DOTENV_LOCATION=./.env pipenv run python ./src/collector/data_tools.py
    Changelog: all notable changes to this file will be documented
"""

import json
import random

import requests

from src.collector import data_config


def get_by_proxy(
    url: str, headers: dict = None, timeout: int = 10, return_type: str = "json"
) -> dict:
    """
    代理请求
    """
    resp_data = {
        "resp_data": {},
        "resp_status": True,
    }
    try:
        proxy = {
            "http": data_config.SPIDER_CONFIG["SPIDER_PROXY_CONFIG"]["PROXY_URL"],
            "https": data_config.SPIDER_CONFIG["SPIDER_PROXY_CONFIG"]["PROXY_URL"],
        }
        headers.update(
            data_config.SPIDER_CONFIG["SPIDER_PROXY_CONFIG"]["PROXY_HEADERS"]
        )
        res = requests.get(url, headers=headers, proxies=proxy, timeout=timeout)
        if return_type == "json":
            resp_data["resp_data"] = res.json()
        else:
            resp_data["resp_data"] = {"text": res.text}
    except Exception as e:
        resp_data["resp_data"] = {"text": str(e)}
        resp_data["resp_status"] = False
    return resp_data


def get_js_html(data: dict, timeout: int = 60) -> str:
    """
    js 加载HTML
    Args:
        data (dict): 请求 data

    Returns:
        str: html
    """
    sk_key_list = data_config.SPIDER_CONFIG["SPIDER_PJS"]
    # 随机获取一个 key
    sk_key = random.choice(sk_key_list)
    url = f"http://PhantomJScloud.com/api/browser/v2/{sk_key}/"
    headers = {"content-type": "application/json"}
    req = requests.post(url, data=json.dumps(data), headers=headers, timeout=timeout)
    render_type = data.get("renderType", "html")
    if render_type == "json":
        html = req.json()
    else:
        html = req.text
    return html


def save_data_to_json(data, file_path: str):
    """将数据保存到文件中"""

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = []

    existing_data.append(data)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # phantomjs_data = {
    #     "url": "https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%83%AD%E9%97%A8&page_limit=50&page_start=0",
    #     "renderType": "json",
    #     "outputAsJson": True,
    # }
    # res = get_js_html(phantomjs_data)
    print(get_by_proxy(url="http://ipinfo.io/json", headers={}, timeout=10))
