"""AUCR analysis plugin database table library models."""
# coding=utf-8
from datetime import datetime
from aucr_app import db


class FileUpload(db.Model):
    """File upload model default database format for analysis_plugin."""

    __searchable__ = ['id', 'md5_hash', 'uploaded_by', 'file_type', 'time_stamp']
    __tablename__ = 'uploaded_file_table'
    id = db.Column(db.Integer, primary_key=True)
    md5_hash = db.Column(db.String(32), unique=True)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    file_type = db.Column(db.String(512), index=True)
    time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        """Official Analysis Plugins Table database name object representation."""
        return '<FileUpload {}>'.format(self.md5_hash)

    def to_dict(self):
        """Return dictionary object type for API File Upload call."""
        data = {
            'id': self.id,
            'md5_hash': self.md5_hash,
            'file_type': self.file_type,
            'last_seen': self.time_stamp.isoformat() + 'Z',
            }
        return data

    def from_dict(self, data):
        """Process from dictionary object type for API Posts."""
        for field in ['file']:
            if field in data:
                setattr(self, field, data[field])
