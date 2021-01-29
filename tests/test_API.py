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

"""
GET /users/
"""
def test_get_users(client):
    rv = client.get('/users/')
    assert rv.get_json() == {"users": []}

