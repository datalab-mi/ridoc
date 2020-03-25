"""Fichier de backend pour gérer les requettes elasticsearch"""

import elasticsearch
from elasticsearch import Elasticsearch
import os
import base64
from converter import pdf2json, odt2json, save_json
import json
import logging
import datetime
from os.path import expanduser
from os import environ
from dotenv import load_dotenv
load_dotenv()
import unicodedata
from datetime import date
from copy import deepcopy

#%%
#On commence par emporter les variables d'environement
home = os.getcwd()

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
#  L'adresse de la liste des mots clefs avec un seul mot affiché à l'utilisateur (temporaire)
#Chemin_one_word_expression_enregitre = home + environ.get('One_word_keyword_non_analyzed_enregistre')
#  L'adresse de la liste des mots clefs avec un seul mot affiché à l'utilisateur
#Chemin_one_word_expression = home + environ.get('One_word_keyword_non_analyzed')
#  L'adresse de la liste des mots clefs avec un seul mot analysé
Chemin_one_word_expression_analyzed = home + environ.get('One_word_keyword_analyzed')

# %%
# On établie une connexion avec le serveur Elastic
es = Elasticsearch([{'host': str(elastic_host), 'port': str(elastic_port)}])
indices = elasticsearch.client.IndicesClient(es)

def simple_request(nom_index):
    request = {
        "query": {
            "match_all" : {}
            }
    }

    #D = es.search(index=str(nom_index), size=15, body=request)
    D = es.search(index=str(nom_index_prop), size=15, body=request)
    return D['hits']['hits']

def request(req , nom_index ,  path_liste_expression_metier = path_list_expression_metier):
    """Fonction qui permet de faire la recherche Elastic dans notre index

    Args:
        nom_index : Le nom de l'index où on effectue la recherche
        req : la requête entrèe par l'utilisateur
        path_liste_expression_metier : Le lien pour la liste des expressions clés analysée
    Output:
        Dictionnaire des résultats de la recherche
    """

    #Je noramlise la requête
    req = unicodedata.normalize('NFKC' , str(req))
    #On récupère la liste des expressions

    file = open(path_liste_expression_metier , 'r')
    content = file.read()
    file.close()
    liste_expression_metier = content.split('\n')[:-1]

    file = open(Chemin_one_word_expression_analyzed , 'r')
    content = file.read()
    file.close()
    liste_keyword = content.split('\n')[:-1]

    file = open(Chemin_Glossaire , 'r', encoding="utf8")
    Liste_glossaire = file.read()
    Liste_glossaire = str(Liste_glossaire)
    file.close()
    Liste_glossaire = Liste_glossaire.split('\n')

    try:
        Liste_glossaire.remove('')
    except:
        pass

    Dic_abrev = {x.split('=>')[0].strip() : x.split('=>')[1].replace(',', '').strip() for x in Liste_glossaire}

    List_acronymes_request = []  # Liste pour la signification des expressions
    List_acro_request = []  #Liste pour les acronymes

    for keyword in Dic_abrev.keys():
        if keyword.lower() in map(lambda x: x.lower() , req.split(' ')):
            List_acronymes_request.append(Dic_abrev[keyword])
            List_acro_request.append(keyword)
    New_req = deepcopy(req)

    for i in range (len(List_acronymes_request)):
        New_req += ' ' + List_acronymes_request[i]

    #Au début on va analyser la requête
    analyse = indices.analyze(body = {'analyzer':"french", "text": New_req})
    L = [analyse["tokens"][i]['token'] for i in range(len(analyse["tokens"]))]

    analyse2 = indices.analyze(body = {'analyzer':"french", "text": req})
    L2 = [analyse2["tokens"][i]['token'] for i in range(len(analyse2["tokens"]))]
    lenght_of_request = len(L2)

    s = " ".join(L)
    request_expression = []
    request_key_one_word = []
    for expression in liste_expression_metier:
        if expression in s and expression.replace(' ', '').replace('-' ,'').replace('_' , '') not in request_expression:
            request_expression.append(expression.replace(' ', '').replace('-' ,'').replace('_' , ''))
            s = s.lstrip(expression).strip()

    for key_one_word in liste_keyword:
        if key_one_word in s and key_one_word not in request_key_one_word:
            request_key_one_word.append(key_one_word)
    #Ensuite on construit notre dictionnaire de la requête
    today = str(date.today())
    year = today.split('-')[0]

    request = {
        "query": {
            "bool": {
                "must": [
                    {
                        "multi_match": {
                            "query": unicodedata.normalize('NFKC', str(req)),
                            "fields": ['DOMAINE', "Question", "Réponse", "TITRE", "Mots clés"],
                            'type': "cross_fields"
                            # "analyze_wildcard": False
                        }
                    },
                    {
                        "multi_match": {
                            "query": unicodedata.normalize('NFKC', str(req)),
                            "fields": ['DOMAINE non stemmed', "Question non stemmed", "Réponse non stemmed", "TITRE non stemmed", "Mots clés non stemmed"],
                            'type': "cross_fields"
                            # "analyze_wildcard": False
                        }
                    },
                    # {
                    #   "simple_query_string":{
                    #   "query": unicodedata.normalize('NFKC' , str(req)) ,
                    #   "fields" : ["all_text"]
                    # }
                    # }
                ],
                "filter": [],
                "should": [],
                "must_not": []
            }
        },
        "highlight": {
            "fragment_size": 150,
            "number_of_fragments": 3,
            "order": "score",
            "boundary_scanner": "sentence",
            "boundary_scanner_locale": "fr-FR",
            "fields": {
                "Réponse": {}
            }
        }
    }

    for key in request_key_one_word:
        request['query']['bool']["should"].append({'match' : {
            "Mots clés analysés": {
                "query": key,
                "boost": 1
                }
            }})
    for key in request_expression:
      print(key)
      request['query']['bool']["should"].append(
          {
              "match": {
                  'Mots clés analysés': {
                      "query": key,
                      "boost": 3
                  }
              }
          })
      request['query']['bool']["should"].append(
          {
              "match": {
                  'TITRE': {
                      "query": key,
                      "boost": 3

                  }
              }
          })
      request['query']['bool']["should"].append(
          {
              "match": {
                  "Réponse": {
                      "query": key,
                      "boost": 1.5
                  }
              }
          })
    request['query']['bool']["should"].append(
        {
            "constant_score": {
                "filter": {
                    "match": {
                        "Date": {
                            "query": year
                        }
                    }
                },
                "boost": 1
            }
        })
    for key in List_acro_request:
      #Boucle sur la liste des acronymes
      request['query']['bool']["should"].append(
          {
              "match": {
                  "Mots clés analysés": {
                      "analyzer": "french",
                      "query": key,
                      "boost": 2
                  }
              }
          })
      request['query']['bool']["should"].append(
          {
              "match": {
                  "TITRE": {
                      "analyzer": "french",
                      "query": key,
                      "boost": 2
                  }
              }
          })
      request['query']['bool']["should"].append(
          {
              "match": {
                  "Réponse": {
                      "analyzer": "french",
                      "query": key,
                      "boost": 1
                  }
              }
          })
    D = es.search(index=str(nom_index), size=15, body=request)
    return D['hits']['hits'] , lenght_of_request


def corriger(req , nom_index):
  """
    Fonction qui permet de corriger la requête de l'utilisateur
    Arguments:
      nom_index : Le nom de l'index où on effectue la recherche des mots
      req : la requête entrèe par l'utilisateur
    Output:
      Liste des suggestions de correction
"""
  D = es.search(index = nom_index , body = {
  "suggest" : {
   "mytermsuggester" : {
      "text" : req,
      "phrase" : {
         "field" : "Réponse"
       }
    }
  }
  })
  L = []
  for i in range (len(list(D['suggest']['mytermsuggester'][0]['options']))):
    L.append(D['suggest']['mytermsuggester'][0]['options'][i]['text'])
  return L

def Synonymes(map , Liste_glossaire , Liste_expression):

  """
  Fonction qui insère la liste des acronymes dans le Mapping
  & gère le boosting des section
  Arguments:
    Map: Le Mapping sans la liste des synonymes
    Liste_glossaire : Liste des acronymes
    Liste_expression : Liste des expressions clefs sous la forme expression => expression, expression_analyzée
  Output:
    Mapping avec la bonne liste des acronymes, des expressions clés et du boosting
"""

  Map_1 = deepcopy(Map)
  Map_1['settings']["index"]["analysis"]["filter"]["french_elision"]["article_case"] = True #Cette igne est ajoutée car le lecteur de fichier JSON considère tout comme une chaine de caractère
  Map_1['settings']["index"]["analysis"]["filter"]["synonym_igpn"]["synonyms"] = Liste_glossaire
  Map_1["settings"]["index"]["analysis"]['char_filter']["my_char_filter"]['mappings'] = Liste_expression
  #Map_1["settings"]["index"]["similarity"]["my_similarity"]["discount_overlaps"] = True

  #Map_1['mappings']['properties']['Question']["boost"] = 1
  #Map_1['mappings']['properties']['TITRE']["boost"] = 2.5
  #Map_1['mappings']['properties']['Mots clés']["boost"] = 1

  #Map_1['mappings']['properties']['Question non stemmed']["boost"] = 1.5
  #Map_1['mappings']['properties']['TITRE non stemmed']["boost"] = 3
  #Map_1['mappings']['properties']['Mots clés non stemmed']["boost"] = 1.5
  return Map_1

def add_syn(acronyme, meaning, Syn_Path = Chemin_Glossaire):

  """
  Fonction qui ecrit le snonyme dans le glossaire
  Arguments:
    acronyme: L'acronyme
    meaning : L'expression correspondante à cet acronyme
    Syn_Path : Le chemin du glossaire
  Output:
    L'acronyme est ecrit dans le fichier du glossaire

"""
  Meaning = meaning.split(' ')
  meaning = str(', '.join(Meaning))
  f = open(Syn_Path , 'a' ,encoding='utf-8')
  f.write("\n" + str(acronyme) + ' => ' +str(acronyme) + ", " + str(meaning))
  f.close()

  return

def add_expression(expression , Chemin_expression):
  """
  Fonction qui ecrit l'expression clés dans l'expression clés
  Arguments:
    expressions: L'expression clé concernée

    Chemin_expression : Le chemin des expressions
  Output:
    L'expressions est ecrite dans le fichier  des expressions clés

"""
  f = open(Chemin_expression , 'a' ,encoding='utf-8')
  f.write("\n" + str(expression))
  f.close()
  return
#%%
def changement_structure_expression():

  """
  Fonction permettant de faire de la réindexation lorsuq'on change notre liste d'expression métier
  Output:
    Un message:
      - "Les changements des expressions clés ont été pris en compte" : La réindexation est faite avec succès

      - "Les changements des expression métiers n'ont pas été appliqué à votre moteur de recherche. Veuillez régler le problème dans l\'acronyme suivant: ": Le problème de la réindexation vient de la liste fournit par l'utilisateur

      -  "Les changements des expression métiers n'ont pas été appliqué à votre moteur de recherche" : Un problème a été rencontré lors de la réindexation

      -   "Une erreur inconnue s'est produite, veuillez réessayer plus tard." : une erreur inconnue s'est produite

"""
#On ajoute le nouveau indice avec les nouveaux mappings
   #On ajoute la Liste des Glossaires notre glossaire
  f = open(Chemin_Glossaire , 'r', encoding="utf8")
  Liste_glossaire_old =f.read()
  Liste_glossaire_old = str(Liste_glossaire_old)
  Liste_glossaire_old = Liste_glossaire_old.split('\n')
  f.close()

  #On commence par construire la nouvelle liste des expressions métier avec des chaines de caractère
  file = open(Chemin_expression_enregistre , 'r' , encoding = "utf-8")
  Expressions = str(file.read())
  file.close()
  Expressions = Expressions.split('\n')

  file = open(Chemin_one_word_expression_enregitre, 'r', encoding="utf-8")
  Keywords = str(file.read())
  file.close()
  Keywords = Keywords.split("\n")

  try:
    Expressions = Expressions.remove('')
  except:
    pass
  try:
    Keywords = Keywords.remove('')
  except:
    pass

  list_expressions = ''
  analyzed_keywords = ""
  analyzed_one_word_keyword = ""

  for expression in Expressions:
    analyse = indices.analyze(body = {'analyzer':"french", "text": expression})
    L = [analyse["tokens"][i]['token'] for i in range(len(analyse["tokens"]))]
    analysed = ''.join(L)
    analysed2 = " ".join(L)
    list_expressions += expression + " => " + expression.strip() + ', ' + analysed.strip() + "\n"
    analyzed_keywords += analysed2.strip() + "\n"

  for keyword in Keywords:
    analyse = indices.analyze(body={"analyzer": "french", "text": keyword})
    L = [analyse["tokens"][i]['token'] for i in range(len(analyse["tokens"]))]
    analysed = ''.join(L)
    analyzed_one_word_keyword += analysed.strip() + "\n"

  file = open(Chemin_list_expression_enregistre , 'w' , encoding = "utf-8")
  file.write(list_expressions)
  file.close()

    #On ajoute le glossaire des expressions métier
  f = open(Chemin_list_expression_enregistre , 'r', encoding="utf8")
  Liste_expression =f.read()
  f.close()
  Liste_expression = str(Liste_expression)
  Liste_expression = Liste_expression.split('\n')
  Liste_expression = Liste_expression[:-1]

  f = open(Chemin_list_expression , 'r', encoding="utf8")
  Liste_expression_old =f.read()
  f.close()
  Liste_expression_old = str(Liste_expression_old)
  Liste_expression_old = Liste_expression_old.split('\n')
  Liste_expression_old = Liste_expression_old[:-1]


  #On crèe notre index
      #On commence par enlever l'ancier index
  if indices.exists(index = nom_index):
    indices.delete(index = nom_index)
    logging.info('On vient de supprimer l\'ancien index')
  with open(Mapping_Directory , 'r' , encoding = 'utf-8') as json_file:
    Map_basic = json.load(json_file)
  Map = Synonymes(Map_basic, Liste_glossaire_old , Liste_expression)
  Map_old = Synonymes(Map_basic , Liste_glossaire_old , Liste_expression_old)

  try:
    indices.create(index = nom_index , body = Map)
    Message = "Les changements des expressions clés ont été pris en compte"

    file = open(Chemin_list_expression_enregistre , 'r' , encoding = 'utf8')
    New_content = file.read()
    file.close()

    file = open(Chemin_list_expression , 'w')
    file.write(New_content)
    del(New_content)
    file.close()

    file = open(Chemin_expression_enregistre , 'r' , encoding = 'utf8')
    New_content = file.read()
    file.close()

    file = open(Chemin_expression , 'w')
    file.write(New_content)
    del(New_content)
    file.close()

    #file = open(Chemin_one_word_expression_enregitre, 'r', encoding='utf-8')
    #New_content = file.read()
    #file.close()

    #file = open(Chemin_one_word_expression, 'w', encoding='utf-8')
    #file.write(New_content)
    #del(New_content)
    #file.close()

    file = open(path_list_expression_metier , "w")
    file.write(analyzed_keywords)
    file.close()

    file = open(Chemin_one_word_expression_analyzed, "w", encoding='utf-8')
    file.write(analyzed_one_word_keyword)
    file.close()

  except elasticsearch.exceptions.RequestError as e:
    indices.create(index = nom_index , body = Map_old)
    print(e)
    try:
      line_of_error = int(e.args[2]['error']['caused_by']['reason'].split('at line')[-1].strip())
      Message = "Les changements des expression métiers n'ont pas été appliqué à votre moteur de recherche. Veuillez régler le problème dans l\'acronyme suivant:\" " +Liste_expression[line_of_error -1] + "\" "
    except:
      Message = "Les changements des expression métiers n'ont pas été appliqué à votre moteur de recherche"
  except:
    indices.create(index = nom_index , body = Map_old)
    Message = "Une erreur inconnue s'est produite, veuillez réessayer plus tard."
  #On met nos documents dans notre index
  for filename in os.listdir(JSON_FILES_DIRECTORY):
    if filename.endswith(".json"):
      f = open(str(JSON_FILES_DIRECTORY + filename) , encoding = 'utf-8')
      docket_content = f.read()
      f.close()

      content = json.loads(docket_content)
      keyword = content['Mots clés'][0].split('-')[1:]
      s = ""

      for i in range(len(keyword)):
        mot_clef = keyword[i].strip()
        analyse = indices.analyze(body = {'analyzer':"french", "text": mot_clef})
        L = [analyse["tokens"][i]['token'] for i in range(len(analyse["tokens"]))]
        words = " ".join(L)
        s += words.replace(' ' , '').replace('-', '').replace('_', '')
        s += ', '
      s = [s]

      content['Mots clés analysés'] = s

      name = str(filename.split('.')[0]) + '.odt'
      es.index(index=nom_index , body=content , id = name)
      logging.info('On vient de charger le fichier %s' %filename)
  return Message
#%%
def changement_structure():

  """
  Fonction permettant de faire de la réindexation lorsuq'on change notre glossaire d'acronyme
  Output:
    Un message:
      - "Les changements du glossaire ont été pris en compte" : La réindexation est faite avec succès

      - "Les changements du glossaire n'ont pas été appliqué à votre moteur de recherche. Veuillez régler le problème dans l\'acronyme suivant: ": Le problème de la réindexation vient de la liste fournit par l'utilisateur

      -  "Les changements du glossaire n'ont pas été appliqué à votre moteur de recherche" : Un problème a été rencontré lors de la réindexation
"""


#On ajoute le nouveau indice avec les nouveaux mappings
   #On ajoute la Liste des Glossaires notre glossaire
  f = open(Chemin_Glossaire_enregistre , 'r', encoding="utf8")
  Liste_glossaire =f.read()
  Liste_glossaire = str(Liste_glossaire)
  Liste_glossaire = Liste_glossaire.split('\n')
  f.close()

  f = open(Chemin_Glossaire , 'r', encoding="utf8")
  Liste_glossaire_old =f.read()
  Liste_glossaire_old = str(Liste_glossaire_old)
  Liste_glossaire_old = Liste_glossaire_old.split('\n')
  f.close()

  #On ajoute le glossaire des expressions métier

  f = open(Chemin_list_expression , 'r', encoding="utf8")
  Liste_expression =f.read()
  Liste_expression = str(Liste_expression)
  Liste_expression = Liste_expression.split('\n')
  f.close()
  Liste_expression = Liste_expression[:-1]

  #On crèe notre index
      #On commence par enlever l'ancier index
  if indices.exists(index = nom_index):
    indices.delete(index = nom_index)
    logging.info('On vient de supprimer l\'ancien index')
  n = len(list(os.listdir(JSON_FILES_DIRECTORY)))
  with open(Mapping_Directory , 'r' , encoding = 'utf-8') as json_file:
    Map_basic = json.load(json_file)
  Map = Synonymes(Map_basic, Liste_glossaire , Liste_expression)
  Map_old = Synonymes(Map_basic , Liste_glossaire_old , Liste_expression)

  try:
    indices.create(index = nom_index , body = Map)
    Message = "Les changements du glossaire ont été pris en compte"

    file = open(Chemin_Glossaire_enregistre , 'r' , encoding = 'utf8')
    New_content = file.read()
    file.close()

    file = open(Chemin_Glossaire , 'w')
    file.write(New_content)
    del(New_content)
    file.close()

  except elasticsearch.exceptions.RequestError as e:
    indices.create(index = nom_index , body = Map_old)
    try:
      line_of_error = int(e.args[2]['error']['caused_by']['reason'].split('at line')[-1].strip())
      Message = "Les changements du glossaire n'ont pas été appliqué à votre moteur de recherche. Veuillez régler le problème dans l\'acronyme suivant:\"" +Liste_glossaire[line_of_error -1] + "\" "
    except:
      Message = "Les changements du glossaire n'ont pas été appliqué à votre moteur de recherche"
  except:
    indices.create(index = nom_index , body = Map_old)
    Message = "Une erreur inconnue s'est produite, veuillez réessayer plus tard."


  #On met nos documents dans notre index


  for filename in os.listdir(JSON_FILES_DIRECTORY):
    if filename.endswith(".json"):
      f = open(str(JSON_FILES_DIRECTORY + filename) , encoding = 'utf-8')
      docket_content = f.read()
      f.close()

      content = json.loads(docket_content)
      keyword = content['Mots clés'][0].split('-')[1:]
      s = ""

      for i in range(len(keyword)):
        mot_clef = keyword[i].strip()
        analyse = indices.analyze(body = {'analyzer':"french", "text": mot_clef})
        L = [analyse["tokens"][i]['token'] for i in range(len(analyse["tokens"]))]
        words = " ".join(L)
        s += words.replace(' ' , '').replace('-', '').replace('_', '')
        s += ', '
      s = [s]

      content['Mots clés analysés'] = s

      name = str(filename.split('.')[0]) + '.odt'
      es.index(index=nom_index , body=content , id = name)
      logging.info('On vient de charger le fichier %s' %filename)
  return Message


def upload_docs(path_doc: str):
    """ Fonction permettant la création de l'index s'il n'est pas déja crée, La conversion des docs odt en Json l'enregistrement de ces Json et leur indexation

   Args:
     path_doc: Le nom du document à uploader

   Output:
     Document indéxé
     Erreur si une erreur intervient dans le process
    """

    if not indices.exists(index = nom_index):   #On crèe l'index s'il n'est pas déja existant
        #f = open(Chemin_Glossaire , 'r', encoding="utf8")
        #Liste_glossaire =f.read()
        #Liste_glossaire = str(Liste_glossaire)
        #Liste_glossaire = Liste_glossaire.split('\n')
        #f.close()

        ##On ajoute le glossaire des expressions métier
        #f = open(Chemin_list_expression , 'r', encoding="utf8")
        #Liste_expression =f.read()
        #Liste_expression = str(Liste_expression)
        #Liste_expression = Liste_expression.split('\n')
        #f.close()
        #Liste_expression = Liste_expression[:-1]

        #On crèe notre index
        with open(Mapping_Directory , 'r' , encoding = 'utf-8') as json_file:
            Map = json.load(json_file)
            #Map = Synonymes(Map, Liste_glossaire , Liste_expression)

        indices.create(index = nom_index , body = Map)

    if path_doc.endswith(".odt"):
        base_name = os.path.basename(path_doc)
        filename, file_extension = os.path.splitext(base_name)
        output_name = '{}.json'.format(filename)
        #T = convertisseur_Odt_Json(path_doc , path_doc)
        data = convertisseur_odt_txt(path_doc)
        T = save_json(data, output_name)
        if type(T) is int:  #Si le type de T est entier je sais qu'l y a eu une erreur dans la conversion dûe à de mauvais titres de section
            logging.error('Une erreur a été détecté dans le document %s'% path_doc)
            return str('Error: Un problème a été détecté dans le document ' + path_doc + 'Veuillez revoir le nom des différentes sections du document')
        else:
            f = open(os.path.join(str(JSON_FILES_DIRECTORY), output_name), encoding="utf-8")
            docket_content = f.read()
            f.close()

            content = json.loads(docket_content)
            #Indexer le document automatiquement dans l'index de correction de fautes d'orthographe
            es.index(index=nom_index_prop, id=base_name, body=content)
            logging.info('On vient d\'uploader le document {} dans {}'.format(base_name, nom_index_prop))


            if 'Mots clés' in content:
                keyword = content['Mots clés'][0].split('-')[1:]
                s = ""

                for i in range(len(keyword)):
                    mot_clef = keyword[i].strip()
                    analyse = indices.analyze(body = {'analyzer':"french", "text": mot_clef})
                    L = [analyse["tokens"][i]['token'] for i in range(len(analyse["tokens"]))]
                    words = " ".join(L)
                    s += words.replace(' ' , '').replace('-', '').replace('_', '')
                    s += ', '
                s = [s]

                content['Mots clés analysés'] = s
                es.index(index = nom_index, id = base_name, body=content)
                logging.info('On vient d\'uploader le document {} dans {}'.format(base_name, nom_index))
    if path_doc.endswith(".pdf"):
        txt = convertisseur_pdf_txt(path_doc)
        name = 'doc name'
        Titre = 'doc titre'
        Date = 'doc date'
        Auteurs = 'doc auteur 1'
        data = dict(Titre=Titre, Date=Date,Auteurs=Auteurs)
        data['Corps'] = txt

        base_name = os.path.basename(path_doc)
        print("BASEname", base_name)
        filename, file_extension = os.path.splitext(base_name)
        output_name = '{}.json'.format(filename)
        T = save_json(data, output_name)
        if type(T) is int:  #Si le type de T est entier je sais qu'l y a eu une erreur dans la conversion dûe à de mauvais titres de section
            logging.error('Une erreur a été détecté dans le document %s'% path_doc)
            return str('Error: Un problème a été détecté dans le document ' + path_doc + 'Veuillez revoir le nom des différentes sections du document')
        else:
            f = open(os.path.join(str(JSON_FILES_DIRECTORY), output_name), encoding="utf-8")
            docket_content = f.read()
            f.close()

            content = json.loads(docket_content)
            #Indexer le document automatiquement dans l'index de correction de fautes d'orthographe
            print(content)
            es.index(index=nom_index_prop, id=base_name, body=content)
            logging.info('On vient d\'uploader le document {} dans {}'.format(base_name, nom_index_prop))
    else: #Le fichier ne se termine pas par un ".odt"
        logging.error('Le document %s n\'est pas un ODT'% path_doc )
        return 'Error: Le document n\'est pas un odt'
    return ('Le document {} a été téléchargé avec succès'.format(path_doc)) #Message retouné pour un succès

if __name__ == '__main__':
    path_doc = '/app/tests/doc.pdf'
    upload_docs(path_doc)
    result = simple_request(nom_index)
