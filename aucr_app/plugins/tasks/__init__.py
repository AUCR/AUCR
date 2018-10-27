"""Tasks AUCR import __init__ that creates the task module framework."""
# coding=utf-8
# If you want the model to create the a table for the database at run time, import it here in the init
from aucr_app.plugins.tasks.models import *


def load(app):
    """"Load function registers tasks plugin blueprint to flask."""
