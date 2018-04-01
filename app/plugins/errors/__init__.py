"""HTTP error code handling plugin."""
# coding=utf-8
from app.plugins.errors.routes import errors_page
# If you want the model to create the a table for the database at run time, import it here in the init
from app.plugins.errors import models


def load(app):
    """AUCR errors plugin flask app blueprint registration."""
    app.register_blueprint(errors_page, url_prefix='/errors')
