"""AUCR main path plugin framework."""
# coding=utf-8
from app.plugins.main.routes import main_template_page as main_page


def load(app):
    """"Register AUCR main plugin flask blueprint."""
    app.register_blueprint(main_page, url_prefix='/main')
