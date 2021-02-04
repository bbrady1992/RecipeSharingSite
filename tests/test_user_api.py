from . import empty_db_client, populated_db_client
from datetime import date

def test_get_users_when_empty(empty_db_client):
    rv = empty_db_client.get('/users')
    assert rv.status_code == 308

    rv = empty_db_client.get('/users/')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert len(json_data) == 1
    assert json_data['users'] == []

def test_get_users_when_nonempty(populated_db_client):
    rv = populated_db_client.get('/users/')
    assert rv.status_code == 200
    json_data = rv.get_json()

    assert len(json_data) == 1
    assert len(json_data['users']) == 3

    user1 = json_data['users'][0]
    assert user1['id'] == 1
    assert user1['name'] == 'TestUser1'
    assert user1['email'] == 'testuser1@gmail.com'
    assert 'password' not in user1.keys()
    assert user1['recipes'] == [{'id': 1}]
    assert user1['comments'] == [{'id': 2}, {'id': 6}]
    assert user1['joined_on'] == '2000-06-23'

    user2 = json_data['users'][1]
    assert user2['id'] == 2
    assert user2['name'] == 'TestUser2'
    assert user2['email'] == 'TU2@gmail.com'
    assert 'password' not in user2.keys()
    assert user2['recipes'] == [{'id': 2}]
    assert user2['comments'] == [{'id': 1}, {'id': 4}]
    assert user2['joined_on'] == '1992-10-05'

    user3 = json_data['users'][2]
    assert user3['id'] == 3
    assert user3['name'] == 'TestUser3'
    assert user3['email'] == 'TestUser3@gmail.com'
    assert 'password' not in user3.keys()
    assert user3['recipes'] == []
    assert user3['comments'] == [{'id': 3}, {'id': 5}]
    assert user3['joined_on'] == '2021-01-20'


def test_get_user_information(populated_db_client):
    # Test getting a nonexistent user
    rv = populated_db_client.get('/users/100')
    assert rv.status_code == 404
    assert rv.get_data() == b'User with ID 100 not found'

    rv = populated_db_client.get('/users/1')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert len(json_data) == 6
    assert json_data['id'] == 1
    assert json_data['email'] == 'testuser1@gmail.com'
    assert json_data['name'] == 'TestUser1'
    assert 'password' not in json_data.keys()
    assert json_data['joined_on'] == '2000-06-23'
    assert json_data['recipes'] == [{'id': 1}]
    assert json_data['comments'] == [{'id': 2}, {'id': 6}]


def test_add_user(empty_db_client):
    rv = empty_db_client.post('/users/', json={
        'name': 'AddedDuringTest',
        'email': 'addedduringtest-55@yahoo.com',
        'password': 'NewUserPassword!@#'
    })
    assert rv.status_code == 201

    json_data = rv.get_json()
    assert json_data['id'] == 1
    assert json_data['email'] == 'addedduringtest-55@yahoo.com'
    assert json_data['name'] == 'AddedDuringTest'
    assert 'password' not in json_data.keys()
    assert json_data['recipes'] == []
    assert json_data['comments'] == []
    assert json_data['joined_on'] == date.today().isoformat()


    rv = empty_db_client.post('/users/', json={
        'name': 'laksnf',
        'email': 'a2n49sk@@5-+@net.net'
    })
    assert rv.status_code == 400


def test_delete_user(populated_db_client):
    rv = populated_db_client.delete('/users/555')
    assert rv.status_code == 404
    assert rv.get_data() == b'User with ID 555 not found'

    rv = populated_db_client.delete('/users/1')
    assert rv.status_code == 204
    assert rv.get_data() == b''


def test_get_comments_made_by_user(populated_db_client):
    rv = populated_db_client.get('/users/555/comments')
    assert rv.status_code == 404
    assert rv.get_data() == b'User with ID 555 not found'

    rv = populated_db_client.get('/users/3/comments')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert len(json_data) == 1
    assert json_data['comment_ids'] == [
        {'id': 3},
        {'id': 5}
    ]

def test_get_recipes_submitted_by_user(populated_db_client):
    rv = populated_db_client.get('/users/555/recipes')
    assert rv.status_code == 404
    assert rv.get_data() == b'User with ID 555 not found'

    rv = populated_db_client.get('/users/1/recipes')
    assert rv.status_code == 200
    assert len(rv.get_json()) == 1
    assert rv.get_json() == {'recipe_ids': [{'id': 1}]}



def test_update_nonexistent_user(populated_db_client):
    rv = populated_db_client.put('/users/555', json={
        'name': 'noname',
        'email': 'noemail@email.com'
    })
    assert rv.status_code == 404
    assert rv.get_data() == b'User with ID 555 not found'


def test_update_fails_with_bad_request(populated_db_client):
    rv = populated_db_client.put('/users/1')
    assert rv.status_code == 400
    assert rv.get_data() == b''


def test_update_user_with_same_info_in_db(populated_db_client):
    rv = populated_db_client.put('/users/1', json={
        'name': 'TestUser1',
        'email': 'testuser1@gmail.com'
    })
    assert rv.status_code == 204

def test_update_user_name_only(populated_db_client):
    rv = populated_db_client.put('/users/1', json={
        'name': 'newusernamefortu1'
    })
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['name'] == 'newusernamefortu1'
    assert json_data['email'] == 'testuser1@gmail.com'


def test_update_user_email_only(populated_db_client):
    rv = populated_db_client.put('/users/2', json={
        'email': 'tu2email@gmail.com'
    })
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['name'] == 'TestUser2'
    assert json_data['email'] == 'tu2email@gmail.com'

def test_update_all_user_info(populated_db_client):
    rv = populated_db_client.put('/users/3', json={
        'name': 'User3ForTesting',
        'email': 'newuser3email@yahoo.com'
    })
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['name'] == 'User3ForTesting'
    assert json_data['email'] == 'newuser3email@yahoo.com'
