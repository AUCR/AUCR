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
exec uwsgi --http :5000 --enable-threads --plugin python38  --module aucr:app --processes 2 --threads 4
