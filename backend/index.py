"""
                                                    Index permettant de rediriger les utilisateurs suivant leur username
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from os.path import expanduser
import sys
import os
from os import environ
from dotenv import load_dotenv
load_dotenv()
home = environ.get('app_directory')
sys.path.append(str(home) + "apps\\")
from app import app
from apps import app_admin, app_user
from flask import request
import flask
import uuid
#%%
#Variables d'environement
home = os.getenv('HOME')
Odt_Files_Directory = home + environ.get('Odt_Files_Directory')

Dash_host = environ.get('Dash_host')
Dash_port = environ.get('Dash_port')

#%%
#Front-end
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
#%%
#Callaback pour repérerer les usernames
@app.callback(Output('page-content', 'children') , 
            [Input('url' , 'pathname')])
def display_page(pathname):
    """
        Fonction qui retourne la page correspondante en fonction du nom d'utilisateur
    """
    flask.session['uid'] = uuid.uuid4()
    username = request.authorization['username']
    if username == 'Admin':
        if pathname == '/apps/app_admin':
            return app_admin.layout
        elif pathname == '/apps/app_user':
            return app_user.layout
        else:
            return app_admin.layout
    else:
        if pathname == '/apps/app_admin':
            return app_user.layout
        elif pathname == '/apps/app_user':
            return app_user.layout
        else:
            return app_user.layout
if __name__=="__main__":
    app.run_server(host=Dash_host , debug=True, port=Dash_port)