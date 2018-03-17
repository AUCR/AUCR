"""The AUCR FLASK APP."""
# coding=utf-8
import logging
from app import aucr_app, db
from app.plugins.main import cli
from app.plugins.auth.models import User, Message, Notification, Task
from app import YamlInfo
app = aucr_app()
cli.register(app)
logging.info("Getting Project Info")
run = YamlInfo("projectinfo.yml", "strip", "LICENSE")
project_data = run.get()
project_info_data = project_data["info"]
project_version_data = project_data["version"]
# Nice Formatting Suggestion from iofault
__version__ = "%(major)s.%(minor)s.%(revision)s" % project_version_data
for items in project_info_data:
    logging.info(str(items) + ":" + str(project_info_data[items]))
logging.info(__version__)


@app.shell_context_processor
def make_shell_context():
    """Main flask app running service for production use."""
    return {'db': db, 'User': User, 'Message': Message, 'Notification': Notification, 'Task': Task}
