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
from shutil import copyfile

from converter import pdf2json
#home = os.getenv('HOME')
home = os.getcwd()

elastic_host = environ.get('Elastic_host')
elastic_port = environ.get('Elastic_port')

GLOSSARY_PATH =  environ.get('Chemin_Glossaire')
EXPRESSION_PATH = environ.get('Chemin_list_expression')
MAPPING_DIR = environ.get('Mapping_Directory')

USER_DATA = '/data'
ES_DATA = '/usr/share/elasticsearch/data/extra/test'

GLOSSARY_FILE = 'glossaire.txt'
EXPRESSION_FILE = 'expression.txt'
MAPPING_FILE = 'map.json'

NOM_INDEX = 'iga'
# Connection avec le serveur Elastic
es = Elasticsearch([{'host': str(elastic_host), 'port': str(elastic_port)}])
indices = elasticsearch.client.IndicesClient(es)
#%%


def create_index(nom_index,
            user_data,
            es_data,
            mapping_file,
            glossary_file=None,
            expression_file=None):

    with open(os.path.join(user_data, mapping_file) , 'r' , encoding = 'utf-8') as json_file:
        map = json.load(json_file)

    if glossary_file:
        print('Use glossary file %s'%glossary_file)
        # Copy glossary and experssion file to elastic search mount volume
        copyfile(os.path.join(user_data, glossary_file),
                os.path.join(es_data, glossary_file))
        map['settings']["index"]["analysis"]["filter"]["glossary"].update(
                {"synonyms_path" : os.path.join(es_data, glossary_file)})

    if expression_file:
        print('Use expresion file %s'%expression_file)
        copyfile(os.path.join(user_data, expression_file),
                os.path.join(es_data, expression_file))
        map["settings"]["index"]["analysis"]['char_filter']["my_char_filter"].update(
                {'mappings_path' : os.path.join(es_data, expression_file)})

    print(map)
    with open(os.path.join(es_data, mapping_file), 'w') as outfile:
        json.dump(map, outfile)

    es.indices.delete(index=nom_index, ignore=[400, 404])
    # create index
    es.indices.create(index = nom_index, body=map)


def inject_documents(nom_index, user_data, pdf_path, json_path,
            metada_file=None):

    no_match = 0
    os.makedirs(os.path.join(user_data, json_path), exist_ok=True)

    if metada_file:
        meta_df = pd.read_excel(metada_file)
        #meta_df.set_index('Unnamed: 0' , inplace = True)

    for name_document in os.listdir(os.path.join(user_data, pdf_path)):
        if name_document.endswith(".pdf"):
            try:
                path_document = os.path.join(user_data, pdf_path, name_document)
                print('Read %s'%path_document)
                data = pdf2json(path_document)

                if metada_file:
                    meta = meta_df.loc[meta_df['file'] == name_document, :]

                    if not meta.empty:

                        #data['titre'] = str(meta['titre'].values[0])
                        #data['Date'] = "%d-01-01"%meta['annee2'].values[0].astype(int)
                        #data['Auteurs'] = str(meta['nomaut1'].values[0])
                        meta = meta.iloc[0]
                        meta['date'] = meta['date'].strftime('%Y-%m-%d')
                        data.update(meta)
                    else:
                        no_match += 1
                        continue

                with open(os.path.join(user_data, json_path, name_document.replace('.pdf','.json')) , 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False)

                es.index(index = nom_index, body=data , id = name_document)
                print('Document %s just uploaded'% name_document)

            except Exception as e:
                print(e)
                #break
                print(20*'*')
                print('Error, cannot upload %s'%name_document)
                print(20*'*')

    print("There is %s documents without metadata match"%no_match)
if __name__ == '__main__':

    NOM_INDEX = 'prod'
    USER_DATA = '/data/user'
    ES_DATA = '/usr/share/elasticsearch/data/extra'

    GLOSSARY_FILE = 'glossaire.txt'
    EXPRESSION_FILE = 'syn_expressions_metier.txt'
    MAPPING_FILE = 'map.json'
    METADATA_FILE = 'METADATA.xlsx'

    PDF_DIR = 'Data_Pdf'
    JSON_DIR = 'Data_Json'

    create_index(NOM_INDEX, USER_DATA, ES_DATA, MAPPING_FILE,
                GLOSSARY_FILE,
                EXPRESSION_FILE)

    inject_documents(NOM_INDEX, USER_DATA, PDF_DIR, JSON_DIR,
            metada_file = METADATA_FILE)
