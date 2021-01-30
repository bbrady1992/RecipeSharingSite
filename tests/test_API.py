import os
import tempfile

import pytest

from RecipeSharingSite import create_app, db

from RecipeSharingSite.models.comment import Comment
from RecipeSharingSite.models.ingredient import Ingredient
from RecipeSharingSite.models.recipe import Recipe
from RecipeSharingSite.models.RecipeIngredient import RecipeIngredient
from RecipeSharingSite.models.recipestep import RecipeStep
from RecipeSharingSite.models.user import User


@pytest.fixture
def empty_db_client():
    db_fd, db_uri = tempfile.mkstemp(suffix='.sqlite')
    app = create_app('sqlite+pysqlite:///' + db_uri)
    app.config['TESTING'] = True
    with app.test_client() as empty_db_client:
        yield empty_db_client

    os.close(db_fd)


@pytest.fixture
def populated_db_client():
    db_fd, db_uri = tempfile.mkstemp(suffix='.sqlite')
    app = create_app('sqlite+pysqlite:///' + db_uri)
    app.config['TESTING'] = True

    user1 = User()
    user1.name = "Test User 1"
    user1.email = "testuser1@gmail.com"
    user1.password = "testpasswordhash"

    recipe1 = Recipe()
    recipe1.user = user1
    recipe1.name = "Test Recipe 1"
    recipe1.prep_time_minutes = 10
    recipe1.cook_time_minutes = 25
    recipe1.steps.append(RecipeStep(1, "Take out the ingredients"))
    recipe1.steps.append(RecipeStep(2, "Cook the ingredients"))
    tomatoes = Ingredient("Tomatoes")
    r1_ingredient1 = RecipeIngredient(tomatoes.id, 1, "can")
    recipe1.ingredients.append(r1_ingredient1)

    recipe2 = Recipe()
    recipe2.user = user1
    recipe2.name = "Test Recipe 2"
    recipe2.prep_time_minutes = 20
    recipe2.cook_time_minutes = 50
    recipe2.steps.append(RecipeStep(1, "Remove pre-cooked meal"))
    recipe2.steps.append(RecipeStep(2, "Eat it"))

    with app.app_context():
        db.session.add(user1)
        db.session.add(tomatoes)
        db.session.add(r1_ingredient1)
        db.session.add(recipe1)
        db.session.add(recipe2)

        db.session.commit()
    with app.test_client() as populated_db_client:
        yield populated_db_client

    os.close(db_fd)



"""
GET /users/
"""
def test_get_users_when_empty(empty_db_client):
    rv = empty_db_client.get('/users/')
    json_data = rv.get_json()
    assert len(json_data) == 1
    assert json_data["users"] == []

def test_get_users_when_nonempty(populated_db_client):
    rv = populated_db_client.get('/users/')
    json_data = rv.get_json()
    print("JSON data for test_get_users_when_nonempty: '{}'".format(json_data))
    assert len(json_data) == 1
    assert len(json_data["users"]) == 1
    user = json_data["users"][0]
    print("User data is: '{}'".format(user))
    assert user["name"] == "Test User 1"
    assert user["email"] == "testuser1@gmail.com"
    assert "password" not in user.keys()

def test_recipes_when_empty(empty_db_client):
    rv = empty_db_client.get('/recipes/')
    json_data = rv.get_json()
    assert len(json_data) == 1
    assert json_data["recipes"] == []

def test_recipes_when_nonempty(populated_db_client):
    rv = populated_db_client.get('/recipes/')
    json_data = rv.get_json()
    print("JSON data for test_recipes_when_nonempty: '{}'".format(json_data))
    assert len(json_data) == 2



