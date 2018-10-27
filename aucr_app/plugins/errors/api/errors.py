"""AUCR http error code plugin response process."""
# coding=utf-8
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def error_response(status_code, message=None):
    """Return HTTP error code response."""
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    try:
        response.status_code = status_code.code
    except AttributeError:
        response.status_code = status_code
    return response


def bad_request(message):
    """HTTP error code 400 bad request messages."""
    return error_response(400, message)
