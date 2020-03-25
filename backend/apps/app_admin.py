"""
Interface Admin
"""
import dash
import dash_auth
import os
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State, ClientsideFunction
import base64
from elastic import request, upload_docs, add_syn, changement_structure
from elastic import corriger, changement_structure_expression, add_expression
from dash.exceptions import PreventUpdate
from os import environ
from dotenv import load_dotenv
from datetime import datetime
import time
import dash_bootstrap_components as dbc
import logging
from logging.handlers import RotatingFileHandler
import sys
import flask
from flask import send_from_directory
sys.path.append('..//')
load_dotenv()


# Variables d'environement
#home = os.getenv('HOME')
home = os.getcwd()
#  Chemin d'enregistrement des logs
Log_path_admin = home + environ.get('Log_path_admin')
Log_path_recherche_admin = home + environ.get('Log_path_recherche_admin')
#  Chemin d'enregistrement du message d'accueil
Chemin_message = home + environ.get('Message_accueil')
Chemin_titre_Message = home + environ.get('Titre_Message_accueil')
#  Chemin pour les seuils
Chemin_seuil = home + environ.get('seuil')
Chemin_seuil_affichage = home + environ.get('seuil_affichage')
#  Chemin pour les pièces jointes
Chemin_PiecesJointes = home + environ.get('PiecesJointes')
#  Chemin des mots clefs avec un seul mot affiché à l'utilisateur
Chemin_one_word_keyword = home + environ.get('One_word_keyword_non_analyzed')
#  Chemin des mots clefs avec un seul mot affiché à l'utilisateur (temporaire)
Chemin_one_word_keyword_enregistre = home + environ.get('One_word_keyword_non_analyzed_enregistre')
# L'adresse du fichier glossaire des acronymes (celui qui est utilisé dans l'indexation)
Chemin_Glossaire = home + environ.get('Chemin_Glossaire')
#  L'adresse du ficher glossaire des acronymes temporaire
Chemin_Glossaire_enregistre = home + environ.get('Chemin_Glossaire_enregistre')
#  L'adresse du Mapping
Mapping_Directory = home + environ.get('Mapping_Directory')
#  L'adresse des fichiers Json
JSON_FILES_DIRECTORY = home + environ.get('JSON_FILES_DIRECTORY')
#  L'adresse des fichiers Odt
Odt_Files_Directory = home + environ.get('Odt_Files_Directory')
#  Nom de l'index dans lequel on fait la recherhce
nom_index = environ.get('Nom_index')
#  Nom de l'index dans lequel on cherche les proposition de correction
nom_index_prop = environ.get('Nom_index_prop')
#  L'adresse d'elasticsearch avec le port
elastic_host = environ.get('Elastic_host')
elastic_port = environ.get('Elastic_port')
#  L'adresse de la liste des expressions clés analysées
path_list_expression_metier = home + environ.get('Path_list_expression_metier')
#  L'adresse de la liste des expressions clés sous la forme (expression => EXPRESSION, expression_analysée)
Chemin_list_expression = home + environ.get('Chemin_list_expression')
#  L'adresse de la liste des expressions clés (temporaire) sous la forme (expression => EXPRESSION, expression_analysée)
Chemin_list_expression_enregistre = home + environ.get('Chemin_list_expression_enregistre')
#  L'adresse de la liste d'expression affiché à l'utilisateur
Chemin_expression = home + environ.get('Chemin_expression')
#  L'adresse de la liste d'expression (temporaire) affiché à l'utilisateur
Chemin_expression_enregistre = home + environ.get('Chemin_expression_enregistre')

# -----------------------------------------------------
# Le Logging

# Construction des loggers

# Construction d'un logger admin
logging.basicConfig(filename=Log_path_admin, level=logging.INFO,
                    format=u'%(asctime)s %(levelname)s:%(message)s')
# Contruction d'un logger recherche
logger = logging.getLogger('My_New_Logger')
logger.setLevel(logging.INFO)
# Création d'un formateur qui va ajouter le temps, le niveau
# de chaque message quand on écrira un message dans le log
formatter = logging.Formatter(u'%(asctime)s :: %(levelname)s :: %(message)s')
# Création de notre Handler
file_handler = RotatingFileHandler(Log_path_recherche_admin, 'a',
                                   10000, backupCount=10, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
# -----------------------------------------------------
# Les CSS utilisés dans le Dash
external_stylesheets = [
    'https://cdnjs.cloudflare.com/ajax/libs/mdbootstrap/4.8.10/css/mdb.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.3.1/css/bootstrap.min.css',
    'https://use.fontawesome.com/releases/v5.8.2/css/all.css',
    "/static/css/style_apps.css"
    ]

# -----------------------------------------------------
# L'application Dash
app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                requests_pathname_prefix='/admin/')
app.server.secret_key = 'Test'
# -----------------------------------------------------
# Dictionnaire des usernames & passwords
VALID_USERNAME_PASSWORD_PAIRS = {
    environ.get('Admin_Username'): environ.get('Admin_Password'),
    environ.get('User_Usernamen'): environ.get('User_Password')
}
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
# ----------------------------------------------------------------------------------------------------------------------------------------------
# Le Front

s = 0       # s est une variable globale pour la barre de progression
app.layout = html.Div(
    [
        html.Div(id='none', children=[], style={'display': 'none'}),
        dcc.Tabs(id='tabs', value='Moteur de recherche', children=[

             dcc.Tab(label="Moteur de recherche", value='Moteur de recherche', children=[
                html.Div([
                    html.Img(src='static/images/IGPN.png'),
                    html.H3("e-consult@tions", style={"font-size": "medium"}),
                            dcc.Textarea(id='input-box',
                                      placeholder='Ecrivez votre requête ici ...',
                                      value='',
                                      className = 'form-control form-control-sm mr-3 w-75'
                                      ),
                    html.Button(id='button', className="fas fa-search")
			], className="navbar navbar-expand-lg navbar-light bg-light"),
                html.Div(
                    id='Affichage_proposition'
                ),
                html.Div(
                    id='Affichage_resultat'
                )
            ]),

             dcc.Tab(label="Changer le glossaire des acronymes", value="Changer le glossaire des acronymes",
                    children=[
                            html.Div(id="Ajouter-des-acronymes", children=[
                                html.H1("Ajout des acronymes"),
                                html.Div([html.Div([dcc.Input(
                                                            id='input-acronyme',
                                                            placeholder='Entrez le nouvel acronyme',
                                                            value='',
                                                            className='form-control form-control-sm mr-3 w-75'
                                                            )
                                                    ] , className='col'),
                                        html.Div([dcc.Input(
                                                            id='input-meaning',
                                                            placeholder='Entrez la signification correspondante',
                                                            value='',
                                                            className='form-control form-control-sm mr-3 w-75'
                                                            )
                                                    ], className='col'),
                                        html.Div([html.Button('Ajouter', id='add_synonyme', className="btn btn-primary")
                                                    ], className="col")
                                        ], className='row')
                                                                            ]
                                     ),
                            html.Div(id='Ajout_synonyme'),
                            html.Div(id="Report_changes", style={"color" : "red"}),
                            html.Div(id="Changement-glossaire", children=[
                                html.H1('Modification du glossaire d\'acronyme'),
                                html.H4('Veuillez respecter le format dans le corps du fichier ci-dessous'),
                                html.Div(id='Reindex_div'),
                                dcc.Textarea(id='Affichage_synonyme', value="", style={
                                                                                            'width': '100%',
                                                                                            'height': '550px',
                                                                                            'lineHeight': '60px',
                                                                                            'borderWidth': '1px',
                                                                                            'borderStyle': 'dashed',
                                                                                            'borderRadius': '5px',
                                                                                            'textAlign': 'center',
                                                                                            'margin': '10px'
                                                                                            }
                                             ),
                                html.Div(id='Vide')
                                                                                ]
                                     ),
                            html.Div(id="sauvegarder_et_appliquer", children=[
                                html.Button('Sauvegarder', id='effectuer_changes', className="btn btn-primary"),
                                html.Button('Appliquer', id='reindex_changes', className="btn btn-success" )
                                                                                ]
                                    )
                             ], className="p-3 mb-2 bg-light text-dark"),


             dcc.Tab(label="Changer les expressions clés", value="Changer les expressions clés",
                     children=[
                            html.Div(id="Ajouter_expression", children=[
                                html.H1("Ajout des expressions"),
                                html.Div([html.Div([dcc.Input(
                                                            id='input_expression',
                                                            placeholder='Entrez l\'expression clé',
                                                            value='',
                                                            className='form-control form-control-sm mr-3 w-75'
                                                            )
                                                    ], className='col'),
                                html.Div([html.Button('Ajouter', id='add_expression', className="btn btn-primary")], className="col")
                                         ], className='row')
                                ]
                                ),
                            html.Div(id='Ajout_expression'),
                            html.Div(id="Report_changes_expression", style={"color": "red"}),
                            html.Div(id="Changement-glossaire-expressions", children=[
                                html.H1('Modification de la liste des expressions clés'),
                                html.H4('Veuillez respecter le format dans le corps du fichier ci-dessous'),
                                html.Div(id='Reindex_div_expression'),
                                dcc.Textarea(id='Affichage_expressions', value="", style={
                                                                                            'width': '100%',
                                                                                            'height': '550px',
                                                                                            'lineHeight': '60px',
                                                                                            'borderWidth': '1px',
                                                                                            'borderStyle': 'dashed',
                                                                                            'borderRadius': '5px',
                                                                                            'textAlign': 'center',
                                                                                            'margin': '10px'
                                                                                            }
                                             ),
                                html.Div(id='Vide_expression')
                                ]
                                ),
                            html.Div(id="sauvegarder_et_appliquer_expression", children=[
                                html.Button('Sauvegarder', id='effectuer_changes_expression', className="btn btn-primary"),
                                html.Button('Appliquer', id='reindex_changes_expression', className="btn btn-success" )
                                ]
                                )
                        ], className="p-3 mb-2 bg-light text-dark"),

             dcc.Tab(label="Mise à jour des documents", value="Mise à jour documents", children=[
                html.Div(id="Chargement-rapport", children=[
                    html.H1('Chargement d\'une nouvelle consultation'),
                    dcc.Upload(id='upload-data', children=
                        html.Div([
                            html.Button('Télécharger les nouvelles consultations', className="btn btn-primary", style={'width': '80%'})
                            ],
                            style={
                                'width': '100%',
                                'height': '60px',
                                'textAlign': 'center'
                                }
                            ),
                        multiple=True
                        )
                     ]
                     ),
                html.Div([
                    dbc.Progress(id="progress", value=0, striped=True, animated=True),
                    dcc.Interval(id="interval", interval=250, n_intervals=0),
                    ]
                    ),
                html.Div(id='output-data-upload'),
                html.Div(id="Chargement-pj", children=[
                    html.H1('Chargement d\'une nouvelle pièce jointe'),
                    dcc.Upload(id='upload-pj',
                        children=html.Div([
                            html.Button('Télécharger les nouvelles pièces jointes', className="btn btn-primary", style={'width': '80%'})
                            ],
                            style={
                                'width': '100%',
                                'height': '60px',
                                'textAlign': 'center'
                                }
                            ), multiple=True
                        )
                    ]),
                html.Div(id='output-pj-upload'),
                html.Div(id="Supression-rapport", children=[
                    html.H1("Supression d'une consultation de la base documentaire"),
                    html.Div([
                            dcc.Markdown('''
                                            ### Supprimer des consultations
                                            '''),
                            dcc.Dropdown(id='select-data-to-del',
                                        multi=True)
                        ],
                        style={'margin-top': 30}) ,
                    html.Button('Supprimer', id='del-data', className="btn btn-primary")
                    ]),
                html.Div(id="Message_confiramtion_utilisateur_pj"),
                html.Div(id="Supression-pj", children=[
                    html.H1("Supression d'une pièce jointe de la base documentaire"),
                    html.Div([
                            dcc.Markdown('''
                                            ### Supprimer des pièces jointes
                                            '''),
                            dcc.Dropdown(id='select-pj-to-del',
                                            multi=True)
                        ],
                        style={'margin-top': 30}) ,
                        html.Button('Supprimer', id='del-pj', className="btn btn-primary")
                ]),
                html.Div(id="Message_confiramtion_utilisateur")
                ]),

             dcc.Tab(label="Paramètres généraux", value="Paramètres généraux", children=[
                html.Div(id="Changement-message-accueil", children=[
                        html.H1('Personnalisation de la page d\'accueil'),
                        html.H3('Modifiez le titre de votre message d\'accueil') ,
                        dcc.Input(id="Titre_Message_d'accueil", style={"width": "50%"}),
                        html.H3('Modifiez le corps de votre message d\'accueil') ,
                        dcc.Textarea(id="Message_d'accueil") ,
                        html.Button("Appliquer", id="Changement_message_accueil", className="btn btn-primary") ,
                        html.Div(id="confirmation_changement")
                        ]
                    ),
                html.H1('Mise à jour des seuils'),
                html.Div(id="Changement de seuil", className="row", children=[
                        html.Div([html.H4('Mise à jour du seuil de pertinence')], className="col") ,
                        html.Div([dcc.Input(id = "slider_seuil")], className="col"),
                        html.Div([html.Button('Appliquer', id='changement_seuil', className="btn btn-primary")], className="col") ,
                        html.Div([html.H3(id='slider-output-container')], className="col")
                     ]),
                html.Div(id="Changement de seuil_affichage", className="row", style = {'position': "relative", "top": "40px"},
                    children=[
                        html.Div([html.H4('Mise à jour du seuil d\'affichage')], className="col"),
                        html.Div([dcc.Input(id = "slider_seuil_affichage")], className="col"),
                        html.Div([html.Button('Appliquer', id='changement_seuil_affichage', className="btn btn-primary")], className="col"),
                        html.Div([
                            html.H3(id='slider-output-container_affichage')
                            ], className="col")
                        ]
                    )
        ])
    ])
])

#-------------------------------------------------------- Callbacks pour l'onglet moteur de recherche ---------------------------------
@app.callback(
    Output('Affichage_resultat' , 'children'),
    [Input('button', 'n_clicks')],
   [State('input-box', 'value')]
    )
def afficher_resultat_recherche(n_clicks ,  value):
    """
    Callback pour afficher les résultats de la requête
    Prend en argument:
        value: la valeur de la requête
        n_clicks : Le clique de l'utilisateur sur le boutton rechercher
    """
    if n_clicks is None:
        #On ne fait rien si l'utilisateur ne clique pas
        raise PreventUpdate

    #On importe l'information des deux seuils
    file = open(Chemin_seuil_affichage , 'r' , encoding = 'utf-8')
    seuil_affichage = float(file.read())
    file.close()
    file = open(Chemin_seuil , 'r' , encoding = 'utf-8')
    seuil = float(file.read())
    file.close()

    #On ecrit dans le Log de recherche
    logger.info('Requête de l\'utilisateur :: %sOn vient de rechercher: %s',str(flask.session['uid']),str(value))

    #On envoie la requête ElasticSearch
    D, lenght = request(value, str(nom_index))

    # On collecte les résultats
    # On initialise Les listes des résultats
    Titres = []
    Ids = []
    Questions = []
    Titres = []
    Réponses = []
    Scores = []
    References = []
    div = []
    n = len(D)
    Dict_piece_jointe = {" ".join(x.split('.')[:-1]).lower() : x for x in os.listdir(Chemin_PiecesJointes)}
    #On remplie les listes des résultats
    for i in range(n):
        Titres.append(D[i]['_source']['TITRE'])

        Ids.append(D[i]['_id'])

        Questions.append(D[i]['_source']['Question'])

        refs = str(D[i]['_source']['Pièces jointes'][0])
        refs = refs.split('\n')
        refs = list(map(lambda x: x.strip() , refs))
        if "Néant" in refs:
            refs.remove('Néant')
        try:
            refs.remove('')
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

        if lenght != 0:
            score_int=D[i]['_score']/lenght
            Scores.append(round(score_int,1))
        else :
            Scores.append(0)

    # On ecrit les résultats de recherche
    Bande = False  # Indique si la bande de pertinence a été affiché ou pas
    for j in range (len(Titres)):
        if Scores[j] < seuil_affichage:
            #Pour le seuil d'affichage
            break
        if Scores[j] < seuil and Bande == False:
            # Pour la bande
            div.append(html.Div([dcc.Markdown('''
                                    ### Le document que vous recherchez a peu de chance de se trouver en dessous de cette bande.''' ,style = {"color" : "red" , "text-align" : "center"})],style = {"border-width" : "thin" , "border": "solid red"}))
            Bande = True

        q = "`Score:" + str(Scores[j]) + "`" + "\n\n`Question` : " + str(Questions[j][0])+"\n"

        q += "\n`Réponse` :"
        for relevent_sentence in Réponses[j]:
            q += str(relevent_sentence) + r'\[...\] '

        q += "\n \n`Pièces jointes`: \n\n"+str(References[j])

        q = q.replace('</em><em>' , '')
        q = q.replace('<em>' , '`')
        q = q.replace('</em>' , '`')

        # Ajout de a réponse dans un Div
        div.append(html.Div([html.A(Titres[j][0], href = '/Documents/' +str(j) +'/'+ str(Ids[j]) , style = {"font-size" : "1.5em" , "font-weight" : "bold"}),
        dcc.Markdown(q)] , style = {"border-width" : "1px 1px" , "border-bottom": "solid purple"}))

    if (len(div) == 0):
        # Le cas ou aucun résultat n'est affiché
        div.append(html.Div([dcc.Markdown('''
                                    ## Aucun résultat''' ,style = {"color" : "red" , "text-align" : "center" })] , style = { "border": "solid red" , "position" : "absolute" , "top" : "500px"  , "left" : "300px" , "border-width" : "thick"}))
    return div
@app.callback(Output('Affichage_proposition' , 'children'),
    [Input('button', 'n_clicks')],
    [State('input-box', 'value')]
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
        div.append(html.H1('Propositions de correction : ' , style = {"color" : "red",
                                                        "font-size" :"medium"}))
        div.append(html.H3('Veuillez copier puis rechercher la suggestion qui vous semble pertinente'))
        for i in range (len(L)):
            div.append(html.Div(L[i]))
        return div
    else:
        return
#-------------------------------------------------------- Callbacks pour l'onglet "Changer le glossaire des acronymes" ---------------------------------
@app.callback(
    Output('Affichage_synonyme' , 'value'),
    [Input('add_synonyme' , 'n_clicks')]
    )
def affichage_acronyme(n_clicks1):
    """
    Callback pour mettre à jour les acronymes affichés
    Input:
        n_clicks1: Le clic de l'utilisatuer sur le bouton Ajouter.
    Output:
        Les acronymes affichés à l'utilisateur sont mis à jour
    """
    f = open(Chemin_Glossaire_enregistre , 'r', encoding="utf8")
    Liste_glossaire =f.read()
    f.close()

    Liste_glossaire = str(Liste_glossaire)
    Liste_glossaire = Liste_glossaire.split('\n')
    try:
        Liste_glossaire.remove('')
    except:
        pass
    Liste_glossaire.sort()
    Liste_glossaire = "\n".join(Liste_glossaire)
    return Liste_glossaire

@app.callback(
    Output('Ajout_synonyme' , 'children'),
    [Input('add_synonyme', 'n_clicks')],
    [State('input-acronyme', 'value') , State('input-meaning', 'value')]
    )
def ajout_synonyme(n_clicks , value_acronyme , value_meaning):
    """
    #Callback pour ajouter des acronymes dès que l'utilisateur clique sur le boutton Ajouter.
        Input:
            n_clicks : Le clic de l'utilisateur sur le bouton Ajouter
            value_acronyme : L'acronyme en question
            value_meaning : L'expression qui correspond à l'acronyme
        Output:
            L'acronyme est l'expression correspondante sont ajouté au Glossaire dont on dispose
"""
    if n_clicks is None:
        raise PreventUpdate

    f = open(Chemin_Glossaire_enregistre , 'r', encoding="utf8")
    Liste_glossaire =f.read()
    f.close()

    Liste_glossaire = str(Liste_glossaire)
    Liste_glossaire = Liste_glossaire.split('\n')
    Liste_acronyme = map(lambda x: str(x.split("=>")[0]).strip() , Liste_glossaire)

    if value_acronyme not in Liste_acronyme:
        add_syn(value_acronyme , value_meaning , Chemin_Glossaire_enregistre)
        return html.H4("Votre acronyme a été ajouté avec succès" , style = {"background-color" : "green"})
    else:
        return html.H4("L'acronyme existe déjà dans la liste" , style = {"background-color" : "red"})


@app.callback(
    Output('Vide' , 'children'),
    [Input('effectuer_changes' , 'n_clicks')],
    [State('Affichage_synonyme' , 'value')]
)
def ecrire_changement_acronymes(n_clicks , value):
    """
    #Callback pour ecrire les changements dans le fichier de Glossaire et prend en argument:
        Inputs:
            n_clicks : Le clique de l'utilisateir sur SAUVEGARDER
            value: La valeur du glossaire changé
        Output :
            Le glossaire est mis à jour avec les nouvelles modifications faites par l'utilisateur
"""
    if n_clicks is None:
        raise PreventUpdate

    f = open(Chemin_Glossaire_enregistre , 'w', encoding="utf8")
    f.write(str(value))
    f.close()

    logging.info('Le glossaire vient d\'être modifié')
    return
@app.callback(
    Output('Reindex_div' , 'children'),
    [Input('reindex_changes' , 'n_clicks')]
)
def reindexation(n_clicks):
    """
    Callback pour effectuer la réindexation avec les nouvelles modifications du glossaire.
        Inputs:
            n_clicks : Le clic de l'utilisateur sur APPLIQUER
        Output:
            Un réindexation est effectué avec un nouveau dictionnaire des acronymes
    """
    if n_clicks is None:
        raise PreventUpdate

    logging.info('Réindexation')
    Message = str(changement_structure())

    if Message == "Les changements du glossaire ont été pris en compte":
        return html.Div([html.H3(Message)] , style = {"background-color" : "green"})
    else:
        return html.Div([html.H3(Message)] , style = {"background-color" : "red"})


@app.callback(
    Output("Report_changes" , "children"),
    [Input('add_synonyme' , 'n_clicks') , Input('effectuer_changes' , 'n_clicks') , Input('reindex_changes' , 'n_clicks')]
)
def afficher_warning(n_clicks1 , n_clicks2 , n_clicks3):

    """
    Callback pour afficher le message d'alerte si l'utilisateur a effectué des changments
    sur le glossaire des acronymes sans les appliquer au moteur de recherche.
    Inputs:
        n_clicks1 : Le clic de l'utilisateur sur le bouton Ajouter
        n_clicls2 : Le clic de l'utilisateur sur le bouton Sauvegarder
        n_clicks3 : Le clic de l'utilisateur sur le bouton Appliquer
    """

    file1 = open(Chemin_Glossaire_enregistre , 'r' , encoding = 'utf8')
    Enregistre = str(file1.read())
    file1.close()
    file2 = open(Chemin_Glossaire , 'r' , encoding = 'utf8')
    Index = str(file2.read())
    file2.close()

    if Enregistre.strip() == Index.strip():
        return
    else:
        return dcc.Markdown('''
                    ##### **Attention** :  vous avez fait des changements et vous ne les avez pas appliqué au moteur de recherche. Pour les appliquer veuillez cliquer sur le bouton **Appliquer**. Attention cette opération peut prendre un peu de temps.
                    ''' , style = {"text-align" : "center"})
#--------------------------------------------------------------- Callbacks pour l'onglet Changer les expressions métier ---------------------------------

@app.callback(
    Output('Affichage_expressions' , 'value'),
    [Input('add_expression' , 'n_clicks')]
    )
def affichage_expression(n_clicks1):
    """
    Callback pour mettre à jour les expressions clés/mots-clef affichés
    Input:
        n_clicks1: Le clic de l'utilisatuer sur le bouton Ajouter.
    Output:
        Les expressions clés/mots-clef affichées à l'utilisateur sont mis à jour
    """

    f = open(Chemin_expression_enregistre, 'r', encoding="utf8")
    Liste_expression =f.read()
    f.close()
    file = open(Chemin_one_word_keyword_enregistre , 'r' , encoding="utf8")
    Liste_one_word_keyword = file.read()
    file.close()

    Liste_expression = str(Liste_expression).lower()
    Liste_expression = Liste_expression.split('\n')
    try:
        Liste_expression.remove('')
    except:
        pass

    Liste_one_word_keyword = str(Liste_one_word_keyword).lower()
    Liste_one_word_keyword = Liste_one_word_keyword.split('\n')
    try:
        Liste_one_word_keyword.remove('')
    except:
        pass

    Liste_expression = Liste_expression + Liste_one_word_keyword
    Liste_expression.sort()
    Liste_expression = "\n".join(Liste_expression)
    return Liste_expression

@app.callback(
    Output('Ajout_expression' , 'children'),
    [Input('add_expression', 'n_clicks')],
    [State('input_expression', 'value')]
    )
def ajout_expresion(n_clicks , value_expression):
    """
    #Callback pour ajouter des expressions clés/mots-clef dès que l'utilisateur clique sur le boutton Ajouter.
        Input:
            n_clicks : Le clic de l'utilisateur sur le bouton Ajouter
            value_expression : L'expression clés/mots-clef en question
        Output:
            L'expression clés/mots-clef est ajoutée à la liste dont on dispose
    """
    if n_clicks is None:
        raise PreventUpdate
    value_expression = value_expression.strip()
    test = value_expression.split(' ')  #Cette variable permet de tester si c'est un mot-clef ou expression clés

    if len(test) > 1:
        # Si c'est une expression clés
        f = open(Chemin_expression_enregistre, 'r', encoding="utf8")
        Liste_expression =f.read()
        Liste_expression = str(Liste_expression).lower()
        f.close()
        Liste_expression = Liste_expression.split('\n')
        if value_expression.lower().strip() not in Liste_expression:
            add_expression(value_expression, Chemin_expression_enregistre)
            return html.H4("Votre expression a été ajoutée avec succés" , style = {"background-color" : "green"})
        else:
            return html.H4("L'expression existe déjà dans la liste" , style = {"background-color" : "red"})
    else:
        # Sinon c'est un mot-clef
        file = open(Chemin_one_word_keyword_enregistre , 'r' , encoding = 'utf8')
        Liste_one_word_keyword =file.read()
        file.close()
        Liste_one_word_keyword = str(Liste_one_word_keyword).lower()
        Liste_one_word_keyword = Liste_one_word_keyword.split('\n')
        if value_expression.lower().strip() not in Liste_one_word_keyword:
            add_expression(value_expression, Chemin_one_word_keyword_enregistre)
            return html.H4("Votre mot-clé a été ajouté avec succés" , style = {"background-color" : "green"})
        else:
            return html.H4("Le mot-clé existe déjà dans la liste" , style = {"background-color" : "red"})

@app.callback(
    Output('Vide_expression' , 'children'),
    [Input('effectuer_changes_expression' , 'n_clicks')],
    [State('Affichage_expressions' , 'value')])
def ecrire_changement_expression(n_clicks , value):
    """
    #Callback pour ecrire les changements dans les deux fichiers (des mots-clef et des expressions clefs) de et prend en argument:
        Inputs:
            n_clicks : Le clique de l'utilisateir sur SAUVEGARDER
            value: La valeur de la liste changé
        Output :
            Les deux fichers sont mis à jour avec les nouvelles modifications faites par l'utilisateur
    """
    if n_clicks is None:
        raise PreventUpdate
    Liste_mots = value.split('\n')
    Liste_mots = list(map(lambda x: x.strip(), Liste_mots))
    try:
        Liste_mots.remove('')
    except:
        pass
    Liste_one_word = list(filter(lambda x: len(x.split(' ')) == 1, Liste_mots))
    Liste_multiple_word = list(filter(lambda x: len(x.split(' '))>1, Liste_mots))

    f = open(Chemin_expression_enregistre , 'w', encoding="utf8")
    f.write('\n'.join(Liste_multiple_word))
    f.close()

    f = open(Chemin_one_word_keyword_enregistre , 'w', encoding="utf8")
    f.write('\n'.join(Liste_one_word))
    f.close()

    logging.info('Changement de la liste des expressions')
    return 'Les changements ont été sauvegardés mais ne sont pas appliqués'

@app.callback(
    Output('Reindex_div_expression' , 'children'),
    [Input('reindex_changes_expression' , 'n_clicks')]
)
def reindexation_expression(n_clicks):
    """
    Callback pour effectuer la réindexation avec les nouvelles modifications des mots-clefs/expressions clés.
        Inputs:
            n_clicks : Le clic de l'utilisateur sur APPLIQUER
        Output:
            La réindexation est effectuée.
    """
    if n_clicks is None:
        raise PreventUpdate
    logging.info('On vient de commencer la réindexation pour les expressions')
    Message = str(changement_structure_expression())

    if Message == "Les changements des expressions clés ont été pris en compte":
        return html.Div([html.H3(Message)] , style = {"background-color" : "green"})
    else:
        return html.Div([html.H3(Message)] , style = {"background-color" : "red"})


@app.callback(
    Output("Report_changes_expression" , "children"),
    [Input('add_expression' , 'n_clicks') , Input('effectuer_changes_expression' , 'n_clicks') , Input('reindex_changes_expression' , 'n_clicks')]
)
def afficher_warning_expression(n_clicks1 , n_clicks2 , n_clicks3):

    """
    Callback pour afficher le message d'alerte si l'utilisateur a effectué des changments
    sans les appliquer au moteur de recherche.
    Inputs:
        n_clicks1 : Le clic de l'utilisateur sur le bouton Ajouter
        n_clicls2 : Le clic de l'utilisateur sur le bouton Sauvegarder
        n_clicks3 : Le clic de l'utilisateur sur le bouton Appliquer
    """

    time.sleep(0.5)
    file1 = open(Chemin_expression_enregistre , 'r' , encoding = 'utf8')
    Enregistre = str(file1.read())
    file1.close()

    file2 = open(Chemin_expression , 'r' , encoding = 'utf8')
    Index = str(file2.read())
    file2.close()

    file3 = open(Chemin_one_word_keyword_enregistre, 'r', encoding='utf8')
    Enregistre_1 = str(file3.read())
    file3.close()

    file4 = open(Chemin_one_word_keyword, 'r', encoding='utf8')
    Index_1 = str(file4.read())
    file4.close()

    if Enregistre.strip() != Index.strip() or Enregistre_1.strip() != Index_1.strip():
        return dcc.Markdown('''
                        ##### **Attention** :  vous avez fait des changements et vous ne les avez pas appliqué au moteur de recherche. Pour les appliquer veuillez cliquer sur le bouton **Appliquer**. Attention cette opération peut prendre un peu de temps.
                    ''' ,
                    style={"text-align": "center"})
    else:
        return

#------------------------------------------------------------- Callbacks pour l'onglet Mise à jour des documents ------------------------------------------
def save_file(name, content , where = Odt_Files_Directory):
    """
    Fonction permettant d'enregistrer les fichiers.
        Input:
            name : Le nom du fichier
            content : Le contenu du fichier
            where : Le chemin vers le dossier où on veut enregistrer les fichiers
        Output:
            Le fichier est sauvegardé
    """
    data = content.encode("utf8").split(b";base64,")[1]
    with open(where + name, "wb") as fp:
        fp.write(base64.decodebytes(data))
    return

@app.callback(Output('output-pj-upload' , "children"),
            [Input('upload-pj' , 'filename'),
            Input('upload-pj' , 'contents')])
def upload_pj(uploaded_filenames, uploaded_file_contents):

    """
    Callback permettant d'enregistrer les pièces jointes dans le bon dossier.
        Inputs:
            upload_filenames : Liste de nom de fichier à traiter
            uploaded_file_contentents : Liste d contenu de ces fichiers
        Output:
            Les pièces jointes sont enregistrées dans le chemin: Chemin_PiecesJointes
    """

    if uploaded_filenames is None:
        raise PreventUpdate
    div = []
    if uploaded_filenames is not None and uploaded_file_contents is not None:
        if type(uploaded_filenames) is list:
            n = len(uploaded_filenames)
            for i in range(n):
                try:
                    name, data = uploaded_filenames[i], uploaded_file_contents[i]
                    save_file(name, data, Chemin_PiecesJointes)
                    div.append(html.Div(['Le document '+ name + 'a été chargé avec succès'] , className="p-3 mb-2 bg-success text-white"))
                except:
                    div.append(html.Div(['Le document '+ name + 'a été chargé avec succès'] , className="p-3 mb-2 bg-danger text-white"))
        else:
            try:
                name, data = uploaded_filenames, uploaded_file_contents
                save_file(name, data, Chemin_PiecesJointes)
                div.append(html.Div(['Le document '+ name + 'a été chargé avec succès'] , className="p-3 mb-2 bg-success text-white"))
            except:
                div.append(html.Div(['Le document '+ name + 'a été chargé avec succès'] , className="p-3 mb-2 bg-danger text-white"))
    return div
@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'filename'),
              Input('upload-data', 'contents')])
def upload_consultations(uploaded_filenames, uploaded_file_contents):

    """
    Callback permettant d'enregistrer les fichiers en ".odt", ".json" et de les indexer.
        Inputs:
            upload_filenames : Liste de nom de fichier à traiter
            uploadedçfile_contentents : Liste de contenu de ces fichiers
        Ouput:
            Les consultation son en rengisté en Data_odt & Data_Json & indéxé
    """

    if uploaded_filenames is None:
        raise PreventUpdate
    global s
    div = []
    if uploaded_filenames is not None and uploaded_file_contents is not None:
        if type(uploaded_filenames) is list:
            n = len(uploaded_filenames)
            for i in range(n):
                try:
                    s = int((i/(n-1)) * 100)
                except:
                    s = 100
                name, data = uploaded_filenames[i], uploaded_file_contents[i]
                save_file(name, data)
                L = str(upload_docs(uploaded_filenames[i]))
                if L.split(' ')[0] == 'Error:':
                    div.append(html.Div([L] , className="p-3 mb-2 bg-danger text-white"))
                else:
                    div.append(html.Div([L] , className="p-3 mb-2 bg-success text-white"))
            return div
        else:
            name, data = uploaded_filenames, uploaded_file_contents
            save_file(name, data)
            div.append(html.Div([upload_docs(uploaded_filenames)] , className="border-top"))
            return div

@app.callback(Output("progress", "value"), [Input("interval", "n_intervals")])
def advance_progress(n):
    """Callback pour la barre de progression de l'upload des fichiers"""
    global s
    return s

@app.callback(Output("Message_confiramtion_utilisateur" , "children"),
            [Input("del-data" , "n_clicks")] ,
            [State("select-data-to-del" , "value")])
def supprimer_consultation(n_clicks , value):

    """
    Callback permettant de supprimer les consultation non désirée de l'index
    Inputs:
        n_clicks : Le clic de l'utilisateur sur le bouton Supprimer
        value : Le nom de la consultaion à supprimer
    Ouputs:
        La consultaion est supprimé de l'index et de Data_odt & Data_Json
    """

    if n_clicks is None or value is None:
        raise PreventUpdate

    div = []
    for name in value:
        try:

            os.remove(Odt_Files_Directory + name)
            os.remove(JSON_FILES_DIRECTORY + name.split('.')[0] + '.json')

            div.append(html.Div([html.H4('La consultation ' + name + ' a été supprimée avec succès')] , style = {"background-color" : "green"}))
        except:
            div.append(html.Div([html.H4('La consultation ' + name +' n\'a pas été supprimé, veuillez raffraichir cette page.')] , style = {"background-color" : "red"}))
    changement_structure()
    return div


@app.callback(Output("select-data-to-del" , "options"),
            [Input("del-data" , "n_clicks")])
def update_consultation_names(n_clicks):

    """
    Callback permettant de mettre à jour la liste déroulante des consultaion à supprimer
    Inputs:
        n_clicks : Le clic de l'utilisateur sur le bouton supprimer
    Output:
        La nouvelle liste des consultaions mise à jour
    """

    return [{'label': str(x), 'value': str(x)} for x in os.listdir(Odt_Files_Directory)]



@app.callback(Output("Message_confiramtion_utilisateur_pj" , "children"),
            [Input("del-pj" , "n_clicks")] ,
            [State("select-pj-to-del" , "value")])
def supprimer_pj(n_clicks , value):

    """
    Callback permettant de supprimer les pièces jointes non désirée de l'index
    Inputs:
        n_clicks : Le clic de l'utilisateur sur le bouton Supprimer
        value : Le nom de la pièce jointe à supprimer
    Ouputs:
        La pièce jointe est supprimée
    """

    if n_clicks is None or value is None:
        raise PreventUpdate

    div = []
    for name in value:
        try:
            os.remove(Chemin_PiecesJointes + name)
            div.append(html.Div([html.H4('La pièce joite ' + name + ' a été supprimée avec succès')] , style = {"background-color" : "green"}))
        except:
            div.append(html.Div([html.H4('La pièce jointe ' + name +' n\'a pas été supprimé, veuillez raffraichir cette page.')] , style = {"background-color" : "red"}))
    return div

@app.callback(Output("select-pj-to-del" , "options"),
            [Input("del-pj" , "n_clicks")])
def update_pj_names(n_clicks):

    """
    Callback permettant de mettre à jour la liste déroulante des pièces jointes à supprimer
    Inputs:
        n_clicks : Le clic de l'utilisateur sur le bouton supprimer
    Output:
        La nouvelle liste des pièces jointes mise à jour
    """

    return [{'label': str(x), 'value': str(x)} for x in os.listdir(Chemin_PiecesJointes)]
#----------------------------------------------------------------------------------- Callbacks pour l'onglet paramètres généraux -----------------------------------------------
@app.callback(Output("confirmation_changement" , "children"),
[Input('Changement_message_accueil' , "n_clicks")] ,
[State('Message_d\'accueil' , "value") , State("Titre_Message_d'accueil" , "value")])
def Changer_message_accueil(n_clicks , message , titre):

    """
    Callback permettant de changer le message affiché dans la page d'accueil.
    Inputs:
        n_clicks: Clic de l'utilisateur
        message: Le corps du message d'accueil
        titre: Le titre du message d'accueil
    Outputs:
        Le message d'accueil est changé
    """

    if n_clicks is None:
        raise PreventUpdate
    file = open(Chemin_message , 'w' , encoding = 'utf-8')
    file.write(message)
    file.close()

    file = open(Chemin_titre_Message , 'w' , encoding = 'utf-8')
    file.write(titre)
    file.close()

    return " Votre message a été changé avec succès"

@app.callback(Output('Message_d\'accueil' , "value"),
[Input('none', 'children')] )
def afficher_message_accueil(n_clicks):

    """
    Callback permettant d'afficher le message d'accueil dans l'input du message d'accueil
    Inputs:
        n_clicks : Le clic de l'utilisateur sur le bouton CHANGER LE MESSAGE D'ACCUEIL
    Outputs:
        Le message d'accueil enregistré
    """

    file = open(Chemin_message , 'r' , encoding = 'utf-8')
    Message = file.read()
    file.close()
    return Message

@app.callback(Output('Titre_Message_d\'accueil' , "value"),
[Input('none', 'children')] )
def afficher_titre_message_accueil(n_clicks):

    """
    Callback permettant d'afficher le titre du message d'accueil dans l'input du titre du message d'accueil
    Inputs:
        n_clicks : Le clic de l'utilisateur sur le bouton CHANGER LE MESSAGE D'ACCUEIL
    Outputs:
        Le titre du message d'accueil enregistré
    """

    file = open(Chemin_titre_Message , 'r' , encoding = 'utf-8')
    Titre_Message = file.read()
    file.close()
    return Titre_Message

@app.callback(Output("slider-output-container" , "children"),
            [Input('changement_seuil' , "n_clicks")],
            [State('slider_seuil' , "value")])
def changement_seuil(n_clicks , value):

    """
    Callback permettant de changer le seuil de pertinence
    Inputs:
        n_clicks : Le clic de l'utilisateur
        value : La nouvelle valeur du seuil de pertinence
    """

    if n_clicks is None:
        raise PreventUpdate
    try:
        test = float(value)
        file = open(Chemin_seuil , 'w')
        file.write(str(value))
        file.close()

        return 'Vous avez fixé le seuil de pertinence à la valeur: ' + str(value)
    except:
        return

@app.callback(Output('slider_seuil' , "value"),
            [Input('none', 'children')])
def affichage_seuil(n_clicks):

    """
    Callback permettant l'affichage du seuil de pertinenece enregistré dans l'input.
    Inputs:
        n_clicks: Le clic de l'utilisateur
    """

    file = open(Chemin_seuil , 'r')
    seuil = float(file.read())
    file.close()
    return seuil

@app.callback(Output("slider-output-container_affichage" , "children"),
            [Input('changement_seuil_affichage' , "n_clicks")],
            [State('slider_seuil_affichage' , "value")])
def changement_seuil(n_clicks , value):

    """
    Callback permettant de changer le seuil d'affichage
    Inputs:
        n_clicks : Le clic de l'utilisateur
        value : La nouvelle valeur du seuil d'affichage
    """

    if n_clicks is None:
        raise PreventUpdate
    try:
        test = float(value)
        file = open(Chemin_seuil_affichage , 'w')
        file.write(str(value))
        file.close()

        return 'Vous avez fixé le seuil d\'affichage à la valeur: ' + str(value)
    except:
        return

@app.callback(Output('slider_seuil_affichage' , "value"),
            [Input('none', 'children')])
def affichage_seuil(n_clicks ):

    """
    Callback permettant l'affichage du seuil d'affichage enregistré dans l'input.
    Inputs:
        n_clicks: Le clic de l'utilisateur
    """

    file = open(Chemin_seuil_affichage , 'r')
    seuil = float(file.read())
    file.close()
    return seuil
