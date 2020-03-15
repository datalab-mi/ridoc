"""Fichier permettant de convertir les fichiers du .odt, pdf à .json """

import os
import json, collections
from odf import text, teletype
from odf.opendocument import load
from tika import parser
from os import environ
from dotenv import load_dotenv

load_dotenv()

# Les variables d'environement
home = os.getcwd()
Json_Files_directory = home + environ.get('Json_Files_directory')


def convertisseur_odt_txt(path: str) -> str:
    """ Fonction qui permet la conversion des Json en Odt elle prend en argument:

    Args:
        path : le chemin du fichier en question
    Returns:
        text: text
    """
    doc = load(path)
    #J'ai accés aux élélments du document
    allparas = doc.getElementsByType(text.P)
    #Liste pour les éléments du document
    L=[]
    for i in range (len(allparas)):
        L.append(teletype.extractText(allparas[i]))
    # remove ''s i.e Nones
    L = list(filter(None, L))
    #J'enlève le cadre
    # TODO Specific to some docs
    ###L = L[3:]
    #J'enlève les caractères spaciaux
    for i in range (len(L)):
        L[i] = L[i].replace(u'\xa0', u' ') #J'enlève les \xa0
        L[i] = L[i].replace(u'\n' , u' ') #J'enlève les \n
    # convert and store all values
    sections = ['TITRE' , 'DOMAINE' , 'Mots clés' , 'Date' , 'Question' , 'Réponse' , 'Pièces jointes' , 'Liens' , 'Références']

    d = dict(Corps=" ".join(L))
    check = 0
    for x in L:
        y = x.split(':')
        if y[0].strip() in sections:
            if len(y[1].strip()) > 1:
                d[y[0].strip()] = y[1].strip()

    # TODO à detailler l'extraction des données
    return d


def convertisseur_pdf_txt(path: str) -> str:
    """
    Fonction qui permet la conversion des Pdf en Jso et prend en argument:

    Args:
        path : le chemin du fichier en question
    Returns:
        path: clean text
    """
    try:
        file_data = parser.from_file(path,"http://tika:9998/")
        data = file_data['content']
        data=data.replace(u'\xa0', u' ')
        data=data.replace(u'\n' , u' ')
        data=data.replace(u'\xa0', u' ')
        data=data.replace(u'\n' , u' ')
        return data
    except Exception as e:
        print(e)
        return 0

def save_json(data, json_path: str):
    if not os.path.exists(Json_Files_directory):
        os.makedirs(Json_Files_directory)
    with open(os.path.join(str(Json_Files_directory),  json_path) , 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    return 'OK'

if __name__ == '__main__':
    path = '/app/tests/doc.odt'
    data = convertisseur_odt_txt(path)
    save_json(data, 'docOdt.json')

    path = '/app/tests/doc.pdf'
    txt = convertisseur_pdf_txt(path)
    name = 'doc name'
    Titre = 'doc titre'
    Date = 'doc date'
    Auteurs = 'doc auteur 1'
    data = dict(Titre=Titre, Date=Date,Auteurs=Auteurs)
    data['Corps'] = txt
    save_json(data, 'doc.json')
