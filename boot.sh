#!/usr/bin/env bash
# this script is used to boot a docker container
source ~/.virtualenvs/flask-microblog-M17gQHIP/bin/activate
while true; do
    flask db upgrade
    if [["$?" == "0]]; then
        break
    fi
    echo Deploy command failed. Retrying in 5 seconds...
    sleep 5
done
exec gunicorn -b :5000 --access-logfile - --error-logfile - microblog:app
