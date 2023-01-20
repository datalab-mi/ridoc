#!/bin/bash
export FLASK_APP=wsgi
export FLASK_DEBUG=$1
FLASK_DEBUG=${FLASK_DEBUG:=1}
export APP_CONFIG_FILE=config.py
echo "$FLASK_DEBUG"
flask run --host "0.0.0.0"
