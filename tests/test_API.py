import os
import tempfile

import pytest

from RecipeSharingSite import create_app

@pytest.fixture
def client():
    db_fd, db_uri = tempfile.mkstemp(suffix='.sqlite')
    app = create_app('sqlite+pysqlite:///' + db_uri)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

    os.close(db_fd)

def test_GET_users(client):
    rv = client.get('/users/')
    assert b'GET /users/ (())' in rv.data

def test_GET_user_information(client):
    rv = client.get('/users/testuser/')
    assert b"GET /users/<user_name> (('testuser',))" in rv.data

