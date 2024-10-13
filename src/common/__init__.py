"""
    Created by fre123 at 2024-10-11.
    Description: 通用模块
    Changelog: all notable changes to this file will be documented
"""

from .mid_decorator import token_required
from .response_base import (
    ResponseCode,
    ResponseField,
    ResponseReply,
    UniResponse,
    response_handle,
)
