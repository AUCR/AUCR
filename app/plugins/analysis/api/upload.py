"""AUCR main analysis plugin api features."""
# coding=utf-8
import os
from flask import jsonify, request, url_for
from app import current_app
from app.plugins.api.routes import api_page
from app.plugins.api.auth import token_auth
from app.plugins.analysis.models import FileUpload
from app.plugins.analysis.file.upload import create_upload_file
from app.plugins.errors.api.errors import bad_request


@api_page.route('/upload_file', methods=['POST'])
@token_auth.login_required
def upload_file():
    """API Create new user."""
    data = request.get_json() or {}
    if 'file' not in data:
        return bad_request('must have file in fields')
    file_hash = create_upload_file(data.file, os.path.join(current_app.UPLOAD_FOLDER))
    file_upload = FileUpload
    file_upload.from_dict(data=data)
    response = jsonify(file_upload.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.upload_file', file_hash=file_hash)
    return response
