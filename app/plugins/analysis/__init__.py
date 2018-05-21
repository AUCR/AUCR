"""Analysis AUCR import __init__ that creates the analysis module framework."""
# coding=utf-8
import os
from app.plugins.analysis.routes import analysis_page
# If you want the model to create the a table for the database at run time, import it here in the init
from app.plugins.analysis import models
from multiprocessing import Process
from app.plugins.analysis.api.upload import api_page
from app.plugins.tasks.mq import get_a_task_mq
from app.plugins.analysis.file.upload import call_back


def load(app):
    """"Load function registers analysis plugin blueprint to flask."""
    tasks = "file"
    app.register_blueprint(analysis_page, url_prefix='/analysis')
    app.register_blueprint(api_page, url_prefix='/analysis')
    p = Process(target=get_a_task_mq, args=(tasks, call_back, os.environ.get('RABBITMQ_SERVER'),))
    p.start()
