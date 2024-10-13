"""
    Created by fre123 at 2024-10-11.
    Description: 网盘常用处理工具
    Changelog: all notable changes to this file will be documented
"""

import random
import re
import time
import urllib.parse

from src.common.remote import send_post_request
from src.config import LOGGER


def get_quark_url_by_txt(source_txt: str) -> str:
    """
    从文本中提取 url
    Args:
        source_txt (str): 文本
    """
    url_list = []
    clean_urls = re.findall(r"pan\.quark\.cn/s/\w+", source_txt)
    if clean_urls:
        for each_url in clean_urls:
            each_url = f"https://{each_url.strip()}"
            url_list.append(each_url)
    return url_list


def get_share_url_token(quark_url: str) -> dict:
    """
    获取分享链接的 stoken 和 title，无需登录
    Args:
        quark_url (str): 分享链接的 pwd_id
    """
    pwd_id = quark_url.split("#")[0].split("?")[0].split("/s/")[1]
    base_url_h = "https://drive-h.quark.cn"
    base_url_pc = "https://drive-pc.quark.cn"
    target_url = f"{base_url_h}/1/clouddrive/share/sharepage/token"
    params = {
        "pr": "ucpro",
        "fr": "pc",
        "uc_param_str": "",
        "__dt": random.randint(100, 9999),
        "__t": int(time.time()) * 1000,
    }
    # 拼接 target_url 和 params
    url_with_params = f"{target_url}?{urllib.parse.urlencode(params)}"

    req_resp_data = send_post_request(
        url=url_with_params, data={"pwd_id": pwd_id, "passcode": ""}, timeout=10
    )
    resp_data = req_resp_data["resp_data"]

    if req_resp_data["resp_status"]:
        # 请求成功
        if resp_data.get("status", -1) != 200:
            return_res = {
                "is_valid": False,
                "stoken": "",
                "stitle": "",
                "resp_data": resp_data,
            }
        else:
            return_res = {
                "is_valid": True,
                "stoken": resp_data.get("data", {}).get("stoken", ""),
                "stitle": resp_data.get("data", {}).get("title", ""),
                "resp_data": resp_data,
            }
    else:
        return_res = {}
        LOGGER.error(f"pan_quark_tools get_share_url_token 请求出错: {resp_data}")

    return return_res


if __name__ == "__main__":
    quark_url = "https://pan.quark.cn/s/28df90b93605?entry=sjss#/list/share"
    print(get_share_url_token(quark_url))
