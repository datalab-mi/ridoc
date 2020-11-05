import os
import pytest
from pathlib import Path

from elasticsearch import Elasticsearch

from application import create_app

section = [{'key': 'SITE', 'array':False},
            {'key': 'DIRECTION', 'array':False},
            {'key': 'DOMAINE', 'array':True},
            {'key': 'TITRE', 'array':True},
            {'key': 'Mots clés', 'array':True},
            {'key': 'Date', 'array':True},
            {'key': 'Question', 'array':True},
            {'key': 'Réponse', 'array':False},
            {'key': 'Pièces jointes', 'array':True},
            {'key': 'Liens', 'array':False},
            {'key': 'Références', 'array':False}]



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
