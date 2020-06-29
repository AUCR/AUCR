"""Get config information or set defaults."""
# coding=utf-8
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    """Set environment variables based on config."""

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'aucr.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = os.environ.get('SQLALCHEMY_POOL_SIZE') or 20
    SQLALCHEMY_MAX_OVERFLOW = os.environ.get('SQLALCHEMY_MAX_OVERFLOW') or 40
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    SERVER_NAME = os.environ.get('SERVER_NAME')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = os.environ.get("ADMIN_EMAILS") or ['admin@aucr.io']
    LANGUAGES = ['en']
    MAX_CONTENT_LENGTH = os.environ.get('MAX_CONTENT_LENGTH') or 2048 * 2048 * 2048
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    FILE_FOLDER = os.environ.get('FILE_FOLDER') or os.path.join(basedir, 'upload')
    TMP_FILE_FOLDER = os.environ.get('TMP_FILE_FOLDER') or os.path.join(basedir, '/tmp/')
    OBJECT_STORAGE = os.environ.get('OBJECT_STORAGE') or None
    OBJECT_STORAGE_TYPE = os.environ.get('OBJECT_STORAGE_TYPE') or None
    ALLOWED_EXTENSIONS = os.environ.get('ALLOWED_EXTENSIONS') or ['txt', 'pdf', 'png', 'jpg',
                                                                  'jpeg', 'gif', 'doc', 'docx', 'exe', 'yar', 'zip', '']
    POSTS_PER_PAGE = os.environ.get('POSTS_PER_PAGE') or 25
    SQLALCHEMY_POOL_TIMEOUT = os.environ.get('SQLALCHEMY_POOL_TIMEOUT') or None
    ALLOWED_EMAIL_LIST = (os.environ.get("ALLOWED_EMAIL_LIST") or "*").split(', ')
    LDAP_PROVIDER_URL = os.environ.get("LDAP_PROVIDER_URL") or None
    LDAP_PROTOCOL_VERSION = os.environ.get("LDAP_PROTOCOL_VERSION") or None
    LDAP_CONNECTION_STRING = os.environ.get("LDAP_CONNECTION_STRING") or None
    LDAP_BASE = os.environ.get("LDAP_BASE") or 3
    LDAP_CERTIFICATE = os.environ.get("LDAP_CERTIFICATE") or None
    LDAP_ADMIN = os.environ.get("LDAP_ADMIN") or None
    LDAP_ADMIN_PASSWORD = os.environ.get("LDAP_ADMIN_PASSWORD") or None
    APP_TITLE = os.environ.get('APP_TITLE') or "Analyst Unknown Cyber Range"
    MONGO_URI = os.environ.get('MONGO_URI') or None
    PRIVACY_POLICY_URL = os.environ.get('PRIVACY_POLICY_URL') or None
    RABBITMQ_SERVER = os.environ.get('RABBITMQ_SERVER') or 'localhost'
    RABBITMQ_PORT = os.environ.get('RABBITMQ_PORT') or '5672'
    RABBITMQ_USERNAME = os.environ.get('RABBITMQ_USERNAME') or 'guest'
    RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD') or 'guest'
    RABBITMQ_URL = "amqp://{username}:{password}@{host}:{port}".format(
                    username=RABBITMQ_USERNAME,
                    password=RABBITMQ_PASSWORD,
                    host=RABBITMQ_SERVER,
                    port=RABBITMQ_PORT)
