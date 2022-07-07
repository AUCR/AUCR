"""AUCR main plugin path importer for all plugins flask app blueprints."""
# coding=utf-8
import udatetime
from flask import render_template, request, g, current_app
from flask_babel import _, get_locale
from flask_login import current_user, login_required
from aucr_app import db
from flask import Blueprint
from aucr_app.plugins.auth.forms import SearchForm


main_template_page = Blueprint('main', __name__, static_folder='static', template_folder='templates')
no_template_page = Blueprint('/', __name__, static_folder='static', template_folder='templates')


@main_template_page.before_app_request
def before_request() -> None:
    """Set user last seen time user."""
    if current_user.is_authenticated:
        current_user.last_seen = udatetime.utcnow().replace(tzinfo=None)
        try:
            db.session.commit()
        except:
            pass
        g.search_form = SearchForm()
    g.locale = str(get_locale())


@no_template_page.route('/', methods=['GET', 'POST'])
@main_template_page.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Return default home page flask app blueprint route."""
    page = request.args.get('page', 1, type=int)
    return render_template('index.html', title=_('Home'), page=page, app_title=current_app.config["APP_TITLE"])


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
    privacy_policy_url = "None"
    if current_app.config["PRIVACY_POLICY_URL"]:
        privacy_policy_url = current_app.config["PRIVACY_POLICY_URL"]
    return render_template('privacy.html', title=_('Privacy & Terms'), privacy_policy_url=privacy_policy_url)
