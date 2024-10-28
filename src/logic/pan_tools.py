"""
    Created by fre123 at 2024-10-28.
    Description: 
    Changelog: all notable changes to this file will be documented
"""

import re

from src.config import Config
from src.utils import extract_domain


def extract_pan_links_by_txt(source_txt: str) -> list:
    """
    从文本中提取各大网盘的链接和提取码
    """
    result = []
    if source_txt:
        # 匹配 baidu.com 网盘完整链接和提取码
        url_regex = re.compile(r"https?://[^\s]+")
        code_regex = re.compile(r"提取码[:：]\s*([a-zA-Z0-9]+)")

        for each_line in source_txt.split("\n"):
            urls = url_regex.findall(each_line)
            url = urls[0] if urls else ""
            code_match = code_regex.search(each_line)
            code = code_match.group(1) if code_match else ""
            if url:
                try:
                    target_domain = extract_domain(url)
                    target_name = Config.DOMAIN_NAME_MAP.get(
                        target_domain, target_domain
                    )
                except Exception as _:
                    target_name = "未知"
                result.append(
                    {
                        "target_name": target_name,
                        "target_url": url.replace("/n", "").replace(" ", ""),
                        "target_mark": code.replace("/n", "").replace(" ", ""),
                    }
                )

    return result



if __name__ == "__main__":
    txt = """"我用夸克网盘分享了「2024抖音、小红书违禁词汇总.pdf」，点击链接即可保存。打开「夸克APP」在线查看，支持多种文档格式转换。
链接：https://pan.quark.cn/s/4f4b518f8519提取码：9NdY"""

    print(extract_pan_links_by_txt(txt))
