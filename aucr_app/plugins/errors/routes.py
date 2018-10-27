"""HTTP error code plugin blueprint routes."""
# coding=utf-8
from aucr_app import db
from flask import Blueprint
from aucr_app.plugins.errors.handlers import render_error_page_template

errors_page = Blueprint('errors', __name__, template_folder='templates')


@errors_page.app_errorhandler(403)
def forbidden_found_error(error):
    """Return http error code 403 forbidden page."""
    return render_error_page_template(error)


@errors_page.app_errorhandler(404)
def not_found_error(error):
    """Return http error code 404 not found page."""
    return render_error_page_template(error)


@errors_page.app_errorhandler(429)
def too_many_requests_error(error):
    """Return http error code 429 too many requests page."""
    return render_error_page_template(error)


@errors_page.app_errorhandler(500)
def internal_error(error):
    """Return http error code 500 internal server error page."""
    db.session.rollback()
    return render_error_page_template(error)


@errors_page.app_errorhandler(502)
def bad_gateway_error(error):
    """Return http error code 502 error bad gateway page."""
    return render_error_page_template(error)
