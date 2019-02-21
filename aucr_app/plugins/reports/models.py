"""AUCR report plugin database table library models."""
# coding=utf-8
from aucr_app import db
import udatetime
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_babel import _, lazy_gettext as _l


class SearchForm(FlaskForm):
    """SearchForm wtf search form builder."""

    q = StringField(_l('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        """AUCR search field init self."""
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)


class Log(db.Model):
    """Log tracking for report_plugin."""

    id = db.Column(db.Integer, primary_key=True)
    log_name = db.Column(db.String(128), index=True)
    time_stamp = db.Column(db.DateTime, index=True, default=udatetime.utcnow)

    def __repr__(self):
        """Log table change tracking."""
        return '<Log {}>'.format(self.report_name)
