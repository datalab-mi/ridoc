import elasticsearch
from elasticsearch import Elasticsearch
import os
import json, collections
from os.path import expanduser
from os import environ
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
from tika import parser
from elastic import Synonymes
import numpy as np


#home = os.getenv('HOME')
home = os.getcwd()
Chemin_Glossaire = home + environ.get('Chemin_Glossaire')
Mapping_Directory = home + environ.get('Mapping_Directory')
Json_Files_directory = home + environ.get('Json_Files_directory')
Pdf_Files_Directory = home + environ.get('Pdf_Files_Directory')
nom_index = environ.get('Nom_index')
elastic_host = environ.get('Elastic_host')
elastic_port = environ.get('Elastic_port')
Chemin_list_expression = home + environ.get('Chemin_list_expression')

#%%
#On établie une connexion avec le serveur Elastic
es = Elasticsearch([{'host': str(elastic_host), 'port': str(elastic_port)}])
indices = elasticsearch.client.IndicesClient(es)
#%%

data = pd.read_excel('METADATA.xlsx')
data.set_index('Unnamed: 0' , inplace = True)

if not indices.exists(index = nom_index):   #On crèe l'index s'il n'est pas déja existant
    f = open(Chemin_Glossaire , 'r', encoding="utf8")
    Liste_glossaire =f.read()
    f.close()
    Liste_glossaire = str(Liste_glossaire)
    Liste_glossaire = Liste_glossaire.split('\n')

    f = open(Chemin_list_expression , 'r', encoding="utf8")
    Liste_expression =f.read()
    Liste_expression = str(Liste_expression)
    Liste_expression = Liste_expression.split('\n')
    f.close()
    Liste_expression = Liste_expression[:-1]

    with open(Mapping_Directory , 'r' , encoding = 'utf-8') as json_file:
        Map = json.load(json_file)
    Map = Synonymes(Map, Liste_glossaire , Liste_expression)

    indices.create(index = nom_index , body = Map)

for name_document in os.listdir(Pdf_Files_Directory):
    if name_document.endswith(".pdf"):
        try:
            directory = Pdf_Files_Directory + name_document
            print("FILE:", directory)
            file_data = parser.from_file(directory,"http://tika:9998/")
            print("data", file_data)
            text = file_data['content']
            if len(text)>1000:
                text=text.replace(u'\xa0', u' ')
                text=text.replace(u'\n' , u' ')
                text=text.replace(u'\xa0', u' ')
                text=text.replace(u'\n' , u' ')
                Sections = ['CORPS']
                d = collections.defaultdict()
                d[Sections[0]] = text

                try:
                    d['Titre'] = str(np.array(data['titre'][data['filename'] == name_document])[0])
                    d['Date'] = str(int(np.array(data['annee2'][data['filename'] == name_document])[0])) + "-05-31"
                    d['Auteurs'] = str(np.array(data['nomaut1'][data['filename'] == name_document])[0])
                except:
                    print('pass')
                    continue
                with open(str(str(Json_Files_directory) + name_document.split('.')[0] + '.json') , 'w', encoding='utf-8') as f:
                    json.dump(d, f, ensure_ascii=False)
                f = open(str(Json_Files_directory + str(name_document.split('.')[0] + '.json')), encoding="utf-8")
                docket_content = f.read()
                es.index(index = nom_index, body=json.loads(docket_content) , id = name_document)
                f.close()
                print('On vient d\'uploader le document %s'% name_document)

            else:
                print("Pas Upload du doc" , name_document)
        except Exception as e:
            print(e)
            break
            print('Pas d\'upload')

