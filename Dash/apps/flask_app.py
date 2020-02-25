from flask import Flask , send_from_directory, render_template, send_file
import flask
import os
from os import environ
import uuid
from dotenv import load_dotenv
from apps.app_user import logger as logger_user
from apps.app_admin import logger as logger_admin
load_dotenv()


home = os.getenv('HOME')
Odt_Files_Directory = home + environ.get('Odt_Files_Directory')
Chemin_message = home + environ.get('Message_accueil')
Chemin_titre_Message = home + environ.get('Titre_Message_accueil')
Chemin_PiecesJointes = home + environ.get('PiecesJointes')
Mode_emploi_file = home + environ.get('Mode_emploi')

app = Flask(__name__)
app.secret_key = 'Test'

@app.route('/')
def index():
    file = open(Chemin_message , 'r' , encoding = 'utf-8')
    Message = str(file.read())
    file.close()

    file = open(Chemin_titre_Message , 'r' , encoding = 'utf-8')
    Titre_Message = str(file.read())
    file.close()

    Message = Message.replace('\n' , '<br>')
    flask.session['uid'] = uuid.uuid4()
    return render_template("index.html" , Message = Message , Titre_Message = Titre_Message)

@app.route("/Documents_user/<path:path>")
def download_user(path):
    """Fonction qui permet de télécharger les documents choisis par l'utilisateur et prend comme argument:
            path: le path sous la forme suivante <classement/Nome_du_document>"""
    logger_user.info('Choix de l\'utilisateur :: L\'utilisateur {0} a choisi le choix {1}'.format(str(flask.session['uid']), str(path.split('/')[0])))
    return send_from_directory(Odt_Files_Directory, path.split('/')[1] , as_attachment=True)

@app.route("/Satisfaction_user/<path:path>")
def collect_user_satisfaction(path):
    """Fonction qui permet de télécharger les documents choisis par l'utilisateur et prend comme argument:
            path: le path sous la forme suivante <classement/Nome_du_document>"""
    logger_user.info('Satisfaction de l\'utilisateur :: L\'utilisateur {0}, pour la requête {1}, a apprécié le document {2} qui était classé {3}'.format(str(flask.session['uid']), str(path.split('/')[0]) , str(path.split('/')[2]) , str(path.split('/')[1])))
    return ('', 204)

@app.route("/Documents/<path:path>")
def download(path):
    """Fonction qui permet de télécharger les documents choisis par l'utilisateur et prend comme argument:
            path: le path sous la forme suivante <classement/Nome_du_document>"""
    logger_admin.info('Choix de l\'utilisateur :: L\'utilisateur {0} a choisi le choix {1}'.format(str(flask.session['uid']), str(path.split('/')[0])))
    return send_from_directory(Odt_Files_Directory, path.split('/')[1] , as_attachment=True)

@app.route("/references/<path:path>")
def download_ref(path):
    """Fonction qui permet de télécharger les documents choisis par l'utilisateur et prend comme argument:
            path: le path sous la forme suivante <classement/Nome_du_document>"""
    return send_from_directory(Chemin_PiecesJointes , path.split('/')[0] , as_attachment=True)
@app.route("/Satisfaction/<path:path>")
def collect_admin_satisfaction(path):
    """Fonction qui permet de télécharger les documents choisis par l'utilisateur et prend comme argument:
            path: le path sous la forme suivante <classement/Nome_du_document>"""
    logger_admin.info('Satisfaction de l\'utilisateur :: L\'utilisateur {0}, pour la requête {1}, a apprécié le document {2} qui était classé {3}'.format(str(flask.session['uid']), str(path.split('/')[0]) , str(path.split('/')[2]) , str(path.split('/')[1])))
    return ('', 204)
@app.route("/aide")
def download_mode_emploi():
    """Fonction qui permet de télécharger le mode d'emploi par l'utilisateur et prend comme argument:
            path: le path sous la forme suivante <classement/Nome_du_document>"""
    return send_file(Mode_emploi_file , as_attachment=True)    
# if __name__ == "__main__":
#     app.run("0.0.0.0" , "2000")
