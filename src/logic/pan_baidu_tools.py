"""
    Created by fre123 at 2024-10-11.
    Description: 百度网盘常用工具
    Changelog: all notable changes to this file will be documented
"""

import re


def get_baidu_url_by_txt(source_txt: str) -> list:
    """
    从文本中提取百度网盘的链接和提取码
    Args:
        source_txt (str): 文本
    Returns:
        list: 包含链接和提取码的字典列表
    """
    result = []
    # 匹配 baidu.com 网盘完整链接和提取码
    pattern = re.compile(
        r"(https://pan\.baidu\.com/s/[a-zA-Z0-9\-]+(?:\?pwd=[a-zA-Z0-9]+)?)\s*提取码[:：\s]*([a-zA-Z0-9]+)?"
    )

    matches = pattern.findall(source_txt)

    for match in matches:
        url = match[0]
        code = match[1] if match[1] else None
        result.append({"url": url, "code": code})

    return result


if __name__ == "__main__":
    txt = """"链接：https://pan.baidu.com/s/181yhj3D3e8q5TnPbCtD4UA?pwd=8888 提取码：8888
链接：https://pan.xunlei.com/s/VO5N-Gw-SoXJtFfL5J43CmFfA1
链接：https://pan.quark.cn/s/0b60b7f36e78
边水往事 链接：https://pan.xunlei.com/s/VO8u-Sdlb7FiYvckCYI_rfe3A1?origin=lilizj# 提取码：2hbv
边水往事链接：https://pan.quark.cn/s/5f5cf42877ac?entry=sjss
边水往事链接: https://pan.baidu.com/s/1FD0DQ1xAPbSS6KYFzBdMTA?pwd=snsk 提取码: snsk
边水往事2024链接：https://pan.baidu.com/s/1n-YcUOHAeOYTKeMGHdwCoQ?pwd=yg3m 提取码：yg3m
边水往事2024（夸克）链接：https://pan.quark.cn/s/28df90b93605?entry=sjss"""
    print(get_baidu_url_by_txt(txt))
