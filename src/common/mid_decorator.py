"""
    Created by fre123 at 2024-10-11.
    Description: 校验中间件
    Changelog: all notable changes to this file will be documented
"""

from functools import wraps

from flask import request

from src.common.response_base import UniResponse, response_handle
from src.config import LOGGER, Config


def token_required(key_name: str = "APP-TOKEN"):
    """Token 校验装饰器"""

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if request.method == "POST":
                app_id = request.headers.get("APP-ID", "")
                app_token = str(request.headers.get(key_name, ""))
                if app_id and app_token and app_id in Config.APP_ID_CONFIG:
                    if app_token == Config.APP_ID_CONFIG[app_id]:
                        try:
                            resp = fn(*args, **kwargs)
                        except Exception as e:
                            resp = UniResponse.SERVER_UNKNOWN_ERR
                            LOGGER.error(f"请求 {request.path} 出错，{e}")
                    else:
                        LOGGER.error(
                            f"{request.path} 验证未通过，APP-ID: {app_id}, {key_name}: {app_token}"
                        )
                        resp = return_401()

                else:
                    LOGGER.error(
                        f"{request.path} 验证未通过，APP-ID: {app_id}, {key_name}: {app_token}"
                    )
                    resp = return_401()
            else:
                resp = return_401()
            return resp

        return decorator

    return wrapper


def return_401():
    """
    返回401
    """
    return response_handle(
        request=request,
        dict_value=UniResponse.NOT_AUTHORIZED,
        status=401,
    )
