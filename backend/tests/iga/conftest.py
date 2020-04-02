import os

import pytest

from application import create_app

NOM_INDEX = 'iga'

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
def search_data():
    return dict(index_name=NOM_INDEX, value='travail illegal')
