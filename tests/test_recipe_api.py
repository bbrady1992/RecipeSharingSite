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

