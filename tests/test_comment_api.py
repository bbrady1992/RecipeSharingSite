from . import empty_db_client, populated_db_client

def test_get_nonexistent_comment(empty_db_client):
    rv = empty_db_client.get('/comments/555')
    assert rv.status_code == 404
    assert rv.get_data() == b'Comment with ID 555 not found'


def test_get_comment_that_exists(populated_db_client):
    rv = populated_db_client.get('/comments/1')
    assert rv.status_code == 200
    json_data = rv.get_json()

    assert json_data['id'] == 1
    assert json_data['content'] == 'This is gross'
    assert json_data['submitted_on'] == '2021-01-20T12:00:00Z'
    assert json_data['recipe_id'] == 1
    assert json_data['user_id'] == 2

