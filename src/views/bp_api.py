"""
    Created by fre123 at 2024-10-11.
    Description: Flask 蓝图
    Changelog: all notable changes to this file will be documented
"""

from flask import Blueprint

from src.views.v1.ping import ping
from src.views.v1.search import get_kk

bp_api = Blueprint("bp_api", __name__)
version = "/v1"

bp_api.add_url_rule(f"{version}/ping", view_func=ping, methods=["GET"])
bp_api.add_url_rule(f"{version}/search/get_kk", view_func=get_kk, methods=["POST"])
