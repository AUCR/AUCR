"""AUCR Chat plugin database table model handler."""
#  coding=utf-8
import udatetime
from app import db


class Chat(db.Model):
    """Chat Database Table."""

    __tablename__ = "chat"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(64), db.ForeignKey('user.username'))
    message = db.Column(db.String(512), index=True)
    room = db.Column(db.String(16), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=udatetime.utcnow)

    def __repr__(self):
        """AUCR chat plugin return messages."""
        return '<Chat {}>'.format(self.message)

