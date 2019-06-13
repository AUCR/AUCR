"""Analysis AUCR import __init__ that creates analysis plugin module framework."""
# coding=utf-8
from aucr_app.plugins.analysis.routes import analysis_page
from aucr_app.plugins.analysis import models
from aucr_app.plugins.analysis.api.upload import api_page


def load(app):
    """"Load function registers analysis plugin blueprint to flask app."""
    app.register_blueprint(analysis_page, url_prefix='/analysis')
    app.register_blueprint(api_page, url_prefix='/analysis')
