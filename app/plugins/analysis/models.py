"""AUCR analysis plugin database table library models."""
# coding=utf-8
import udatetime
from app import db


class AnalysisPlugins(db.Model):
    """Default database format for analysis_plugin."""

    __tablename__ = 'analysis_plugins'
    id = db.Column(db.Integer, primary_key=True)
    analysis_name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(256), index=True)
    time_stamp = db.Column(db.DateTime, index=True, default=udatetime.utcnow)

    def __repr__(self):
        """Official Analysis Plugins Table database name object representation."""
        return '<AnalysisPlugins {}>'.format(self.analysis_name)


class AnalysisTable(db.Model):
    """Analysis Table models Class defines default database table's all analysis plugins use."""

    __tablename__ = 'analysis_table'
    id = db.Column(db.Integer, primary_key=True)
    analysis_name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(256), index=True)
    time_stamp = db.Column(db.DateTime, index=True, default=udatetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_access = db.Column(db.String(128), db.ForeignKey('groups.name'))
    is_starred = db.Column(db.Boolean, default=False)
    analysis_subject = db.Column(db.String(256), index=True)
    task_subject = db.Column(db.String(256), db.ForeignKey('task_table.task_subject'))
    task_category = db.Column(db.String(128), db.ForeignKey('task_category.task_category_name'))
    current_state = db.Column(db.Integer, db.ForeignKey('task_states.id'), index=True)

    def __repr__(self):
        """Official Analysis Table database name object representation."""
        return '<AnalysisTable {}>'.format(self.analysis_name)


class FileUpload(db.Model):
    """File upload model default database format for analysis_plugin."""

    __searchable__ = ['id', 'file_hash', 'uploaded_by', 'file_type', 'time_stamp']
    __tablename__ = 'uploaded_file_table'
    id = db.Column(db.Integer, primary_key=True)
    file_hash = db.Column(db.String(32), index=True)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    file_type = db.Column(db.String(512), index=True)
    time_stamp = db.Column(db.DateTime, index=True, default=udatetime.utcnow)

    def __repr__(self):
        """Official Analysis Plugins Table database name object representation."""
        return '<FileUpload {}>'.format(self.file_hash)

    def to_dict(self):
        """Return dictionary object type for API File Upload call."""
        data = {
            'id': self.id,
            'file_hash': self.file_hash,
            'file_type': self.file_type,
            'last_seen': self.time_stamp.isoformat() + 'Z',
            }
        return data

    def from_dict(self, data):
        """Process from dictionary object type for API Posts."""
        for field in ['file']:
            if field in data:
                setattr(self, field, data[field])
