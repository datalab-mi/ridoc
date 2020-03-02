"""
                On lance le serveur Elasticsearch
"""


import dash
import dash_auth
import os
from os import environ
from dotenv import load_dotenv
load_dotenv()
import logging
import flask
import uuid
from flask import send_from_directory
from logging.handlers import RotatingFileHandler

#%%
#Les variables d'environement
home = os.getenv("HOME")
Log_path = home + environ.get('Log_path')
Log_path_recherche= home + environ.get('Log_path_recherche')
Odt_Files_Directory = home + environ.get('Odt_Files_Directory')
#%%
            #Construction des loggers
#Construction d'un logger admin
logging.basicConfig(filename=Log_path ,level=logging.INFO , format=u'%(asctime)s %(levelname)s:%(message)s')
#Contruction d'un logger recherche
logger = logging.getLogger('My_New_Logger')
logger.setLevel(logging.INFO)
#création d'un formateur qui va ajouter le temps, le niveau
# de chaque message quand on écrira un message dans le log
formatter = logging.Formatter(u'%(asctime)s :: %(levelname)s :: %(message)s')
#Création de notre Handler
file_handler = RotatingFileHandler(Log_path_recherche, 'a', 10000, backupCount=10 , encoding = 'utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
#%%
#Les CSS utilisé dans le Dash
external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/mdbootstrap/4.8.10/css/mdb.min.css',
 'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.3.1/css/bootstrap.min.css',
 'https://use.fontawesome.com/releases/v5.8.2/css/all.css' , "/assets/asset.css"]
#%%
#Le Serveur Flask 
server = flask.Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.server.secret_key = 'Test'
#%%
#Authentification
VALID_USERNAME_PASSWORD_PAIRS = {
    environ.get('Admin_Username'): environ.get('Admin_Password'),
   environ.get('User_Usernamen'): environ.get('User_Password')
}
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
app.config.suppress_callback_exceptions = True
