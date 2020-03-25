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

USER_DATA = 'tests/iga/data'
ES_DATA = '/usr/share/elasticsearch/data/extra/iga'

GLOSSARY_FILE = 'glossaire.txt'
EXPRESSION_FILE = 'expression.txt'
MAPPING_FILE = 'map.json'

PDF_DIR = 'pdf'
JSON_DIR = 'json'

os.makedirs(ES_DATA, exist_ok=True)

es = Elasticsearch([{'host': str(elastic_host), 'port': str(elastic_port)}])
NOM_INDEX = 'iga'

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
          "analyzer": "french",
          "text": "Sans la carte agent il est difficile de rentrer au MI"
        }


    res = indices.analyze(index = NOM_INDEX, body=body)
    print(res)
    print(' '.join([token['token'] for token in res['tokens']]))
    list_synonym = [token['token'] for token in res['tokens'] if token['type'] == 'SYNONYM']
    assert list_synonym == ['minister', 'interieu'], list_synonym

    body = {
          "analyzer": "french",
          "text": "Jusqu'ici, je n'ai jamais été à un comité de pilotage de la DCRFPN"
        }


    res = indices.analyze(index = NOM_INDEX, body=body)
    print(res)
    print(' '.join([token['token'] for token in res['tokens']]))

    assert 'Jusqu'not in  str(res['tokens'])
    assert 'comitpilo' in  str(res['tokens']), 'expresion not taken into account'

    # § sensibilité au accents


if __name__ == '__main__':
    test_create_index()
    test_inject_documents()
    test_analyse_index()
