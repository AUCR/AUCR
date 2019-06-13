#!/bin/sh
# this script is used to boot a Docker container
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
    flask translate init en
    flask translate pybabel-compile
done
exec gunicorn -b :5000 -w 4 --access-logfile - --error-logfile - aucr:app