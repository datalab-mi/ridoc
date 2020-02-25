"""
                                                                        Interface Utilisateur 
"""
import dash
import dash_core_components as dcc
import dash_html_components as html 
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State, ClientsideFunction  
import base64
from elastic import request, corriger
import urllib.request
import os
from os import environ
from dotenv import load_dotenv
load_dotenv()
import sys
sys.path.append('..//')
from flask import send_from_directory
import logging
import flask
from logging.handlers import RotatingFileHandler

#-----------------------------------------------------------

#Variables d'environement
home = os.getenv('HOME')
#  L'adresse des fichiers Odt
Odt_Files_Directory = home + environ.get('Odt_Files_Directory')
#  Nom de l'index dans lequel on fait la recherhce
nom_index = environ.get('Nom_index')
#  Nom de l'index dans lequel on cherche les proposition de correction
nom_index_prop = environ.get('Nom_index_prop')
#  Chemin d'enregistrement des logs
Log_path_user = home + environ.get('Log_path_user')
Log_path_recherche_user = home + environ.get('Log_path_recherche_user')
#  Chemin pour les seuils
Chemin_seuil = home + environ.get('seuil')
Chemin_seuil_affichage = home + environ.get('seuil_affichage')
#  Chemin pour les pièces jointes
Chemin_PiecesJointes = home + environ.get('PiecesJointes')

#-----------------------------------------------------------

            #Construction des loggers
#Construction d'un logger admin
logging.basicConfig(filename=Log_path_user ,level=logging.INFO , format=u'%(asctime)s %(levelname)s:%(message)s')
#Contruction d'un logger recherche
logger = logging.getLogger('My_New_Logger')
logger.setLevel(logging.INFO)
#création d'un formateur qui va ajouter le temps, le niveau
# de chaque message quand on écrira un message dans le log
formatter = logging.Formatter(u'%(asctime)s :: %(levelname)s :: %(message)s')
#Création de notre Handler
file_handler = RotatingFileHandler(Log_path_recherche_user, 'a', 10000, backupCount=10 , encoding = 'utf-8')
file_handler.setLevel(logging.DEBUG)    
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
#------------------------------------------

external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/mdbootstrap/4.8.10/css/mdb.min.css',
 'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.3.1/css/bootstrap.min.css',
 'https://use.fontawesome.com/releases/v5.8.2/css/all.css']

 #--------------------------------------------------------------------
app = dash.Dash(__name__,
                requests_pathname_prefix = '/user/',
                external_stylesheets=external_stylesheets)
app.server.secret_key = 'Test'

#-----------------------------------------------------------------------

#Notre Front
app.layout = html.Div(
    [

        html.Div(
            [
                html.H2("e-consult@tions"),
                html.Img(src='static/images/IGPN.png'),
               # html.Form([
                        dcc.Textarea(
                            id='input-box_user',
                            placeholder='Ecrivez votre requête ici ...',
                            value='',
                            className = 'form-control form-control-sm mr-3 w-75'
                        ) , 
                        html.Button(id='button_user' , className = "fas fa-search")
                      #  ], action='/user/request', method='GET')
            ],
            className = "navbar navbar-expand-lg navbar-light bg-light"
        ),html.Div(
                    id = 'Affichage_proposition_user'
                ),
        html.Div(
            id = 'Affichage_resultat_user'
        )
    ], className="p-3 mb-2 bg-light text-dark")

#-----------------------------------------------------------


@app.server.route('/request' , methods = ['GET'])
def run():
    return ('' , 204)
    
#Les Callbacks
@app.callback(
    Output('Affichage_resultat_user' , 'children'),
    [Input('button_user', 'n_clicks')],
    [State('input-box_user', 'value')]
    )
def afficher_resultat_recherche(n_clicks, value):
    """
    Callback pour afficher les résultats de la requête
    Prend en argument:
        value: la valeur de la requête
        n_clicks : Le clique de l'utilisateur sur le boutton rechercher
    """

    if n_clicks is None:
        #On ne fait rien si l'utilisateur ne clique pas
        raise PreventUpdate

    file = open(Chemin_seuil , 'r' , encoding = 'utf-8')
    seuil = float(file.read())
    file.close()

    file = open(Chemin_seuil_affichage , 'r' , encoding = 'utf-8')
    seuil_affichage = float(file.read())
    file.close()

    #On ecrit dans notre Log
    #logger.info('Requête de l\'utilisateur ::  %s On vient de rechercher: %s',str(flask.session['uid']),str(value))
    #On fait notre requête
    D , lenght  = request(value , str(nom_index))
    
    Titres = []
    Ids = []
    Questions = []
    Scores = []
    Titres = []
    Réponses = []
    References = []
    div = []
    
    n = len(D)

    #On remplie la liste des résultats
    Dict_piece_jointe = {" ".join(x.split('.')[:-1]).lower() : x for x in os.listdir(Chemin_PiecesJointes)}

    for i in range(n):
        Titres.append(D[i]['_source']['TITRE'])
        Ids.append(D[i]['_id'])
        Questions.append(D[i]['_source']['Question'])
        if lenght != 0:
            score_int=D[i]['_score']/lenght
            Scores.append(round(score_int,1))
        else : 
            Scores.append(0)
        refs = str(D[i]['_source']['Pièces jointes'][0])
        refs = refs.split('\n')
        refs = list(map(lambda x: x.strip() , refs))
        if "Néant" in refs:
            refs.remove('Néant')
        try:
            refs.remove('')
            refs.remove('Néant')
        except:
            pass
        reference = ''
        for ref in refs:
            if ref[0] == '-':
                ref = ref[1:].strip()
            if ref[:2] == "cf":
                ref = ref[2:].strip()
            if ref.lower() in Dict_piece_jointe.keys():
                ref_link = Dict_piece_jointe[ref.lower()].replace(' ' , "%20")
                reference += '- ' + '[' + ref +'] (/references/' + ref_link  +')' + "\n"
            else:
                reference += '- ' + ref + "\n"

        References.append(reference)
        try:
            Réponses.append(D[i]['highlight']['Réponse'])
        except:
            Réponses.append([])
    
    # if Bande:
    #     div.append(html.Div([dcc.Markdown('''
    #                         ### En première approche, votre question ne semble pas répondre à un document particulier nous vous recommandons de contacter [igpn-cadre@interieur.gouv.fr] (mailto://igpn-cadre@interieur.gouv.fr?subject=Demande_de_consultation), vous pouvez toutefois regarder les documents ci-dessous
    #                         ''' , style = {"color" : "red" , "text-align" : "center"})],style = {"border-width" : "medium" , "border": "solid red"}))
    
    #On ecrit les résultats de recherche
    Bande = False 

    for j in range (len(Titres)):
        if Scores[j] < seuil_affichage:
            break
        if Scores[j] < seuil and Bande == False:
            div.append(html.Div([dcc.Markdown('''
                                    ### Le document que vous recherchez a peu de chance de se trouver en dessous de cette bande.''' ,style = {"color" : "red" , "text-align" : "center"})],style = {"border-width" : "thin" , "border": "solid red"}))
            Bande = True

        q ="`Question` : " + str(Questions[j][0])+"\n"
        q += "\n`Réponse` :"
        for relevent_sentence in Réponses[j]:
            q += str(relevent_sentence) + r'\[...\]'
        q += "\n \n`Pièces jointes`: \n\n"+str(References[j])
        q = q.replace('</em><em>' , '')
        q = q.replace('<em>' , '`')
        q = q.replace('</em>' , '`')
        div.append(html.Div([html.A(Titres[j][0], href = '/Documents_user/' +str(j) +'/'+ str(Ids[j])  , style = {"font-size" : "1.5em" , "font-weight" : "bold"}),
        dcc.Markdown(q)] , style = {"border-width" : "1px 1px" , "border-bottom": "solid purple"}))     
    if (len(div) == 0):
        div.append(html.Div([dcc.Markdown('''
                                    ## Aucun résultat ''' ,style = {"color" : "red" , "text-align" : "center" , "border-width" : "thin" , "border": "solid red" })], className="border border-primary", style = { "position" : "absolute" , "top" : "500px"  , "left" : "300px"}))
    return div
@app.callback(Output('Affichage_proposition_user' , 'children'),
    [Input('button_user', 'n_clicks')],
    [State('input-box_user', 'value')]
)
def afficher_propositions(n_clicks, value):
    """
    Callback pour afficher les suggestions de correction de faute d'orthographe à l'utilisateur:
        Input:
            n_clicks: Le click de l'utilisateur sur le bouton rechercher
            value: La valeur de la requête
        Output:
            Les suggestions de correction de faute d'orthographe
    """
    if n_clicks is None:
        raise PreventUpdate
    L = corriger(value , nom_index_prop)
    if len(L)>=1:
        div = []
        div.append(html.H1('Propositions de correction:'))
        div.append(html.H3('Veuillez copier puis rechercher la suggestion qui vous semble pertinente'))
        for i in range (len(L)):
            div.append(html.Div(L[i]))
        return div
    else:
        return
