"""AUCR report plugin default flask app blueprint routes."""
# coding=utf-8
from flask import Blueprint, render_template
from flask_login import login_required
from flask_babel import _
# If you want the model to create the a table for the database at run time, import it here in the init
from app.plugins.reports.models import ReportPlugins

# Search plugin flask blueprints routes for search features.

reports_page = Blueprint('reports', __name__, template_folder='templates')
search_page = Blueprint('search', __name__, template_folder='templates')


@reports_page.route('/reports', methods=['GET'])
@login_required
def reports():
    """Return AUCR report plugin flask app report blueprint."""
    reports_info = ReportPlugins.query.all()
    return render_template('reports.html', title='Reports', report_info=reports_info)


@reports_page.route('/leaderboard', methods=['GET'])
@login_required
def get_leaderboard():
    """Return the leaderboard AUCR page."""
    return render_template('../spartan/templates/leaderboard.html', title=_('Leaderboard'))
