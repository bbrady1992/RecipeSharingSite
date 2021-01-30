import os
import tempfile

import pytest
from flask_api import status

from pprint import pprint

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

    user1 = User(name="Test User 1", email="testuser1@gmail.com", password="tu3passwordhash")
    user2 = User(name="Test User 2", email="TU2@gmail.com", password="tu2passwordhash")
    user3 = User(name="Test User 3", email="TestUser3@gmail.com", password="tu3passwordhash")

    """
    Recipe 1
    """
    recipe1 = Recipe(user=user1, name="Test Recipe 1", prep_time_minutes=10, cook_time_minutes=25)
    recipe1.steps.extend([
        RecipeStep(number=1, content="Take out the ingredients"),
        RecipeStep(number=2, content="Cook the ingredients"),
        RecipeStep(number=3, content="Eat the meal")])
    recipe1.ingredient_assoc.extend([
        RecipeIngredient(ingredient=Ingredient(name="Canned tomatoes"), amount=1, units="can"),
        RecipeIngredient(ingredient=Ingredient(name="Cumin powder"), amount=2, units="Tbsp")])
    recipe1.comments.extend([
        Comment(user=user2, content="This is gross"),
        Comment(user=user1, content="That's just, like, your opinion, man"),
        Comment(user=user3, content="Simmer dean")])

    """
    Recipe 2
    """
    recipe2 = Recipe(user=user2, name="Test Recipe 2", prep_time_minutes=25, cook_time_minutes=50)
    recipe2.steps.extend([
        RecipeStep(number=1, content="Thaw meat"),
        RecipeStep(number=2, content="Season meat"),
        RecipeStep(number=3, content="Cook meat"),
        RecipeStep(number=4, content="Let sit for 5 minutes, then serve")])
    recipe2.ingredient_assoc.extend([
        RecipeIngredient(ingredient=Ingredient(name="Ribeye"), amount=14, units="oz"),
        RecipeIngredient(ingredient=Ingredient(name="Salt"), amount=1, units="Tsp"),
        RecipeIngredient(ingredient=Ingredient(name="Pepper"), amount=1.5, units="Tsp")
    ])
    recipe2.comments.extend([
        Comment(user=user2, content="Now this is a meal"),
        Comment(user=user3, content="He might have you beat @user1"),
        Comment(user=user1, content="Okay, this IS better")
    ])

    with app.app_context():
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
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
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert len(json_data) == 1
    assert json_data["users"] == []

def test_get_users_when_nonempty(populated_db_client):
    rv = populated_db_client.get('/users/')
    assert rv.status_code == 200
    json_data = rv.get_json()
    print("JSON data for test_get_users_when_nonempty: '{}'".format(json_data))
    assert len(json_data) == 1
    assert len(json_data["users"]) == 3

    user1 = json_data["users"][0]
    assert user1["name"] == "Test User 1"
    assert user1["email"] == "testuser1@gmail.com"
    assert "password" not in user1.keys()
    assert user1["recipes"] == [1]
    assert user1["comments"] == [2, 6]

    user2 = json_data["users"][1]
    assert user2["name"] == "Test User 2"
    assert user2["email"] == "TU2@gmail.com"
    assert "password" not in user2.keys()
    assert user2["recipes"] == [2]
    assert user2["comments"] == [1, 4]

    user3 = json_data["users"][2]
    assert user3["name"] == "Test User 3"
    assert user3["email"] == "TestUser3@gmail.com"
    assert "password" not in user3.keys()
    assert user3["recipes"] == []
    assert user3["comments"] == [3, 5]


"""
GET /recipes/
"""
def test_recipes_when_empty(empty_db_client):
    rv = empty_db_client.get('/recipes/')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert len(json_data) == 1
    assert json_data["recipes"] == []

def test_recipes_when_nonempty(populated_db_client):
    rv = populated_db_client.get('/recipes/')
    assert rv.status_code == 200
    json_data = rv.get_json()
    print("JSON data for test_recipes_when_nonempty: '{}'".format(json_data))
    assert len(json_data) == 1
    recipes = json_data["recipes"]
    assert len(recipes) == 2

    """
    Recipe 1
    """
    recipe1 = recipes[0]
    assert recipe1["name"] == "Test Recipe 1"
    assert recipe1["prep_time_minutes"] == 10
    assert recipe1["cook_time_minutes"] == 25

    assert len(recipe1["steps"]) == 3
    assert recipe1["steps"][0]["number"] == 1
    assert recipe1["steps"][0]["content"] == "Take out the ingredients"
    assert recipe1["steps"][1]["number"] == 2
    assert recipe1["steps"][1]["content"] == "Cook the ingredients"
    assert recipe1["steps"][2]["number"] == 3
    assert recipe1["steps"][2]["content"] == "Eat the meal"

    assert len(recipe1["ingredients"]) == 2
    assert recipe1["ingredients"][0]["ingredient"] == "Canned tomatoes"
    assert recipe1["ingredients"][0]["amount"] == 1
    assert recipe1["ingredients"][0]["units"] == "can"
    assert recipe1["ingredients"][1]["ingredient"] == "Cumin powder"
    assert recipe1["ingredients"][1]["amount"] == 2
    assert recipe1["ingredients"][1]["units"] == "Tbsp"

    assert len(recipe1["comments"]) == 3
    assert recipe1["comments"][0]["user"] == "Test User 2"
    assert recipe1["comments"][0]["content"] == "This is gross"
    assert recipe1["comments"][1]["user"] == "Test User 1"
    assert recipe1["comments"][1]["content"] == "That's just, like, your opinion, man"
    assert recipe1["comments"][2]["user"] == "Test User 3"
    assert recipe1["comments"][2]["content"] == "Simmer dean"

    """
    Recipe 2
    """
    recipe2 = recipes[1]
    assert recipe2["name"] == "Test Recipe 2"
    assert recipe2["prep_time_minutes"] == 25
    assert recipe2["cook_time_minutes"] == 50

    assert len(recipe2["steps"]) == 4
    assert recipe2["steps"][0]["number"] == 1
    assert recipe2["steps"][0]["content"] == "Thaw meat"
    assert recipe2["steps"][1]["number"] == 2
    assert recipe2["steps"][1]["content"] == "Season meat"
    assert recipe2["steps"][2]["number"] == 3
    assert recipe2["steps"][2]["content"] == "Cook meat"
    assert recipe2["steps"][3]["number"] == 4
    assert recipe2["steps"][3]["content"] == "Let sit for 5 minutes, then serve"

    assert len(recipe2["ingredients"]) == 3
    assert recipe2["ingredients"][0]["ingredient"] == "Ribeye"
    assert recipe2["ingredients"][0]["amount"] == 14
    assert recipe2["ingredients"][0]["units"] == "oz"
    assert recipe2["ingredients"][1]["ingredient"] == "Salt"
    assert recipe2["ingredients"][1]["amount"] == 1
    assert recipe2["ingredients"][1]["units"] == "Tsp"
    assert recipe2["ingredients"][2]["ingredient"] == "Pepper"
    assert recipe2["ingredients"][2]["amount"] == 1.5
    assert recipe2["ingredients"][2]["units"] == "Tsp"

    assert len(recipe2["comments"]) == 3
    assert recipe2["comments"][0]["user"] == "Test User 2"
    assert recipe2["comments"][0]["content"] == "Now this is a meal"
    assert recipe2["comments"][1]["user"] == "Test User 3"
    assert recipe2["comments"][1]["content"] == "He might have you beat @user1"
    assert recipe2["comments"][2]["user"] == "Test User 1"
    assert recipe2["comments"][2]["content"] == "Okay, this IS better"



"""
Comments
"""

def test_get_comments_for_existing_user(populated_db_client):
    rv = populated_db_client.get('/users/3/comments/')
    assert rv.status_code == 200
    json_data = rv.get_json()
    print("test_get_comments_for_existing_user: {}".format(json_data))
    assert len(json_data) == 3
    assert json_data["user_id"] == "3"
    assert json_data["total_comments"] == len(json_data["comments"]) == 2

    comment1 = json_data["comments"][0]
    assert comment1["id"] == 3
    assert comment1["recipe_id"] == 1
    assert comment1["content"] == "Simmer dean"

    comment2 = json_data["comments"][1]
    assert comment2["id"] == 5
    assert comment2["recipe_id"] == 2
    assert comment2["content"] == "He might have you beat @user1"

def test_get_comments_for_nonexistent_user(empty_db_client):
    rv = empty_db_client.get('/users/1/comments/')
    assert rv.status_code == 404
    assert rv.get_data() == b"User 1 not found"

