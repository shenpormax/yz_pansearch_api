"""
    Created by fre123 at 2024-10-11.
    Description:
    Changelog: all notable changes to this file will be documented
"""

from src.utils.log_middleware import get_logger

from .config import Config

LOGGER = get_logger(Config.PROJECT_NAME)
