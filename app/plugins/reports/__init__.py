"""Report AUCR import __init__ that creates the report module framework."""
# coding=utf-8
from app.plugins.reports.routes import reports_page, search_page
# If you want the model to create the a table for the database at run time, import it here in the init
from app.plugins.reports.models import ReportPlugins, ReportTable, Log, SearchForm


def load(app):
    """"Load function registers report plugin blueprint to flask."""
    app.register_blueprint(reports_page, url_prefix='/reports')
    app.register_blueprint(search_page, url_prefix='/search')
