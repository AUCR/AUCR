"""Imports plugins directory using load app call."""
# coding=utf-8
import glob
import importlib
import os
import logging


def init_task_plugins(app) -> None:
    """Load all AUCR Plugin flask blueprints."""
    modules = glob.glob(os.path.dirname(__file__) + "/*")
    blacklist = {'__pycache__'}
    for module in modules:
        module_name = os.path.basename(module)
        if os.path.isdir(module) and module_name not in blacklist:
            module = '.' + module_name
            module = importlib.import_module(module, package='aucr_app.plugins')
            # This gets the app defined call in the __init__.py looking for flask app objects
            module.load(app)
            logging.info("*Loaded module, %s" % module)
