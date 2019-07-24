"""The AUCR FLASK APP."""
# coding=utf-8
from aucr_app import aucr_app
from aucr_app.plugins.main import cli

app = aucr_app()
cli.register(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0")

