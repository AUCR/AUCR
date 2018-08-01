"""AUCR main analysis plugin api features."""
# coding=utf-8
import os
from flask import current_app
from flask_login import current_user
from app import db
from app.plugins.analysis.models import FileUpload
from app.plugins.analysis.file.zip import write_file_map, encrypt_zip_file
from app.plugins.reports.storage.googlecloudstorage import upload_blob, get_blob
from app.plugins.tasks.mq import index_mq_aucr_report


def call_back(ch, method, properties, file_hash):
    """File upload call back."""
    file_hash = file_hash.decode('utf8')
    zip_password = os.environ.get('ZIP_PASSWORD')
    upload_folder = os.environ.get('FILE_FOLDER')
    rabbit_mq_server_ip = os.environ.get('RABBITMQ_SERVER')
    file_blob = get_blob("aucr", str(file_hash))
    if file_blob is None:
        index_mq_aucr_report(("Processing file_hash " + file_hash), str(rabbit_mq_server_ip))
        file_name = [str(upload_folder + file_hash)]
        zip_file_name = str(file_hash + ".zip")
        encrypt_zip_file(zip_password, zip_file_name, file_name)
        upload_blob("aucr", str(upload_folder + zip_file_name), file_hash)
        os.remove(str(upload_folder + zip_file_name))


def create_upload_file(file, upload_folder) -> str:
    """Create compressed new file from uploaded file."""
    file_info = write_file_map(file, os.path.join(upload_folder))
    file_info_dict = file_info["file_info"]
    file_hash = file_info["file_hash"]
    if current_user:
        uploaded_by_id = current_user.id
        file_type = file_info_dict.type
    else:
        file_type = file_info_dict
        uploaded_by_id = 1
    duplicate_file = FileUpload.query.filter_by(file_hash=file_hash).first()
    if duplicate_file:
        pass
    else:
        uploaded_file = FileUpload.__call__(file_hash=file_hash, uploaded_by=uploaded_by_id,
                                            file_type=str(file_type))
        db.session.add(uploaded_file)
        db.session.commit()
    return file_hash


def allowed_file(filename):
    """Return filename if allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
