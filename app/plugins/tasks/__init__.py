"""Tasks AUCR import __init__ that creates the task module framework."""
# coding=utf-8
from app.plugins.tasks.routes import tasks_page
# If you want the model to create the a table for the database at run time, import it here in the init
from app.plugins.tasks import models


def load(app):
    """"Load function registers tasks plugin blueprint to flask."""
    app.register_blueprint(tasks_page, url_prefix='/tasks')
