"""AUCR report plugin database table library models."""
# coding=utf-8
from app import db
from datetime import datetime
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_babel import _, lazy_gettext as _l


class ReportPlugins(db.Model):
    """The Report Plugins models defines default database format for report_plugin."""

    id = db.Column(db.Integer, primary_key=True)
    report_name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(256), index=True)
    time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        """Official Report Plugins Table database name object representation."""
        return '<ReportPlugins {}>'.format(self.report_name)


class ReportTable(db.Model):
    """Report Table models Class defines default database table's all report plugins use."""

    __tablename__ = 'report_table'
    id = db.Column(db.Integer, primary_key=True)
    report_name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(256), index=True)
    time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_access = db.Column(db.String, db.ForeignKey('group.group_name'))
    is_starred = db.Column(db.Boolean, default=False)
    # task_subject = db.Column(db.String, db.ForeignKey('task_category.task_subject'))
    task_category = db.Column(db.String, db.ForeignKey('task_category.task_category_name'))
    business_level_awareness = db.Column(db.String, db.ForeignKey('group.group_name'))
    # main_business_coverage = db.ManyToManyField(BusinessCoverage, related_name='incidents_affecting_main', blank=True)
    # current_state = db.Column(db.String(10), db.ForeignKey('report_states.id'), index=True)

    def __repr__(self):
        """Official Report Table database name object representation."""
        return '<ReportTable {}>'.format(self.report_name)


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
    time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        """Log table change tracking."""
        return '<Log {}>'.format(self.report_name)
