"""Handlers.py is AUCR's main http error code handling backend."""
# coding=utf-8
from flask import render_template, request, current_app
from app.plugins.errors.models import Errors
from app.plugins.errors.api.errors import error_response as api_error_response
from app.plugins.tasks.mq import index_mq_aucr_report


def wants_json_response():
    """Data type json response request."""
    return request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']


def render_error_page_template(error_code):
    """Return http error code page template."""
    # TODO add random message from a list of more than a single message
    if wants_json_response():
        index_mq_aucr_report(error_code.code, current_app.config["RABBITMQ_SERVER"])
        return api_error_response(error_code)
    if error_code is int:
        error_info = Errors.query.filter_by(error_name=error_code).first()
    elif type(error_code) is int:
        error_info = Errors.query.filter_by(error_name=error_code).first()
    else:
        error_info = Errors.query.filter_by(error_name=error_code.code).first()
    return render_template('error.html', error_code_name=error_info.error_name, error_message=error_info.error_message)
