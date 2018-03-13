"""AUCR main driver init database model creation and import plugins."""
# coding=utf-8
import logging
import os
import rq
import yaml
from redis import Redis
from config import Config
from elasticsearch import Elasticsearch
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from app.plugins import init_task_plugins
from app.plugins import init_task_plugins
from logging.handlers import SMTPHandler, RotatingFileHandler


class YamlInfo:
    """ProjectInfo Class gets and loads the project information like authors, version and license."""

    yaml_info_dict = {}

    def __init__(self, yaml_config_file, option, input_file) -> None:
        """Load project information and license info."""
        with open(yaml_config_file, 'rb') as input_config_file_object:
            project_info_strings = input_config_file_object.read()
        self.yaml_info_dict = yaml.load(project_info_strings)
        if option == "strip":
            if input_file == "LICENSE":
                with open("LICENSE") as license_file:
                    license_strings = license_file.read()
                self.yaml_info_dict["license"] = license_strings.strip('\n')

    def get(self) -> dict:
        """Return project_info as a dict."""
        return self.yaml_info_dict


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l("Please log in to access this page.")
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()


def create_app(config_class=Config):
    """Start AUCR app flask object."""
    logging.info("Getting Project Info")
    run = YamlInfo("projectinfo.yml", "strip", "LICENSE")
    project_data = run.get()
    project_info_data = project_data["info"]
    project_version_data = project_data["version"]
    # Nice Formatting Suggestion from iofault
    __version__ = "%(major)s.%(minor)s.%(revision)s" % project_version_data
    logging.info("Starting AUCR v" + __version__)
    for items in project_info_data:
        logging.info(str(items) + ":" + str(project_info_data[items]))
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('aucr-tasks', connection=app.redis)
    init_task_plugins(app)
    from app.plugins.main import main_page as main_bp
    app.register_blueprint(main_bp)
    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='AUCR Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/aucr.log', maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s '
                                                        '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('AUCR startup')
    init_task_plugins(app)
    return app


def aucr_app():
    """AUCR app flask function framework create and get things started."""
    app = create_app()
    app.secret_key = os.urandom(64)
    app.app_context().push()
    db.create_all()
    return app


@babel.localeselector
def get_locale():
    """Get default language function returns systems default in config."""
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])
