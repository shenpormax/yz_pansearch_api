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
                    target_name = Config.DOMAIN_NAME_MAP[target_domain]
                    result.append(
                        {
                            "target_name": target_name,
                            "target_url": url.replace("/n", "").replace(" ", ""),
                            "target_mark": code.replace("/n", "").replace(" ", ""),
                        }
                    )
                except Exception as _:
                    target_name = "未知"

    return result


if __name__ == "__main__":
    txt = """"image
1、斗罗大陆218:https://www.aliyundrive.com/s/yTx4nqJGvJn;

2、斗罗大陆:https://www.aliyundrive.com/s/xomaTkMsoLm;

3、斗罗大陸漫画合集:https://www.aliyundrive.com/s/QtWX95Q8iCt;

4、斗罗:https://www.aliyundrive.com/s/zPvMZLwBRKo;

5、斗罗之万相斗罗:https://pan.quark.cn/s/ce0e60cd3f19;

6、斗罗大陆4终极斗罗:https://www.aliyundrive.com/s/EQuw58aUeC8;

7、斗罗大陆4终极斗罗:https://www.aliyundrive.com/s/PbEhWBoxN2K;

8、斗罗大陆4终极斗罗:https://www.aliyundrive.com/s/ei8pm14UEht;

9、斗罗大帝:https://pan.quark.cn/s/a5c5a132a897;

10、斗罗大陆4终极斗罗txt:https://www.alipan.com/s/xLY3By12UkG;"""

    print(extract_pan_links_by_txt(txt))
