import sys, json, os
from pathlib import Path  # python3 only
from dotenv import load_dotenv
from os import environ
import pandas as pd
import elasticsearch
from elasticsearch import Elasticsearch
from shutil import copyfile

from tools.elastic import create_index, inject_documents, search
from tools.converter import pdf2json

#import pdb; pdb.set_trace()

env_path = '/app/tests/iga/.env-iga'
load_dotenv(dotenv_path=env_path)

NOM_INDEX = os.getenv('NOM_INDEX')

USER_DATA = os.getenv('USER_DATA')
ES_DATA = os.getenv('ES_DATA')

GLOSSARY_FILE = os.getenv('GLOSSARY_FILE')
EXPRESSION_FILE = os.getenv('EXPRESSION_FILE')
MAPPING_FILE =  os.getenv('MAPPING_FILE')

PDF_DIR = os.getenv('PDF_DIR')
JSON_DIR = os.getenv('JSON_DIR')

os.makedirs(ES_DATA, exist_ok=True)

es = Elasticsearch([{'host': 'elasticsearch', 'port': '9200'}])

doc_guyane_eau = "les-bonnes-feuilles-IGA-eau-potable-en-guadeloupe.pdf"


def test_create_index():
    create_index(NOM_INDEX, USER_DATA, ES_DATA, MAPPING_FILE, GLOSSARY_FILE, EXPRESSION_FILE )



def test_inject_documents():
    metada_file = 'iga.xlsx'
    META_DIR = os.path.join(USER_DATA, PDF_DIR, metada_file)
    inject_documents(NOM_INDEX, USER_DATA, PDF_DIR, JSON_DIR,
                metada_file = META_DIR)

    res = es.get(index=NOM_INDEX, id= doc_guyane_eau)
    assert len(str(res)) > 1000, res

def test_analyse_index():

    # create elasticsearch index

    indices = elasticsearch.client.IndicesClient(es)

    body = {
          "analyzer": "custom_french",
          "text": "Sans la carte agent il est difficile de rentrer au MI"
        }

    res = indices.analyze(index = NOM_INDEX, body=body)
    print(res)
    print(' '.join([token['token'] for token in res['tokens']]))
    list_synonym = [token['token'] for token in res['tokens'] if token['type'] == 'SYNONYM']
    assert list_synonym == ['minister', 'interieu'], list_synonym

    body = {
          "analyzer": "custom_french",
          "text": "Jusqu'ici, je n'ai jamais été à un comité de pilotage de la DCRFPN"
        }


    res = indices.analyze(index = NOM_INDEX, body=body)
    print(res)
    print(' '.join([token['token'] for token in res['tokens']]))

    assert 'Jusqu'not in  str(res['tokens'])
    assert 'comisearchtpilo' in  str(res['tokens']), 'expresion not taken into account'

    # § sensibilité au accents

def test_search():
    glossary_file = Path(USER_DATA) / GLOSSARY_FILE
    expression_file = Path(USER_DATA) / 'analysed_expression.txt'

    req = 'travail illegal'
    #import pdb; pdb.set_trace()
    hits, length_req, bande = search(req, NOM_INDEX, str(glossary_file), str(expression_file))
    print(hits, length_req, bande)
    
if __name__ == '__main__':
    #test_create_index()
    #test_inject_documents()
    #test_analyse_index()
    test_search()
