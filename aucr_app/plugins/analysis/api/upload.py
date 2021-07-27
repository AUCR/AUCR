"""AUCR main analysis plugin apiv2 features."""
# coding=utf-8
import os
from flask import jsonify, request, url_for
from aucr_app import current_app
from aucr_app.plugins.apiv2.routes import api_page
from aucr_app.plugins.apiv2.auth import token_auth
from aucr_app.plugins.analysis.models import FileUpload
from aucr_app.plugins.analysis.file.upload import create_upload_file
from aucr_app.plugins.errors.api.errors import bad_request


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
    response.headers['Location'] = url_for('apiv2.upload_file', md5_hash=file_hash)
    return response
