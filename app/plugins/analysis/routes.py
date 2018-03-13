"""AUCR analysis plugin default flask app blueprint routes."""
# coding=utf-8
from flask import Blueprint, render_template
from flask_login import login_required
# If you want the model to create the a table for the database at run time, import it here in the init
from app.plugins.analysis.models import AnalysisPlugins


analysis_page = Blueprint('analysis', __name__, template_folder='templates')


@analysis_page.route('', methods=['GET'])
@login_required
def analysis():
    """Return AUCR analysis plugin flask app analysis blueprint."""
    analysis_info = AnalysisPlugins.query.all()
    return render_template('analysis.html', title='Analysis', analysis_info=analysis_info)
