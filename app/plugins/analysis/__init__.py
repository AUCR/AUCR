"""Analysis AUCR import __init__ that creates the analysis module framework."""
# coding=utf-8
from app.plugins.analysis.routes import analysis_page
# If you want the model to create the a table for the database at run time, import it here in the init
from app.plugins.analysis.models import AnalysisPlugins


def load(app):
    """"Load function registers analysis plugin blueprint to flask."""
    app.register_blueprint(analysis_page, url_prefix='/analysis')
