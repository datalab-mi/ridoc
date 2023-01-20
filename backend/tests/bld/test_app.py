import pytest
import json, os, time
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from tools.elastic import get_index_name, replace_blue_green, create_index, put_alias

env_path = '/app/tests/bld/.env-bld'
load_dotenv(dotenv_path=env_path, override=True)

INDEX_NAME = os.getenv('INDEX_NAME')

USER_DATA = os.getenv('USER_DATA')
ES_DATA = os.getenv('ES_DATA')

GLOSSARY_FILE = os.getenv('GLOSSARY_FILE')
RAW_EXPRESSION_FILE = os.getenv('RAW_EXPRESSION_FILE')
MAPPING_FILE =  os.getenv('MAPPING_FILE')

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


def test_auth_user(app, client):
    """Test without token
    """
    app.config
    response = client.get('/user/files')
    assert response.status_code == 200

def test_healthcheck(client, app):
    # test that viewing the page renders without template errors
    res = client.get("/healthcheck")
    print(res)
    assert res.status_code == 200,res

@pytest.mark.run(after='test_search')
@pytest.mark.parametrize("role", ['admin'])
def test_reindex(client, app, access_headers, file_name, form_to_upload, bad_form_to_upload):

    old_index = get_index_name(INDEX_NAME)
    new_index = replace_blue_green(old_index, INDEX_NAME)
    # add text extension document, reindex should return list of indexation error
    form_to_upload1 = form_to_upload.copy()
    resp = client.put(
            '/admin/files/odt/empty.txt',
            content_type = 'multipart/form-data',
            data = form_to_upload1,
            headers=access_headers)

    form_to_upload["mots cles"] = ''

    resp = client.put(
            '/admin/%s'%file_name,
            content_type = 'multipart/form-data',
            data = bad_form_to_upload,
            headers=access_headers)

    resp = client.get('/admin/%s/reindex'%INDEX_NAME, headers=access_headers)
    assert resp.json["log"][0] in [{'filename': 'ignit_pnigitis.pdf', 'msg': "failed to parse field [date] of type [date] in document with id 'ignit_pnigitis.pdf'. Preview of field's value: '14/1451-52'"},
                                {'filename': 'empty.txt', 'msg': 'Format not supported'}]
    assert resp.status_code == 200, 'Status Code : %s'%resp.status_code
    assert resp.json['color'] == new_index

    # clean and delete file
    resp = client.delete(
            '/admin/%s'%"empty.txt", headers=access_headers)

def test_search(client, app, search_data):
    with app.test_client() as c:
        resp = c.post(
            '/user/search',
            content_type='application/json',
            data = json.dumps(search_data))
    time.sleep(2)

    assert resp.status_code == 200, 'Status Code : %s'%resp.status_code

    res = json.loads(resp.get_data(as_text=False).decode('utf-8'))
    assert len(res)>0, "No document found"
    #import pdb; pdb.set_trace()
    assert [hits['_id'] for hits in res['hits']] == ['moteur de recherche.odt'], 'Find %s'%[hits['_id'] for hits in res['hits']]

@pytest.mark.parametrize("role", ['admin'])
def test_upload_file(client, app, form_to_upload, file_name, access_headers):
    # Add document
    resp = client.put(
            '/admin/%s'%file_name,
            content_type = 'multipart/form-data',
            data = form_to_upload,
            headers=access_headers)
    print( resp.get_json())
    assert resp.status_code in [200, 201], 'Status Code : %s, msg: %s'%(resp.status_code, resp.get_json())
    #import pdb; pdb.set_trace()

    # Delete document
    resp = client.delete(
            '/admin/%s'%file_name, headers=access_headers)

    assert resp.status_code == 204, 'Status Code : %s'%resp.status_code

@pytest.mark.parametrize("role", ['admin'])
def test_index_file(client, app, index_name, pdf_file, access_headers):
    # Add document
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

    assert resp.status_code in [200, 201, 202], 'Status Code : %s'%resp.status_code
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

    assert resp.status_code in [200, 201, 202], 'Status Code : %s'%resp.status_code
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

    assert resp.status_code in [200, 201, 202], 'Status Code : %s'%resp.status_code
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

def test_get_files(client, app):
    doc_name = "moteur de recherche"
    with app.test_client() as c:
        resp = c.get(
            '/user/files')
    assert resp.status_code == 200
    path = 'json/%s.json'% doc_name
    with app.test_client() as c:
        req = c.get(
            '/user/files/{path}'.format(path=path))
        resp = json.loads(req.get_data())
        #import pdb; pdb.set_trace()
        assert doc_name in resp['titre'].lower(), resp

@pytest.mark.run(after='test_reindex')
@pytest.mark.parametrize("role", ['admin'])
def test_threshold(client, app, access_headers):
    # Add display threshold to threshold.json
    thresholds = {"d_threshold":5,"r_threshold":5}
    resp = client.put('/admin/threshold',
            data = json.dumps(thresholds),
            headers=access_headers)

    # TODO: open THRESHOLD_FILE and test its content
    assert resp.status_code in [200, 201], 'Status Code : %s'%resp.status_code
