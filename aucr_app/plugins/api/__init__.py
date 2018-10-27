"""AUCR API blueprint plugin."""
# coding=utf-8
from aucr_app.plugins.api.routes import api_page
# If you want the model to create the a table for the database at run time, import it here in the init


def load(app):
    """Load overrides for Tasks plugin to work properly."""
    app.register_blueprint(api_page, url_prefix='/api')
