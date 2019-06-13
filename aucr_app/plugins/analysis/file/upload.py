"""AUCR main analysis plugin api features."""
# coding=utf-8
import os
from flask import current_app, g
from flask_login import current_user
from aucr_app import db
from aucr_app.plugins.analysis.models import FileUpload
from aucr_app.plugins.analysis.file.zip import write_file_map


def create_upload_file(file, upload_folder) -> str:
    """Create compressed new file from uploaded file."""
    file_info = write_file_map(file, os.path.join(upload_folder))
    file_info_dict = file_info["file_info"]
    md5_hash = file_info["md5_hash"]
    if current_user:
        try:
            uploaded_by_id = current_user.id
        except AttributeError:
            uploaded_by_id = g.current_user.id
        file_type = file_info_dict.type
    else:
        file_type = file_info_dict
        uploaded_by_id = 1
    duplicate_file = FileUpload.query.filter_by(md5_hash=md5_hash).first()
    if duplicate_file:
        pass
    else:
        uploaded_file = FileUpload.__call__(md5_hash=md5_hash, uploaded_by=uploaded_by_id, file_type=str(file_type))
        db.session.add(uploaded_file)
        db.session.commit()
    return md5_hash


def allowed_file(filename):
    """Return filename if allowed."""
    result = '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
    if '.' not in filename:
        result = True
    return result
