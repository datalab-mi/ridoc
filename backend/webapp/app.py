import sys
import json
from os import environ
from flask import Flask, Response, send_from_directory, request, abort

sys.path.append('./tools')
from elastic import simple_request

#  Nom de l'index dans lequel on fait la recherhce
nom_index = environ.get('Nom_index')
Dash_host = environ.get('Dash_host')
Dash_port = environ.get('BACKEND_PORT')

app = Flask(__name__)

@app.route('/api/v1/request')
def api_request():
    d = simple_request(nom_index)
    return json.dumps(d)

@app.route('/api/v1/healthcheck')
def healthcheck():
    return json.dumps({"status": "ok"})

if __name__ == '__main__':
    app.run(
            host=Dash_host,
            debug=True,
            threaded=True,
            port=int(Dash_port)
            )
