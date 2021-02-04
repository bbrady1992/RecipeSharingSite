from . import empty_db_client, populated_db_client

def test_get_recipes_when_empty(empty_db_client):
    rv = empty_db_client.get('/recipes')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert len(json_data) == 1
    assert json_data["recipe_ids"] == []

def test_get_recipes(populated_db_client):
    rv = populated_db_client.get('/recipes')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert len(json_data) == 1
    assert len(json_data["recipe_ids"]) == 2

    assert json_data["recipe_ids"] == [
        {'id': 1},
        {'id': 2}
    ]

def test_get_recipe_by_id(populated_db_client):
    rv = populated_db_client.get('/recipes/555')
    assert rv.status_code == 404
    assert rv.get_data() == b'Recipe with ID 555 not found'

    rv = populated_db_client.get('/recipes/1')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['name'] == 'Test Recipe 1'
    assert json_data['prep_time_minutes'] == 10
    assert json_data['cook_time_minutes'] == 25
    assert json_data['submitted_on'] == '2021-01-20'
    assert json_data['user_id'] == 1
    assert json_data['comments'] == [{'id': 1}, {'id': 2}, {'id': 3}]
    assert json_data['ingredients'] == [
        {'ingredient': {'name': 'Canned tomatoes'}, 'amount': 1, 'units': 'can'},
        {'ingredient': {'name': 'Cumin powder'}, 'amount': 2, 'units': 'Tbsp'}
    ]
    assert json_data['steps'] == [
        {'number': 1, 'content': 'Take out the ingredients'},
        {'number': 2, 'content': 'Cook the ingredients'},
        {'number': 3, 'content': 'Eat the meal'}
    ]

def test_delete_recipe(populated_db_client):
    rv = populated_db_client.delete('/recipes/555')
    assert rv.status_code == 404
    assert rv.get_data() == b'Recipe with ID 555 not found'

    rv = populated_db_client.delete('/recipes/1')
    assert rv.status_code == 204


def test_get_comments_for_recipe(populated_db_client):
    rv = populated_db_client.get('/recipes/555/comments')
    assert rv.status_code == 404
    assert rv.get_data() == b'Recipe with ID 555 not found'

    rv = populated_db_client.get('/recipes/1/comments')
    assert rv.status_code == 200
    assert rv.get_json() == {'comment_ids': [
        {'id': 1},
        {'id': 2},
        {'id': 3}
    ]}
