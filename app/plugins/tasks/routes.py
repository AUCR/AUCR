"""AUCR task plugin default flask app blueprint routes."""
# coding=utf-8
from flask import Blueprint, render_template
from flask_login import login_required
# If you want the model to create the a table for the database at run time, import it here in the init
from app.plugins.tasks.models import TasksPlugins

tasks_page = Blueprint('tasks', __name__, template_folder='templates')


@tasks_page.route('/tasks', methods=['GET'])
@login_required
def tasks():
    """Return AUCR task plugin flask app tasks blueprint."""
    task_info = TasksPlugins.query.all()
    return render_template('tasks.html', title='Tasks', task_info=task_info)
