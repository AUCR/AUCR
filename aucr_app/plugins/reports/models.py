"""AUCR report plugin database table library models."""
# coding=utf-8
from aucr_app import db
import udatetime


class Log(db.Model):
    """Log tracking for report_plugin."""

    id = db.Column(db.Integer, primary_key=True)
    log_name = db.Column(db.String(128), index=True)
    time_stamp = db.Column(db.DateTime, index=True, default=udatetime.utcnow)

    def __repr__(self):
        """Log table change tracking."""
        return '<Log {}>'.format(self.report_name)
