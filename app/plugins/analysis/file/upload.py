"""AUCR main analysis plugin api features."""
# coding=utf-8
import os
from flask import current_app
from flask_login import current_user
from app import db
from app.plugins.analysis.models import FileUpload
from app.plugins.analysis.file.zip import compress_zip_file_map


def create_upload_file(file, upload_folder) -> str:
    """Create compressed new file from uploaded file."""
    file_hash = compress_zip_file_map(file, os.path.join(upload_folder))
    if current_user:
        uploaded_by_id = current_user.id
    else:
        uploaded_by_id = 1
    uploaded_file = FileUpload.__call__(file_hash=file_hash, uploaded_by=uploaded_by_id)
    db.session.add(uploaded_file)
    db.session.commit()
    return file_hash


def allowed_file(filename):
    """Return filename if allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
