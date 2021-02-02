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
    assert len(json_data['comments']) == 2

    comment1 = json_data['comments'][0]
    assert comment1['id'] == 3
    assert comment1['user_id'] == 3
    assert comment1['recipe_id'] == 1
    assert comment1['content'] == 'Simmer dean'
    assert comment1['submitted_on'] == '2021-01-22T05:30:00Z'

    comment2 = json_data['comments'][1]
    assert comment2['id'] == 5
    assert comment2['user_id'] == 3
    assert comment2['recipe_id'] == 2
    assert comment2['content'] == 'He might have you beat @user1'
    assert comment2['submitted_on'] == '2021-01-24T08:45:00Z'


