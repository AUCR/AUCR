# coding=utf-8
"""Default aucr log function process."""
from logging import error, info
from app.plugins.tasks.mq import get_a_task_mq
from app.plugins.analysis.file.upload import call_back


def create_log(log_message, error_code):
    if error_code == "info":
        info(log_message)
    elif error_code == "error":
        error(error_code)
