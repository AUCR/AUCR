# AUCR Project main drivers Please note this support python 3 only and I have zero intention of supporting python 2
import os
import sys
from flask import Flask
import yaml
from sqlalchemy.engine.url import make_url
from sqlalchemy_utils import database_exists, create_database
from jinja2 import FileSystemLoader
from jinja2.sandbox import SandboxedEnvironment


# This is based of a template from CTFd
class AUCRFlask(Flask):
    def __init__(self, *args, **kwargs):
        """Overriden Jinja constructor setting a custom jinja_environment"""
        self.jinja_environment = SandboxedBaseEnvironment
        Flask.__init__(self, *args, **kwargs)

    def create_jinja_environment(self):
        """Overridden jinja environment constructor"""
        return super(AUCRFlask, self).create_jinja_environment()


# This is based of a template from CTFd
class SandboxedBaseEnvironment(SandboxedEnvironment):
    """SandboxEnvironment that mimics the Flask BaseEnvironment"""
    def __init__(self, app, **options):
        if 'loader' not in options:
            options['loader'] = app.create_global_jinja_loader()
        SandboxedEnvironment.__init__(self, **options)
        self.app = app


class ThemeLoader(FileSystemLoader):
    """Custom FileSystemLoader that switches themes based on the configuration value"""
    def __init__(self, searchpath, encoding='utf-8', followlinks=False):
        super(ThemeLoader, self).__init__(searchpath, encoding, followlinks)
        self.overriden_templates = {}

    def get_source(self, environment, template):
        # Check if the template has been overriden
        if template in self.overriden_templates:
            return self.overriden_templates[template], template, True

        # Check if the template requested is for the admin panel
        if template.startswith('config/'):
            template = template[6:]  # Strip out admin/
            template = "/".join(['config', 'templates', template])
            return super(ThemeLoader, self).get_source(environment, template)

        # Load regular theme data
        theme = utils.get_config('user_theme')
        template = "/".join([theme, 'user_theme_templates', template])
        return super(ThemeLoader, self).get_source(environment, template)


class AUCR:
    def __init__(self):
        """Start and load config things"""
        with open("config.yml", 'rb') as config_file:
            read_config_file = config_file.read()
        self.project_info = yaml.load(read_config_file)

    @staticmethod
    def create_app():
        """Start the application AUCR"""

