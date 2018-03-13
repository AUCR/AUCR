"""Imports plugins directory using load app call."""
# coding=utf-8
import glob
import importlib
import os
import logging

# TODO make it so we can render the entire nav bar based on group permissions and allow plugins to add to it


def register_plugin_assets_directory(app, base_path)-> None:
    """Register AUCR plugin flask app blueprint assets directory."""
    base_path = base_path.strip('/')
    rule = '/' + base_path + '/<path:path>'
    app.add_url_rule(rule=rule, endpoint=base_path)


def init_task_plugins(app)-> None:
    """Load all AUCR Plugin flask blueprints."""
    modules = glob.glob(os.path.dirname(__file__) + "/*")
    blacklist = {'__pycache__'}
    for module in modules:
        module_name = os.path.basename(module)
        if os.path.isdir(module) and module_name not in blacklist:
            module = '.' + module_name
            module = importlib.import_module(module, package='app.plugins')
            # This gets the app defined call in the __init__.py looking for flask app objects
            module.load(app)
            logging.info("*Loaded module, %s" % module)
