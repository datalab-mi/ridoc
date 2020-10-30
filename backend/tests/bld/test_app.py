import pytest
import json, os, time
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from tools.elastic import get_index_name, replace_blue_green, create_index, put_alias

import elasticsearch
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'elasticsearch', 'port': '9200'}])

import elasticsearch
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'elasticsearch', 'port': '9200'}])

env_path = '/app/tests/iga/.env-iga'
load_dotenv(dotenv_path=env_path)

INDEX_NAME = os.getenv('INDEX_NAME')

USER_DATA = os.getenv('USER_DATA')
ES_DATA = os.getenv('ES_DATA')

GLOSSARY_FILE = os.getenv('GLOSSARY_FILE')
RAW_EXPRESSION_FILE = os.getenv('RAW_EXPRESSION_FILE')
MAPPING_FILE =  os.getenv('MAPPING_FILE')

PDF_DIR = os.getenv('PDF_DIR')
JSON_DIR = os.getenv('JSON_DIR')


def test_healthcheck(client, app):
    # test that viewing the page renders without template errors
    res = client.get("user/healthcheck")
    print(res)
    assert res.status_code == 200,res

def test_reindex(client, app):
    # Clear
    for i in range(3): # to be sure alias and indexes are removed
        es.indices.delete(index=INDEX_NAME, ignore=[400, 404])
        es.indices.delete(index=INDEX_NAME + '_green', ignore=[400, 404])
        es.indices.delete(index=INDEX_NAME + '_blue', ignore=[400, 404])
        es.indices.delete_alias(index=[INDEX_NAME + '_blue', INDEX_NAME + '_green'],
            name=INDEX_NAME, ignore=[400, 404])

    create_index(INDEX_NAME + '_blue', USER_DATA, ES_DATA, MAPPING_FILE, GLOSSARY_FILE, RAW_EXPRESSION_FILE )
    put_alias(INDEX_NAME + '_blue', INDEX_NAME)

    for i in range(3):
        es.indices.delete_alias(index=[new_index],
                name=INDEX_NAME, ignore=[400, 404])

    with app.test_client() as c:
        resp = c.get(
            '/admin/%s/reindex'%INDEX_NAME)

    assert resp.status_code == 200, 'Status Code : %s'%resp.status_code
    assert resp.json['color'] == INDEX_NAME + '_green'

def test_search(client, app, search_data):
    with app.test_client() as c:
        resp = c.post(
            '/common/search',
            content_type='application/json',
            data = json.dumps(search_data))

    assert resp.status_code == 200, 'Status Code : %s'%resp.status_code

    res= json.loads(
            resp.get_data(as_text=False).decode('utf-8'))

    assert len(res)>0, "No document found"
    #import pdb; pdb.set_trace()
    time.sleep(2)
    assert [hits['_id'] for hits in res['hits']] == ['BF2016-08-16010-dfci.pdf'], 'Find %s'%[hits['_id'] for hits in res['hits']]

def test_upload_file(client, app, form_to_upload, file_name):
    # Add document
    with app.test_client() as c:
        resp = c.put(
            '/admin/%s'%file_name,
            content_type = 'multipart/form-data',
            data = form_to_upload)

    assert resp.status_code in [200, 201], 'Status Code : %s'%resp.status_code
    #import pdb; pdb.set_trace()

    # Delete document
    with app.test_client() as c:
        resp = c.delete(
            '/admin/%s'%file_name)

    assert resp.status_code == 204, 'Status Code : %s'%resp.status_code

def test_index_file(client, app, index_name, pdf_file):
    # Add document
    with app.test_client() as c:
        resp = c.put(
            '/admin/{index_name}/_doc/{filename}'.format(
            index_name=index_name,
            filename=pdf_file
            ))

    assert resp.status_code in [200, 201], 'Status Code : %s'%resp.status_code

    # Delete document
    with app.test_client() as c:
        resp = c.delete(
            '/admin/{index_name}/_doc/{filename}'.format(
            index_name=index_name,
            filename=pdf_file
            ))

    assert resp.status_code == 200, 'Status Code : %s'%resp.status_code

def test_synonym(client, app):
    # Add synonym
    filename = 'glossaire'
    synonym_file = Path(app.config['USER_DATA']) / (filename + '.txt')
    names = ['expressionB','expressionA']
    sep = ' => '
    key = 0
    body = {"expressionA":"dnum","expressionB":"Direction du numérique"}
    res_body = {"expressionA":"_DNUM_","expressionB":"direction numerique"}

    with app.test_client() as c:
        resp = c.put(
            '/admin/synonym/{key}?filename={filename}'.format(
            key=key,
            filename=filename),
            data = json.dumps(body))

    assert resp.status_code in [200, 201], 'Status Code : %s'%resp.status_code
    synonym_df = pd.read_csv(synonym_file, sep=sep,header=None, names=names)
    #import  pdb; pdb.set_trace()
    assert synonym_df.iloc[0].to_dict() == res_body

    # Delete synonym
    key = 1
    with app.test_client() as c:
        resp = c.delete(
            '/admin/synonym/{key}?filename={filename}'.format(
            key=key,
            filename=filename))

    assert resp.status_code in [200, 201], 'Status Code : %s'%resp.status_code
    synonym_df = pd.read_csv(synonym_file, sep=sep,header=None, names=names)
    #import  pdb; pdb.set_trace()
    assert synonym_df.iloc[0].to_dict() != res_body

def test_expression(client, app):
    # Add synonym
    filename = 'raw_expression'
    synonym_file = Path(app.config['USER_DATA']) / (filename + '.txt')
    names = ['expressionA']
    sep = ';'

    key = 0
    body = {"expressionA":"Direction du numérique"}
    res_body = {"expressionA":"DIRECTION NUMERIQUE"}

    with app.test_client() as c:
        resp = c.put(
            '/admin/synonym/{key}?filename={filename}'.format(
            key=key,
            filename=filename),
            data = json.dumps(body))

    assert resp.status_code in [200, 201], 'Status Code : %s'%resp.status_code
    synonym_df = pd.read_csv(synonym_file, sep=sep,header=None, names=names)
    #import  pdb; pdb.set_trace()
    assert synonym_df.iloc[0].to_dict() == res_body

    # Delete synonym
    key = 1
    with app.test_client() as c:
        resp = c.delete(
            '/admin/synonym/{key}?filename={filename}'.format(
            key=key,
            filename=filename))

    assert resp.status_code in [200, 201], 'Status Code : %s'%resp.status_code
    synonym_df = pd.read_csv(synonym_file, sep=sep,header=None, names=names)
    #import  pdb; pdb.set_trace()
    assert synonym_df.iloc[0].to_dict() != res_body

def test_get_files(client, app):
    doc_name = "moteur de recherche"
    with app.test_client() as c:
        resp = c.get(
            '/common/files')
    assert resp.status_code == 200
    path = 'json/%s.json'% doc_name
    with app.test_client() as c:
        req = c.get(
            '/common/files/{path}'.format(path=path))
        resp = json.loads(req.get_data())
        assert doc_name in resp['titre'], resp
