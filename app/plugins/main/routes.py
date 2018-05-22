"""AUCR main plugin path importer for all plugins flask app blueprints."""
# coding=utf-8
import logging
import udatetime
from flask import render_template, request, g
from flask_babel import _, get_locale
from flask_login import current_user, login_required
from app import db
from flask import Blueprint
from app.plugins.reports.forms import SearchForm


main_template_page = Blueprint('main', __name__, static_folder='static', template_folder='templates')


@main_template_page.before_app_request
def before_request() -> None:
    """Set user last seen time user."""
    if current_user.is_authenticated:
        current_user.last_seen = udatetime.utcnow().replace(tzinfo=None)
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())


@main_template_page.route('/index', methods=['GET', 'POST'])
@main_template_page.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Return default home page flask app blueprint route."""
    page = request.args.get('page', 1, type=int)
    try:
        return render_template('index.html', title=_('Home'), page=page)
    except AttributeError:
        logging.info("No groups found for this user")
        return render_template('index.html', title=_('Home'), page=page)


@main_template_page.route('/about_us', methods=['GET'])
def about_us():
    """Return the about AUCR page."""
    return render_template('about_us.html', title=_('About Us'))


@main_template_page.route('/help', methods=['GET'])
def help_page():
    """Return the Help AUCR page."""
    return render_template('help.html', title=_('Help'))


@main_template_page.route('/privacy', methods=['GET'])
def privacy():
    """Return the Privacy AUCR page."""
    return render_template('privacy.html', title=_('Privacy & Terms'))
