import sys, json, os, time
from pathlib import Path  # python3 only
from dotenv import load_dotenv
from os import environ
import pandas as pd
import elasticsearch
from elasticsearch import Elasticsearch
from shutil import copyfile

from tools.elastic import es, create_index, get_alias, put_alias, delete_alias, get_index_name, replace_blue_green, inject_documents, search, index_file, suggest, get_tag
from tools.converter import pdf2json

import pytest
#import pdb; pdb.set_trace()

env_path = '/app/tests/iga/.env-iga'
load_dotenv(dotenv_path=env_path, override=True)

INDEX_NAME = os.getenv('INDEX_NAME')

USER_DATA = os.getenv('USER_DATA')
ES_DATA = os.getenv('ES_DATA')

GLOSSARY_FILE = os.getenv('GLOSSARY_FILE')
EXPRESSION_FILE = os.getenv('EXPRESSION_FILE')
RAW_EXPRESSION_FILE = os.getenv('RAW_EXPRESSION_FILE')
THRESHOLD_FILE = os.getenv('THRESHOLD_FILE')

MAPPING_FILE =  os.getenv('MAPPING_FILE')

DST_DIR = os.getenv('DST_DIR')
JSON_DIR = os.getenv('JSON_DIR')
META_DIR =  os.getenv('META_DIR')

os.makedirs(ES_DATA, exist_ok=True)
# Section path
path_sections = Path(USER_DATA) / 'sections.json'
if path_sections.exists():
    with open(path_sections, 'r' , encoding = 'utf-8') as json_file:
        sections = json.load(json_file)
else:
    sections = []
# es = Elasticsearch([{'host': 'elasticsearch', 'port': '9200'}])

doc_guyane_eau = "les-bonnes-feuilles-IGA-eau-potable-en-guadeloupe.pdf"

def test_create_index():
    # Clear
    #import pdb; pdb.set_trace()
    for i in range(3): # to be sure alias and indexes are removed
        es.indices.delete(index=INDEX_NAME, ignore=[400, 404])
        es.indices.delete_alias(index='_all',
            name=INDEX_NAME, ignore=[400, 404])

    create_index(INDEX_NAME + '_blue', USER_DATA, ES_DATA, MAPPING_FILE, GLOSSARY_FILE, RAW_EXPRESSION_FILE )
    put_alias(index_name=INDEX_NAME + '_blue', alias_name=INDEX_NAME)

@pytest.mark.run(after='test_create_index')
def test_inject_documents():
    inject_documents(INDEX_NAME, USER_DATA, DST_DIR, JSON_DIR,
                meta_path = META_DIR, sections=sections)

    res = es.get(index=INDEX_NAME, id=doc_guyane_eau)
    assert len(str(res)) > 1000, res

@pytest.mark.run(after='test_inject_documents')
def test_analyse_index():

    # create elasticsearch index

    indices = elasticsearch.client.IndicesClient(es)

    body = {
          "analyzer": "my_analyzer",
          "text": "Sans sa carte national d'identité, il est difficile de rentrer au MI"
        }

    res = indices.analyze(index = INDEX_NAME, body=body)
    print(res)
    print(' '.join([token['token'] for token in res['tokens']]))
    list_synonym = [token['token'] for token in res['tokens'] if token['type'] == 'SYNONYM']
    assert 'cni' in list_synonym, list_synonym

    body = {
          "analyzer": "my_analyzer",
          "text": "Jusqu'ici, les commandes publiques de la DCRFPN me sont inconnus"
        }


    res = indices.analyze(index = INDEX_NAME, body=body)
    print(res)
    print(' '.join([token['token'] for token in res['tokens']]))

    assert 'Jusqu' not in  str(res['tokens'])
    #import pdb; pdb.set_trace()
    assert 'commandepublique' in  str(res['tokens']), 'expression not taken into account'
    assert 'command' in  str(res['tokens']), 'expression remove command!'

@pytest.mark.run(after='test_inject_documents')
def test_search():
    glossary_file = Path(USER_DATA) / GLOSSARY_FILE
    expression_file = Path(USER_DATA) / RAW_EXPRESSION_FILE
    threshold_file = Path(USER_DATA) / THRESHOLD_FILE


    req = 'travail illegal'
    must = [{"query_string":{"fields":["titre","content"],"query":req}}]
    #import pdb; pdb.set_trace()
    time.sleep(2)
    res = search(must, [], [], INDEX_NAME, [],
                glossary_file = glossary_file,
                expression_file = expression_file,
                threshold_file = threshold_file)

    #print(hits, length_req, bande)
    assert  res['hits'][0]['_id'] == 'BF2016-08-16010-dfci.pdf', 'Found to result %s'%res['hits'][0]['_id']
    assert res['length']>= 2, res['length']
    assert not res['band']
    #import pdb; pdb.set_trace()
    # test expression
    req = "chiffre d'affaire"
    must = [{"query_string":{"fields":["titre","content"],"query":req}}]
    res = search(must, [], [], INDEX_NAME, [],
                glossary_file = glossary_file,
                expression_file = expression_file,
                threshold_file = threshold_file)
    assert res['hits'][0]['_score']  > 10, 'boosting no taken into account'



"""
@pytest.mark.run(after='test_search')
def test_index_file(index_name, pdf_file):
    # Index ignit_pnigitis inside USER_DATA
    DST_DIR = ''
    JSON_DIR = ''
    META_DIR = ''
    data = index_file(str(pdf_file), index_name, USER_DATA, DST_DIR, JSON_DIR, META_DIR)
    assert data['author'] == 'babar', data
"""
@pytest.mark.run(after='test_search')
def test_reindex(client, app, es, dummy_index):
    # test reindex after a change of synonym data without downtime, using alias
    # First test : change synonym analyser in index

    # test with very basic index
    es.indices.delete(index='dummy_index', ignore=[400, 404])
    # create index
    es.indices.create(index='dummy_index', body=dummy_index)
    # create alias
    #es.indices.delete_alias(index='dummy_index', name='dummy_alias',ignore=[400, 404])
    es.indices.put_alias(index='dummy_index', name='dummy_alias')

    # index a document
    name_document = 'babar'
    data = {'content' : 'celeste aime le chat mais pas le chien'}
    es.index(index='dummy_index', body=data, id=name_document)

    # change index setting
    dummy_index['settings']['analysis']['filter']['my_synonym']['synonyms'] += ["chien => loup"]

    #es.indices.close(index='dummy_index')
    #es.indices.put_settings(index='dummy_index',body=settings)
    #es.indices.open(index='dummy_index')

    es.indices.delete(index='dummy_index2', ignore=[400, 404])
    # create index
    es.indices.create(index='dummy_index2', body=dummy_index)
    # index a document
    es.index(index='dummy_index2', body=data, id=name_document)

    # change the index pointer of the alias
    es.indices.put_alias(index='dummy_index2', name='dummy_alias')
    es.indices.delete(index='dummy_index', ignore=[400, 404])

    import time
    time.sleep(1)

    # search lion in new index
    request = {'query' : {'match_phrase': {'content': 'lion'}}}
    res = es.search(index='dummy_alias', body=request)
    assert  res['hits']['hits'][0]['_id'] == 'babar', res

    # search loup  in new index
    request = {'query' : {'match_phrase': {'content': 'loup'}}}
    res = es.search(index='dummy_alias', body=request)
    assert  res['hits']['hits'][0]['_id'] == 'babar', res

@pytest.mark.run(after='test_reindex')
def test_blue_green():

    req = 'MI'
    """
    the user request is an acronym meaning "mistere interieur"
    test if blue index without acronym hits low result and
    green index hits documents with "mistere interieur"
    """
    # Clear
    es.indices.delete_alias(index=[INDEX_NAME+'_blue',INDEX_NAME+'_green'], name=INDEX_NAME, ignore=[400, 404])
    es.indices.delete(index=INDEX_NAME, ignore=[400, 404])

    # Create blue index without synonym
    create_index(INDEX_NAME + '_blue', USER_DATA, ES_DATA, MAPPING_FILE )

    put_alias(INDEX_NAME + '_blue', INDEX_NAME)
    old_index = get_index_name(INDEX_NAME)
    assert old_index == INDEX_NAME + '_blue', 'Alias get issue'

    # index time to blue
    inject_documents(old_index, USER_DATA, DST_DIR, JSON_DIR,
                meta_path = META_DIR)

    # Test search
    must = [{"query_string":{"fields":["titre","content"],"query":req}}]
    res_blue = search(must, [], [], INDEX_NAME, [])
    #print(hits, length_req, bande)
    time.sleep(2)
    assert [hits['_id'] for hits in res_blue['hits']] == \
         ['BF2014-08-13069 - Plan submersions rapides.pdf',
         'BF2014-01-13041 Dépenses de contentieux.pdf',
         'BF2015-09-14124 - Accueil ressortissants étrangers.pub.pdf'],\
                            'Found to result %s'%res_blue['hits'][0]['_id']
    print([hits['_id'] for hits in res_blue['hits']])

    ####  Switch to new index #####
    glossary_file = Path(USER_DATA) / GLOSSARY_FILE
    expression_file = Path(USER_DATA) / RAW_EXPRESSION_FILE

    # Create green index with synonym
    new_index = replace_blue_green(old_index, INDEX_NAME)
    assert new_index == INDEX_NAME + '_green', 'Alias get issue'

    create_index(new_index, USER_DATA, ES_DATA, MAPPING_FILE,
                GLOSSARY_FILE, RAW_EXPRESSION_FILE)

    # index time to green
    inject_documents(new_index, USER_DATA, DST_DIR, JSON_DIR,
                meta_path = META_DIR)

    # Switch index in alias
    put_alias(new_index, INDEX_NAME)
    delete_alias(old_index, INDEX_NAME)
    must = [{"multi_match":{"fields":["titre","content"],"query":req}}]
    res_green = search(must, [], [], INDEX_NAME, [],
                glossary_file = glossary_file,
                expression_file = expression_file)
    #import pdb; pdb.set_trace()
    # should be equal rather than in, but doesn't work with test_app.py. WHY??
    time.sleep(2)
    assert  'BF2015-15-15034-action-sociale-du-mi.pdf' in [hits['_id'] for hits in res_green['hits']], 'Found to result %s'%res_green['hits'][0]['_id']

    print([hits['_id'] for hits in res_green['hits']])


    assert get_alias(INDEX_NAME) == {INDEX_NAME + '_green': {'aliases': {INDEX_NAME: {}}}}


@pytest.mark.run(after='test_search')
def test_suggest():
    req = "travail ilegal"
    res = suggest(req, INDEX_NAME)
    assert [element['text'] for element in res] == ['travail illégal', 'travail inégal', 'travail légal']

def test_get_tag():
    document = 'BF2016-11-15132-sargasses.pub.pdf'
    fields = 'content'
    res = get_tag(INDEX_NAME, document, fields)
    assert res == ['d’échouages', 'sargasses']

if __name__ == '__main__':
    test_create_index()
    test_inject_documents()
    test_analyse_index()
    test_search()
