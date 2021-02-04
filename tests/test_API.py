from . import empty_db_client, populated_db_client
#def test_get_recipes_for_nonexistent_user(empty_db_client):
#    rv = empty_db_client.get('/users/TestUser1/recipes/')
#    assert rv.status_code == 404
#    assert rv.get_data() == b"User TestUser1 not found"
#
#def test_get_recipes_for_existing_user(populated_db_client):
#    rv = populated_db_client.get('/users/TestUser1/recipes/')
#    assert rv.status_code == 200
#    json_data = rv.get_json()
#    assert len(json_data) == 3
#    assert json_data["user_id"] == 1
#    assert json_data["total_recipes"] == len(json_data["recipes"]) == 1
#    recipe1 = json_data["recipes"][0]
#    assert recipe1["id"] == 1
#    assert recipe1["name"] == "Test Recipe 1"
#    assert recipe1["submitted_on"] == "2021-01-20"
#
#def test_get_recipe(populated_db_client):
#    rv = populated_db_client.get('/recipes/1/')
#    assert rv.status_code == 200
#    json_data = rv.get_json()
#    assert len(json_data) == 8
#    assert json_data["id"] == 1
#    assert json_data["name"] == "Test Recipe 1"
#    assert json_data["submitted_on"] == "2021-01-20"
#    assert json_data["prep_time_minutes"] == 10
#    assert json_data["cook_time_minutes"] == 25
#    assert json_data["user"] == "TestUser1"
#    assert len(json_data["ingredients"]) == 2
#    assert json_data["ingredients"][0]["ingredient"] == "Canned tomatoes"
#    assert json_data["ingredients"][0]["amount"] == 1
#    assert json_data["ingredients"][0]["units"] == "can"
#    assert json_data["ingredients"][1]["ingredient"] == "Cumin powder"
#    assert json_data["ingredients"][1]["amount"] == 2
#    assert json_data["ingredients"][1]["units"] == "Tbsp"
#    assert len(json_data["steps"]) == 3
#    assert json_data["steps"][0]["number"] == 1
#    assert json_data["steps"][0]["content"] == "Take out the ingredients"
#    assert json_data["steps"][1]["number"] == 2
#    assert json_data["steps"][1]["content"] == "Cook the ingredients"
#    assert json_data["steps"][2]["number"] == 3
#    assert json_data["steps"][2]["content"] == "Eat the meal"
#
#    rv = populated_db_client.get('/recipes/55/')
#    assert rv.status_code == 404
#    assert rv.get_data() == b"Recipe 55 not found"
#
#
#
#"""
#Comments
#"""
#
#def test_get_comments_for_user(populated_db_client):
#    rv = populated_db_client.get('/users/TestUser3/comments/')
#    assert rv.status_code == 200
#    json_data = rv.get_json()
#    print("test_get_comments_for_existing_user: {}".format(json_data))
#    assert len(json_data) == 3
#    assert json_data["user_id"] == 3
#    assert json_data["total_comments"] == len(json_data["comments"]) == 2
#
#    comment1 = json_data["comments"][0]
#    assert comment1["id"] == 3
#    assert comment1["recipe_id"] == 1
#    assert comment1["content"] == "Simmer dean"
#    assert comment1["submitted_on"] == "2021-01-22T05:30:00"
#
#    comment2 = json_data["comments"][1]
#    assert comment2["id"] == 5
#    assert comment2["recipe_id"] == 2
#    assert comment2["content"] == "He might have you beat @user1"
#    assert comment2["submitted_on"] == "2021-01-24T08:45:00"
#
#    rv = populated_db_client.get('/users/nonexistentuser/comments/')
#    assert rv.status_code == 404
#    assert rv.get_data() == b"User nonexistentuser not found"
#
#def test_delete_comment(populated_db_client):
#    rv = populated_db_client.delete('/comments/1/')
#    assert rv.status_code == 204
#    assert rv.get_data() == b''
#
#    rv = populated_db_client.delete('/comments/55/')
#    assert rv.status_code == 404
#    assert rv.get_data() == b"Comment 55 not found"
#
#