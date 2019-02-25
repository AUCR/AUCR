"""Report AUCR import __init__ that creates the report module framework."""
# coding=utf-8
import os
from aucr_app.plugins.reports.routes import search_page
# If you want the model to create the a table for the database at run time, import it here in the init
from aucr_app.plugins.reports.models import Log, SearchForm
from aucr_app.plugins.tasks.mq import get_a_task_mq
from aucr_app.plugins.tasks.log import log_call_back
from multiprocessing import Process


def load(app):
    """"Load function registers report plugin blueprint to flask."""
    app.register_blueprint(search_page, url_prefix='/search')
    object_storage_type = os.environ.get('OBJECT_STORAGE')
    rabbitmq_server = os.environ.get('RABBITMQ_SERVER')
    rabbitmq_username = os.environ.get('RABBITMQ_USERNAME')
    rabbitmq_password = os.environ.get('RABBITMQ_PASSWORD')
    tasks = "reports"
    if object_storage_type == "gcp":
        p = Process(target=get_a_task_mq, args=(tasks, log_call_back, rabbitmq_server, rabbitmq_username,
                                                rabbitmq_password))
        p.start()
