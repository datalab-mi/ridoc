export FLASK_APP=wsgi.py
export FLASK_DEBUG=1
export APP_CONFIG_FILE=config.py
flask run --host "0.0.0.0"
#python3 -m http.server --bind 0.0.0.0 wsgi.py
