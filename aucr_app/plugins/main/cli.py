"""Command line interface to manage AUCR build tasks."""
# coding=utf-8
import os
import click


def register(app):
    """App flask register app blueprint get's our flask app and provides the cli some functions."""
    @app.cli.group()
    def translate():
        """Translation and localization commands."""
        pass

    @translate.command()
    @click.argument('lang')
    def init(lang):
        """Initialize a new language."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system('pybabel init -i messages.pot -d aucr_app/translations -l ' + lang):
            raise RuntimeError('init command failed')
        os.remove('messages.pot')

    @translate.command()
    def update():
        """Update all languages."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system('pybabel update -i messages.pot -d aucr_app/translations'):
            raise RuntimeError('update command failed')
        os.remove('messages.pot')

    @translate.command()
    def pybabel_compile():
        """Compile all languages."""
        if os.system('pybabel compile -d aucr_app/translations'):
            raise RuntimeError('compile command failed')
