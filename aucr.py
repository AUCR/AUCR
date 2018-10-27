"""The AUCR FLASK APP."""
# coding=utf-8
from aucr_app import aucr_app, db
from aucr_app.plugins.auth.models import User, Message, Notification, Task

app = aucr_app()


@app.shell_context_processor
def make_shell_context():
    """Main flask app running service for production use."""
    return {'db': db, 'User': User, 'Message': Message, 'Notification': Notification, 'Task': Task}
