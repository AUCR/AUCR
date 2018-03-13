"""Models.py tasks plugin database library table models."""
# coding=utf-8
from datetime import datetime
from app import db


class TasksPlugins(db.Model):
    """The TasksPlugins models Class defines the default database format for tasks_plugin."""

    # TODO add all the possible fields we should be using
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(256), index=True)
    time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        """Official Tasks Plugins Table database name object representation."""
        return '<TasksPlugins {}>'.format(self.task_name)


class TaskCategory(db.Model):
    """Tasks Category models class defines default database format for tasks_plugin."""

    __tablename__ = 'task_category'
    id = db.Column(db.Integer, primary_key=True)
    task_category_name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(256), index=True)
    time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        """Official Task Category Table database name object representation."""
        return '<TaskCategory {}>'.format(self.task_category_name)


class BusinessCoverage(db.Model):
    """BusinessCoverage models class defines business coverage database table format for tasks_plugin."""

    __tablename__ = 'business_coverage'
    id = db.Column(db.Integer, primary_key=True)
    business_coverage = db.Column(db.String(128), index=True)
    description = db.Column(db.String(256), index=True)
    time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        """Official Business Coverage Table database name object representation."""
        return '<BusinessCoverage {}>'.format(self.business_coverage)


class Label(db.Model):
    """Label models class defines the default database format for tasks_plugin."""

    __tablename__ = 'label'
    id = db.Column(db.Integer, primary_key=True)
    label_name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(256), index=True)
    time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        """Official Label Table database name object representation."""
        return '<Label {}>'.format(self.label_name)


class TaskTable(db.Model):
    """Task Table models Class defines default database table's all tasks plugins use."""

    __tablename__ = 'task_table'
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(256), index=True)
    time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_access = db.Column(db.String, db.ForeignKey('group.group_name'))
    is_starred = db.Column(db.Boolean, default=False)
    task_subject = db.Column(db.String(256), index=True)
    task_category = db.Column(db.String, db.ForeignKey('task_category.task_category_name'))
    business_level_awareness = db.Column(db.String, db.ForeignKey('group.group_name'))
    # TODO figure this out
    # main_business_coverage = db.ManyToManyField(BusinessCoverage, related_name='incidents_affecting_main', blank=True)
    current_state = db.Column(db.String(10), db.ForeignKey('task_states.id'), index=True)

    def __repr__(self):
        """Official Task Table database name object representation."""
        return '<TaskTable {}>'.format(self.task_name)


class TaskStates(db.Model):
    """Tasks States models class defines default database format for tasks_plugin."""

    __tablename__ = 'task_states'
    id = db.Column(db.Integer, primary_key=True)
    task_state_name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(256), index=True)
    time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        """Official Task States database name object representation."""
        return '<TaskStates {}>'.format(self.task_state_name)
