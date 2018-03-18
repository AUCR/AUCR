"""Auth AUCR Plugin init."""
# coding=utf-8
from app.plugins.auth.routes import auth_page
# If you want the model to create the a table for the database at run time, import it here in the init
from app.plugins.auth import models
from app.plugins.auth.api.users import api_page
from app.plugins.auth.api.groups import api_page as group_api


def load(app):
    """Load overrides for Tasks plugin to work properly."""
    # app.register_blueprint(user_main, url_prefix='/auth')
    app.register_blueprint(auth_page, url_prefix='/auth')
    app.register_blueprint(api_page, url_prefix='/auth')
    app.register_blueprint(group_api, url_prefix='/auth')
