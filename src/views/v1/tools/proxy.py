"""
    Created by howie.hu at 2024-11-23.
    Description: RSS tools
    Changelog: all notable changes to this file will be documented
"""

from urllib.parse import urlparse

import requests

from flask import Response, request

from src.config import LOGGER, Config


def is_url_allowed(url):
    """检查URL是否在允许列表中"""
    is_ok = False
    try:
        parsed = urlparse(url)
        if Config.ALLOWED_CORS_DOMAINS:
            is_ok = parsed.netloc in Config.ALLOWED_CORS_DOMAINS
        else:
            is_ok = True
    except Exception as _:
        is_ok = False
    return is_ok


def proxy():
    """
    代理接口，开放
    """
    if request.method == "OPTIONS":
        return "", 200
    # 获取目标URL
    target_url = request.args.get("url")

    if not target_url:
        return {"error": "Missing url parameter"}, 400

    # 安全检查
    if not is_url_allowed(target_url):
        return {"error": "URL not allowed"}, 403

    try:
        # 构建请求头，移除一些敏感header
        headers = dict(request.headers)
        headers["Host"] = urlparse(target_url).netloc
        headers.pop("If-None-Match", None)
        # headers.update({"Cache-Control": "no-cache"})

        # 转发请求
        if request.method == "GET":
            resp = requests.get(
                target_url, headers=headers, params=request.args.copy(), timeout=10
            )
        else:  # POST
            resp = requests.post(
                target_url, headers=headers, json=request.get_json(), timeout=10
            )

        # 构建响应
        excluded_headers = [
            "content-encoding",
            "content-length",
            "transfer-encoding",
            "connection",
        ]
        headers = [
            (name, value)
            for (name, value) in resp.raw.headers.items()
            if name.lower() not in excluded_headers
        ]

        return Response(resp.content, resp.status_code, headers)

    except requests.exceptions.RequestException as e:
        LOGGER.error(f"Failed to proxy request: {e}")
        return {"error": "Failed to proxy request"}, 500
