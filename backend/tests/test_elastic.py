import sys, json, os
from dotenv import load_dotenv
from os import environ
import pandas as pd
import elasticsearch
from elasticsearch import Elasticsearch
from shutil import copyfile

load_dotenv()
elastic_host = environ.get('Elastic_host')
elastic_port = environ.get('Elastic_port')

sys.path.append('./tools')

from script import create_index, inject_documents
from converter import pdf2json

GLOSSARY_PATH =  environ.get('Chemin_Glossaire')
EXPRESSION_PATH = environ.get('Chemin_list_expression')
MAPPING_DIR = environ.get('Mapping_Directory')

USER_DATA = 'tests/data'
ES_DATA = '/usr/share/elasticsearch/data/extra/test'

GLOSSARY_FILE = 'glossaire.txt'
EXPRESSION_FILE = 'expression.txt'
MAPPING_FILE = 'map.json'

PDF_DIR = ''
JSON_DIR = ''

os.makedirs(ES_DATA, exist_ok=True)
es = Elasticsearch([{'host': str(elastic_host), 'port': str(elastic_port)}])
NOM_INDEX = 'test'

def test_inject():

    # delete index, ignore if not exist.
    es.indices.delete(index=nom_index, ignore=[400, 404])
    # create index
    es.indices.create(index = nom_index)

    directory = '/app/tests/data/doc.pdf'
    #directory = '/app/tests/data/ignit_pnigitis.pdf'
    name = 'doc name'
    Titre = 'doc titre'
    Date = 'doc date'
    Auteurs = 'doc auteur 1'
    #convertisseur_Pdf_Json(directory, name, Titre, Date, Auteurs)
    data = pdf2json(directory)
    es.index(index = nom_index, body=data , id = 'doc.pdf')

    res = es.get(index=NOM_INDEX, id= 'doc.pdf')
    assert res['source'] == {'content': 'Ceci est un texte pdf'}, res['source']



def test_create_index():

    create_index(NOM_INDEX, USER_DATA, ES_DATA, MAPPING_FILE)

    with open(os.path.join(USER_DATA, MAPPING_FILE) , 'r' , encoding = 'utf-8') as json_file:
        map = json.load(json_file)

    # Copy glossary and experssion file to elastic search mount volume
    copyfile(os.path.join(USER_DATA, GLOSSARY_FILE), os.path.join(ES_DATA, GLOSSARY_FILE))
    copyfile(os.path.join(USER_DATA, EXPRESSION_FILE), os.path.join(ES_DATA, EXPRESSION_FILE))

    map['settings']["index"]["analysis"]["filter"]["glossary"].update(
            {"synonyms_path" : os.path.join(ES_DATA, GLOSSARY_FILE)})
    map["settings"]["index"]["analysis"]['char_filter']["my_char_filter"].update(
            {'mappings_path' : os.path.join(ES_DATA, EXPRESSION_FILE)})

    print(map)
    es.indices.delete(index=NOM_INDEX, ignore=[400, 404])
    # create index
    es.indices.create(index = NOM_INDEX, body=map)

def test_analyse_index():

    # create elasticsearch index

    indices = elasticsearch.client.IndicesClient(es)

    body = {
          "analyzer": "rebuilt_french_content",
          "text": "Sans la carte agent il est difficile de rentrer au MI"
        }


    res = indices.analyze(index = NOM_INDEX, body=body)
    print(res)
    list_synonym = [token['token'] for token in res['tokens'] if token['type'] == 'SYNONYM']
    assert list_synonym == ['minister', 'interieu'], list_synonym

    body = {
          "analyzer": "rebuilt_french_content",
          "text": "Jusqu'ici, je n'ai jamais été à un comité de pilotage de la PN"
        }


    res = indices.analyze(index = NOM_INDEX, body=body)
    print(res)
    assert 'Jusqu'not in  str(res['tokens'])
    assert 'comitpilo' in  str(res['tokens']), 'expresion not taken into account'

def test_inject_documents():
    metada_file = 'metadata.xlsx'

    inject_documents(NOM_INDEX, USER_DATA, PDF_DIR, JSON_DIR,
                metada_file = metada_file)

    meta_df = pd.read_excel(os.path.join(USER_DATA, metada_file) )
    print(meta_df)
    for name_document in os.listdir(USER_DATA):
        if name_document.endswith(".pdf"):
            path_document = os.path.join(USER_DATA, name_document)
            print('Read %s'%path_document)
            data = pdf2json(path_document)
            meta = meta_df.loc[meta_df['filename'] == name_document, :]
            data['titre'] = str(meta['titre'].values[0])
            data['Date'] = str(meta['annee2'].values[0])
            data['Auteurs'] = str(meta['nomaut1'].values[0])
            print(data)


if __name__ == '__main__':
    test_create_index()
    test_analyse_index()
    test_inject_documents()
