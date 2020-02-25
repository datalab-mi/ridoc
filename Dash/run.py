from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple

from apps.app_admin import app as app_admin
from apps.app_user import app as app_user
from apps.flask_app import app as flask_app

from os import environ
from dotenv import load_dotenv
load_dotenv()

Dash_host = environ.get('Dash_host')
Dash_port = environ.get('Dash_port')

application = DispatcherMiddleware(flask_app, {
    '/admin': app_admin.server,
    '/user': app_user.server,
})

if __name__ == '__main__':
    run_simple(Dash_host, int(Dash_port), application , use_reloader = False , use_debugger = True)  