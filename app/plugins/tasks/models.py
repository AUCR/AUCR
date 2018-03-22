"""Models.py tasks plugin database library table models."""
# coding=utf-8
from datetime import datetime
from app import db, YamlInfo


class TasksPlugins(db.Model):
    """The TasksPlugins models Class defines the default database format for tasks_plugin."""

    __tablename__ = 'task_plugins'
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(256), index=True)
    time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        """Official Tasks Plugins Table database name object representation."""
        return '<TasksPlugins {}>'.format(self.task_name)


class TaskCategory(db.Model):
    """Task Category models class default database format for tasks_plugin."""

    __tablename__ = 'task_category'
    id = db.Column(db.Integer, primary_key=True)
    task_category_name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(256), index=True)
    time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        """Official Task Category Table database name object representation."""
        return '<TaskCategory {}>'.format(self.task_category_name)


def insert_initial_category_values(*args, **kwargs):
    """Insert Task category default database values from a yaml template file."""
    run = YamlInfo("app/plugins/tasks/category.yaml", "none", "none")
    category_data = run.get()
    for items in category_data:
        new_category_table_row = TaskCategory(task_category_name=items)
        db.session.add(new_category_table_row)
        db.session.commit()


db.event.listen(TaskCategory.__table__, 'after_create', insert_initial_category_values)


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
    group_access = db.Column(db.String(128), db.ForeignKey('groups.group_name'))
    is_starred = db.Column(db.Boolean, default=False)
    task_subject = db.Column(db.String(256), index=True)
    task_category = db.Column(db.String(128), db.ForeignKey('task_category.task_category_name'))
    main_business_coverage = db.Column(db.String(128), db.ForeignKey('business_coverage.business_coverage'))
    current_state = db.Column(db.Integer, db.ForeignKey('task_states.id'), index=True)

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


def insert_initial_tasks_states_values(*args, **kwargs):
    """Insert TLP default database values from a yaml template file."""
    run = YamlInfo("app/plugins/tasks/task_states.yaml", "none", "none")
    tlp_data = run.get()
    for items in tlp_data:
        new_task_state_table_row = TaskStates(task_state_name=items)
        db.session.add(new_task_state_table_row)
        db.session.commit()


db.event.listen(TaskStates.__table__, 'after_create', insert_initial_tasks_states_values)


class Tags(db.Model):
    """Tag default database table format for tasks_plugin."""

    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(256), index=True)
    time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        """Official Tag Table database name object representation."""
        return '<Tags {}>'.format(self.tag_name)


class Comments(db.Model):
    """Comment default database table format for tasks_plugin."""

    __tablename__ = 'task_comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(1024), index=True)
    time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        """Official Comments Table database name object representation."""
        return '<Comments {}>'.format(self.comment)


class TrafficLightProtocol(db.Model):
    """TLP default database table format for tasks_plugin."""

    __tablename__ = 'task_tlp'
    id = db.Column(db.Integer, primary_key=True)
    color_name = db.Column(db.String(5), index=True)
    when_description = db.Column(db.String(256), index=True)
    how_description = db.Column(db.String(512), index=True)
    quick_description = db.Column(db.String(128), index=True)

    def __repr__(self):
        """Official TLP Table database name object representation."""
        return '<TrafficLightProtocol {}>'.format(self.color_name)


def insert_initial_tlp_values(*args, **kwargs):
    """Insert TLP default database values from a yaml template file."""
    run = YamlInfo("app/plugins/tasks/tlp.yaml", "none", "none")
    tlp_data = run.get()
    for items in tlp_data:
        new_tlp_table_row = TrafficLightProtocol(
                              color_name=items, quick_description=tlp_data[items]
                              ["quick_description"], how_description=tlp_data[items]["how_description"],
                              when_description=tlp_data[items]["when_description"]
        )
        db.session.add(new_tlp_table_row)
        db.session.commit()


db.event.listen(TrafficLightProtocol.__table__, 'after_create', insert_initial_tlp_values)


class Severity(db.Model):
    """Severity default database table format for tasks_plugin."""

    __tablename__ = 'task_severity'
    id = db.Column(db.Integer, primary_key=True)
    severity = db.Column(db.Integer, index=True)

    def __repr__(self):
        """Official TLP Table database name object representation."""
        return '<Severity {}>'.format(self.severity)


def insert_initial_severity_values(*args, **kwargs):
    """Insert severity default database values from a yaml template file."""
    run = YamlInfo("app/plugins/tasks/severity.yaml", "none", "none")
    severity_data = run.get()
    for items in severity_data:
        new_severity_table_row = Severity(severity=items)
        db.session.add(new_severity_table_row)
        db.session.commit()


db.event.listen(Severity.__table__, 'after_create', insert_initial_severity_values)
