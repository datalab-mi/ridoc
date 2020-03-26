import pytest

USER_DATA = 'tests/iga/data'
ES_DATA = '/usr/share/elasticsearch/data/extra/iga'

GLOSSARY_FILE = 'glossaire.txt'
EXPRESSION_FILE = 'expression.txt'
MAPPING_FILE = 'map.json'

PDF_DIR = 'pdf'
JSON_DIR = 'json'

NOM_INDEX = 'iga'

def test_healthcheck(client, app):
    # test that viewing the page renders without template errors
    res = client.get("user/healthcheck")
    print(res)
    assert res.status_code == 200,res

    res = client.get("admin/cluster")
    import pdb; pdb.set_trace()
    print(res.body)
    assert res.status_code == 200,res
