"""
            Fichier permettant de convertir les fichiers du ".odt" à ".json" 
"""
#%%
import json, collections
from odf import text, teletype
from odf.opendocument import load
import os
from os import environ
from dotenv import load_dotenv

load_dotenv()




#%%
#Les variables d'environement
home = os.getenv("HOME")

Chemin_Glossaire = home + environ.get('Chemin_Glossaire')
#Chemin_Dictionnaire = home + environ.get('Chemin_Dictionnaire')
Mapping_Directory = home + environ.get('Mapping_Directory')
JSON_FILES_DIRECTORY = home + environ.get('JSON_FILES_DIRECTORY')
Odt_Files_Directory = home + environ.get('Odt_Files_Directory')
nom_index = environ.get('Nom_index')
#%%
def convertisseur_Odt_Json(directory, name , sections = ['TITRE' , 'DOMAINE' , 'Mots clés' , 'Date' , 'Question' , 'Réponse' , 'Pièces jointes' , 'Liens' , 'Références']):
    """
    Fonction qui permet la conversion des Json en Odt elle prend en argument:
        directory : le chemin du fichier en question
        name : Le nome du fichier
        sections : les sections constituants le document
    Output:
        Fichier convertis en Json et enregistré dans le JSON_File_Directory
    """
    doc = load(directory)
    #J'ai accés aux élélments du document
    allparas = doc.getElementsByType(text.P)
    #Liste pour les éléments du document
    L=[]
    for i in range (len(allparas)):
        L.append(teletype.extractText(allparas[i]))
    # remove ''s i.e Nones
    L = list(filter(None, L))
    #J'enlève le cadre
    L = L[3:]
    #J'enlève les caractères spaciaux
    for i in range (len(L)):
        L[i] = L[i].replace(u'\xa0', u' ') #J'enlève les \xa0
        L[i] = L[i].replace(u'\n' , u' ') #J'enlève les \n
    json_li = []
    # convert and store all values
    Sections = sections 
    position_section = 0
    d = collections.defaultdict()
    Refs = True
    check = 0
    for x in L:
        y = x.split(':')
        if (position_section < 7 and y[0].replace(u' ' ,u'').lower() == Sections[position_section].replace(u' ' , u'').lower()) or (position_section == 7 and (y[0].replace(u' ' ,u'').lower() ==  Sections[position_section].replace(u' ' , u'').lower() or y[0].replace(u' ' ,u'').lower() ==  Sections[position_section + 1].replace(u' ' , u'').lower())): #Je ne tiens pas compte des espaces et majiscules
            try:
                if position_section < 7:
                    d[Sections[position_section]] = y[1:]
                else:
                    d['Liens'] = y[1:]
                    Refs = False
            except:
                d[y[0]] = ''
            if position_section<7: #Pour ne pas avoir de problème dans la dernière itération de la boucle
                position_section += 1
            check += 1
        
        else:
            if list(d.keys())[-1] == "Pièces jointes":
                d[list(d.keys())[-1]][-1] += str(x) + "\n"
            else:
                d[list(d.keys())[-1]][-1] += str(x)
    
    if check != 8:
        #Je check s'il y a vraiment 8 sections comme ça j'enlève à la main tout ce qui n'est pas conforme
        return int(check)
        
    with open(str(str(JSON_FILES_DIRECTORY) + name.split('.')[0] + '.json') , 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False)
    return 'Ok'
    
