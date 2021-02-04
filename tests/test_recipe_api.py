from . import empty_db_client, populated_db_client

def test_get_recipes_when_empty(empty_db_client):
    rv = empty_db_client.get('/recipes')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert len(json_data) == 1
    assert json_data["recipes"] == []

def test_get_recipes(populated_db_client):
    rv = populated_db_client.get('/recipes')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert len(json_data) == 1
    assert len(json_data["recipes"]) == 2

    recipe1 = json_data["recipes"][0]
    assert recipe1['name'] == 'Test Recipe 1'
    assert recipe1['prep_time_minutes'] == 10
    assert recipe1['cook_time_minutes'] == 25
    assert recipe1['submitted_on'] == '2021-01-20'
    assert recipe1['user_id'] == 1
    assert recipe1['comments'] == [{'id': 1}, {'id': 2}, {'id': 3}]
    assert recipe1['ingredients'] == [
        {'ingredient': {'name': 'Canned tomatoes'}, 'amount': 1, 'units': 'can'},
        {'ingredient': {'name': 'Cumin powder'}, 'amount': 2, 'units': 'Tbsp'}
    ]
    assert recipe1['steps'] == [
        {'number': 1, 'content': 'Take out the ingredients'},
        {'number': 2, 'content': 'Cook the ingredients'},
        {'number': 3, 'content': 'Eat the meal'}
    ]

    recipe2 = json_data["recipes"][1]
    assert recipe2['name'] == 'Test Recipe 2'
    assert recipe2['prep_time_minutes'] == 25
    assert recipe2['cook_time_minutes'] == 50
    assert recipe2['submitted_on'] == '2021-01-21'
    assert recipe2['user_id'] == 2
    assert recipe2['comments'] == [{'id': 4}, {'id': 5}, {'id': 6}]
    assert recipe2['ingredients'] == [
        {'ingredient': {'name': 'Ribeye'}, 'amount': 14, 'units': 'oz'},
        {'ingredient': {'name': 'Salt'}, 'amount': 1, 'units': 'Tsp'},
        {'ingredient': {'name': 'Pepper'}, 'amount': 1.5, 'units': 'Tsp'}
    ]
    assert recipe2['steps'] == [
        {'number': 1, 'content': 'Thaw meat'},
        {'number': 2, 'content': 'Season meat'},
        {'number': 3, 'content': 'Cook meat'},
        {'number': 4, 'content': 'Let sit for 5 minutes, then serve'},
    ]
