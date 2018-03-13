web: flask db upgrade; flask translate compile; gunicorn aucr:app
worker: rq worker aucr-tasks
