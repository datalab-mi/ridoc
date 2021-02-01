import pytest
import json, os, time
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from tools.elastic import get_index_name, replace_blue_green
from flask import request

env_path = '/app/tests/iga/.env-iga'
load_dotenv(dotenv_path=env_path, override=True)

INDEX_NAME = os.getenv('INDEX_NAME')

USER_DATA = os.getenv('USER_DATA')
ES_DATA = os.getenv('ES_DATA')

GLOSSARY_FILE = os.getenv('GLOSSARY_FILE')
EXPRESSION_FILE = os.getenv('EXPRESSION_FILE')
MAPPING_FILE =  os.getenv('MAPPING_FILE')
THRESHOLDS = os.getenv('THRESHOLDS')

PDF_DIR = os.getenv('PDF_DIR')
JSON_DIR = os.getenv('JSON_DIR')

@pytest.mark.parametrize("role", ['admin', 'user', 'visitor'])
def test_auth_admin(app, client, access_headers, role):
    app.config
    response = client.get('/admin/cluster', headers=access_headers)
    if role in ['visitor', 'user']:
        expected_json = {'msg': 'Admins only, you are %s'%role}
        assert response.status_code == 403
        assert response.get_json() == expected_json, response.get_json()
    elif role == 'admin':
        assert response.status_code == 200

@pytest.mark.parametrize("role", ['admin', 'user', 'visitor'])
def test_auth_user(app, client, access_headers, role):
    app.config
    response = client.get('/user/files', headers=access_headers)
    if role in ['visitor']:
        expected_json = {'msg': 'Admins or users only, you are %s'%role}
        assert response.status_code == 403
        assert response.get_json() == expected_json, response.get_json()
    elif role in ['admin', 'user']:
        assert response.status_code == 200

@pytest.mark.parametrize("role", ['admin'])
def test_authorized_resource(app, client, access_headers, role):
    app.config
    response = client.get('/authorized_resource', headers=access_headers)
    assert response.status_code == 200
    assert response.json == {'rules': ['visitor', 'user', 'admin'], 'role': 'admin'}
    faked_headers = {"Authorization": 'Bearer faked'}
    faked_response = client.get('/authorized_resource', headers=faked_headers)
    assert faked_response.status_code == 422
    no_header_response = client.get('/authorized_resource')
    assert no_header_response.status_code == 200
    assert no_header_response.json == {'rules': ['visitor'], 'role': 'visitor'}, no_header_response.json
    role_response = client.get('/authorized_resource/admin')
    assert role_response.json == {'resources': ['search', 'glossary', 'expression', 'admin', 'description', 'notice'], 'rules': ['visitor', 'user', 'admin']}, role_response.json



def test_healthcheck(client, app):
    # test that viewing the page renders without template errors
    res = client.get("/healthcheck")
    print(res)
    assert res.status_code == 200,res

@pytest.mark.parametrize("role", ['admin'])
def test_reindex(client, app, access_headers):

    old_index = get_index_name(INDEX_NAME)
    new_index = replace_blue_green(old_index, INDEX_NAME)

    with app.test_client() as c:
        resp = c.get(
            '/admin/%s/reindex'%INDEX_NAME,
            headers=access_headers)

    assert resp.status_code == 200, 'Status Code : %s'%resp.status_code
    assert resp.json['color'] == new_index

@pytest.mark.parametrize("role", ['admin'])
def test_search(client, app, access_headers, search_data):
    with app.test_client() as c:
        resp = c.post(
            '/user/search',
            content_type='application/json',
            data=json.dumps(search_data),
            headers=access_headers)

    assert resp.status_code == 200, 'Status Code : %s'%resp.status_code

    res= json.loads(
            resp.get_data(as_text=False).decode('utf-8'))

    assert len(res)>0, "No document found"
    #import pdb; pdb.set_trace()
    time.sleep(2)
    assert [hits['_id'] for hits in res['hits']] == ['BF2016-08-16010-dfci.pdf'], 'Find %s'%[hits['_id'] for hits in res['hits']]

@pytest.mark.parametrize("role", ['admin'])
def test_threshold(client, app, access_headers):
    # Add display threshold to threshold.json
    thresholds = {"d_threshold": 1, "r_threshold": 1}
    with app.test_client() as c:
        resp = c.put('/admin/threshold',
            data = json.dumps(thresholds),
            headers=access_headers)

    # TODO: open THRESHOLD_FILE and test its content
    assert resp.status_code in [200, 201], 'Status Code : %s'%resp.status_code

@pytest.mark.parametrize("role", ['admin'])
def test_upload_file(client, app, form_to_upload, access_headers):
    # Add document
    resp = client.put(
            '/admin/%s'%form_to_upload['filename'],
            content_type = 'multipart/form-data',
            data = form_to_upload,
            headers=access_headers)

    assert resp.status_code in [200, 201], 'Status Code : %s'%resp.status_code

    # Delete document
    resp = client.delete(
            '/admin/%s'%form_to_upload['filename'],
            headers=access_headers)

    assert resp.status_code == 204, 'Status Code : %s'%resp.status_code

@pytest.mark.parametrize("role", ['admin'])
def test_index_file(client, app, index_name, pdf_file, access_headers):
    # Index document
    resp = client.put(
            '/admin/{index_name}/_doc/{filename}'.format(
                index_name=index_name,
                filename=pdf_file
                ),
            headers=access_headers)

    assert resp.status_code in [200, 201], 'Status Code : %s'%resp.status_code

    # Delete document
    resp = client.delete(
            '/admin/{index_name}/_doc/{filename}'.format(
                index_name=index_name,
                filename=pdf_file
                ),
            headers=access_headers)

    assert resp.status_code == 200, 'Status Code : %s'%resp.status_code

@pytest.mark.parametrize("role", ['admin'])
def test_synonym(client, app, access_headers):
    # Add synonym
    filename = 'glossaire'
    synonym_file = Path(app.config['USER_DATA']) / (filename + '.txt')
    names = ['expressionB','expressionA']
    sep = ' => '
    key = 0
    body = {"expressionA":"dnum","expressionB":"Direction du numérique"}
    res_body = {"expressionA":"_DNUM_","expressionB":"direction numerique"}

    resp = client.put(
            '/admin/synonym/{key}?filename={filename}'.format(
                key=key,
                filename=filename),
            data = json.dumps(body),
            headers=access_headers)
#import pdb; pdb.set_trace()

    assert resp.status_code in [200, 201], 'Status Code : %s'%resp.status_code
    synonym_df = pd.read_csv(synonym_file, sep=sep,header=None, names=names)
    #import  pdb; pdb.set_trace()
    assert synonym_df.iloc[0].to_dict() == res_body

    # Delete synonym
    key = 1
    resp = client.delete(
            '/admin/synonym/{key}?filename={filename}'.format(
                key=key,
                filename=filename),
            headers=access_headers)

    assert resp.status_code in [200, 201], 'Status Code : %s'%resp.status_code
    synonym_df = pd.read_csv(synonym_file, sep=sep,header=None, names=names)
    #import  pdb; pdb.set_trace()
    assert synonym_df.iloc[0].to_dict() != res_body

@pytest.mark.parametrize("role", ['admin'])
def test_expression(client, app, access_headers):
    # Add synonym
    filename = 'raw_expression'
    synonym_file = Path(app.config['USER_DATA']) / (filename + '.txt')
    names = ['expressionA']
    sep = ';'

    key = 0
    body = {"expressionA":"Direction du numérique"}
    res_body = {"expressionA":"DIRECTION NUMERIQUE"}

    resp = client.put(
            '/admin/synonym/{key}?filename={filename}'.format(
                key=key,
                filename=filename),
            data = json.dumps(body),
            headers=access_headers)


    assert resp.status_code in [200, 201], 'Status Code : %s'%resp.status_code
    synonym_df = pd.read_csv(synonym_file, sep=sep,header=None, names=names)
    #import  pdb; pdb.set_trace()
    assert synonym_df.iloc[0].to_dict() == res_body

    # Delete synonym
    key = 1
    resp = client.delete(
            '/admin/synonym/{key}?filename={filename}'.format(
                key=key,
                filename=filename),
            headers=access_headers)


    assert resp.status_code in [200, 201], 'Status Code : %s'%resp.status_code
    synonym_df = pd.read_csv(synonym_file, sep=sep,header=None, names=names)
    #import  pdb; pdb.set_trace()
    assert synonym_df.iloc[0].to_dict() != res_body
