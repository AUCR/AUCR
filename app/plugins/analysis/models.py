"""AUCR analysis plugin database table library models."""
# coding=utf-8
from app import db
from datetime import datetime


class AnalysisPlugins(db.Model):
    """The Analysis Plugins models Class defines the default database format for analysis_plugin."""

    # TODO add all the possible fields we should be using
    id = db.Column(db.Integer, primary_key=True)
    analysis_name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(256), index=True)
    time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        """Official Analysis Plugins Table database name object representation."""
        return '<AnalysisPlugins {}>'.format(self.analysis_name)


class AnalysisTable(db.Model):
    """Analysis Table models Class defines default database table's all analysis plugins use."""

    __tablename__ = 'analysis_table'
    id = db.Column(db.Integer, primary_key=True)
    analysis_name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(256), index=True)
    time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    # group_access = db.Column(db.String, db.ForeignKey('group.group_name'))
    is_starred = db.Column(db.Boolean, default=False)
    analysis_subject = db.Column(db.String(256), index=True)
    # analysis_category = db.Column(db.String, db.ForeignKey('task_category.task_category_name'))
    # business_level_awareness = db.Column(db.String, db.ForeignKey('group.group_name'))
    # TODO figure this out
    # main_business_coverage = db.ManyToManyField(BusinessCoverage, related_name='incidents_affecting_main', blank=True)
    # current_state = db.Column(db.String(10), db.ForeignKey('analysis_states.id'), index=True)

    def __repr__(self):
        """Official Analysis Table database name object representation."""
        return '<AnalysisTable {}>'.format(self.analysis_name)

