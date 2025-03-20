"""
Created by fre123 at 2024-10-11.
Description: 项目HTTP启动文件
    - 启动: pipenv run python ./api/http_app.py
Changelog: all notable changes to this file will be documented
"""

import requests

from flask import Flask, request

from src.config import LOGGER, Config
from src.views import bp_api


def create_app():
    """
    建立 web 应用
    :return:
    """
    flask_app = Flask(__name__)

    @flask_app.after_request
    def add_cors_headers(response):
        # 限制 /v1/tools/proxy 才能跨域
        if request.path == "/v1/tools/proxy":
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Methods"] = (
                "GET, POST, OPTIONS, PUT, DELETE"
            )
            response.headers["Access-Control-Allow-Headers"] = (
                "Content-Type, Authorization"
            )
            if request.method == "OPTIONS":
                response.headers["Access-Control-Max-Age"] = "3600"
        return response

    with flask_app.app_context():
        # 项目内部配置
        flask_app.config["app_config"] = Config
        flask_app.config["app_logger"] = LOGGER
        flask_app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024
        # 全局请求 session
        req_session = requests.session()
        adapter = requests.adapters.HTTPAdapter(pool_connections=200, pool_maxsize=200)
        req_session.mount("http://", adapter)
        req_session.mount("https://", adapter)
        flask_app.config["app_req_session"] = req_session
        flask_app.config["app_logger"] = LOGGER

        # 打印启动日志
        api_version = Config.get_version()
        LOGGER.info(
            f"Service({Config.PROJECT_NAME}) started successfully: {api_version}"
        )

    # 注册相关蓝图
    flask_app.register_blueprint(bp_api)

    return flask_app


app = create_app()

if __name__ == "__main__":
    app.run(port=Config.HTTP_PORT, debug=Config.DEBUG)
