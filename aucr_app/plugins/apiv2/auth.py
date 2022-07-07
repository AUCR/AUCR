"""Basic AUCR auth apiv2."""
# coding=utf-8
from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from aucr_app.plugins.auth.models import User
from aucr_app.plugins.errors.api.errors import error_response


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    """Check username and password with stored password hash from database."""
    user = User.query.filter_by(username=username).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)


@basic_auth.error_handler
def basic_auth_error():
    """API meh HTTP error code 401 responses."""
    return error_response(401)


@token_auth.verify_token
def verify_token(token):
    """API verify auth user token."""
    g.current_user = User.check_token(token) if token else None
    return g.current_user is not None


@token_auth.error_handler
def token_auth_error():
    """HTTP error auth token API 403 responses ."""
    return error_response(401)
