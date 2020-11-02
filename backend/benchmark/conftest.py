import os
import pytest
from pathlib import Path

from elasticsearch import Elasticsearch

from application import create_app

INDEX_NAME = 'bld'

USER_DATA = '/benchmark/bld/data'
filename = 'moteur de recherche.odt'

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    app = create_app()
    yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()



@pytest.fixture
def dummy_index():
    return {
          "settings": {
            "analysis": {
              "filter" : {
                "my_synonym": {
                  "type": "synonym",
                  "synonyms": [
                    "chat => lion"
                      ]
                  }
            },
              "analyzer": {
                "my_analyzer": {
                  "tokenizer": "standard",
                  "filter": [
                    "my_synonym"
                    ]
                  }
                }
            }
          },
          "mappings":{
              "properties": {
                 "content": {
                    "type": "text",
                    "analyzer" : "my_analyzer",
                    "search_analyzer" : "my_analyzer"
                }
              }
            }
        }



@pytest.fixture
def sections():
    yield [{'key': 'SITE', 'array':False},
            {'key': 'DIRECTION', 'array':False},
            {'key': 'DOMAINE', 'array':False},
            {'key': 'TITRE', 'array':False},
            {'key': 'Mots clés', 'array':True},
            {'key': 'Date', 'array':False},
            {'key': 'Question', 'array':False},
            {'key': 'Réponse', 'array':False},
            {'key': 'Réponse', 'array':False},
            {'key': 'Pièces jointes', 'array':True},
            {'key': 'Liens', 'array':False},
            {'key': 'Références', 'array':False}
            ]
