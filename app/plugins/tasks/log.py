# coding=utf-8
"""Default aucr log function process."""
from logging import error, info


def log_call_back(ch, method, properties, log_message, error_code):
    create_log(log_message, error_code)


def create_log(log_message, error_code):
    if error_code == "info":
        info(log_message)
    elif error_code == "error":
        error(error_code)
