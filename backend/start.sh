#!/bin/bash
export FLASK_APP=wsgi
export FLASK_ENV=$1
FLASK_ENV=${FLASK_ENV:=development}
export APP_CONFIG_FILE=config.py
echo "$FLASK_ENV"
flask run --host "0.0.0.0"
