"""Python AUCR development debugging framework for use from an IDE like pycharm. NOT FOR PRODUCTION."""
# coding=utf-8
import logging
from app import aucr_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = aucr_app()
app.run(debug=True, threaded=True, host="127.0.0.1", port=8080)
