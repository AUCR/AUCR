"""AUCR main analysis plugin api features."""
# coding=utf-8
import os
from flask_login import current_user
from app import db
from app.plugins.analysis.models import FileUpload
from app.plugins.analysis.file.zip import compress_zip_file_map


def create_upload_file(file, upload_folder) -> str:
    """Create compressed new file from uploaded file."""
    file_hash = compress_zip_file_map(file, os.path.join(upload_folder))
    uploaded_file = FileUpload.__call__(file_hash=file_hash, uploaded_by=current_user.id)
    db.session.add(uploaded_file)
    db.session.commit()
    return file_hash
