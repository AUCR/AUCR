"""The AUCR FLASK APP."""
# coding=utf-8
from aucr_app import aucr_app, db
from aucr_app.plugins.auth.models import User, Message, Notification, Task

app = aucr_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
