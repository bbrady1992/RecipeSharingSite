import os
import tempfile
from datetime import date, datetime
import pytz

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

    user1 = User(
        name="TestUser1",
        email="testuser1@gmail.com",
        password="tu3passwordhash",
        joined_on=date(2000, 6, 23))
    user2 = User(
        name="TestUser2",
        email="TU2@gmail.com",
        password="tu2passwordhash",
        joined_on=date(1992, 10, 5))
    user3 = User(
        name="TestUser3",
        email="TestUser3@gmail.com",
        password="tu3passwordhash",
        joined_on=date(2021, 1, 20))

    """
    Recipe 1
    """
    recipe1 = Recipe(
        user=user1,
        name="Test Recipe 1",
        prep_time_minutes=10,
        cook_time_minutes=25,
        submitted_on=date(2021, 1, 20))
    recipe1.steps.extend([
        RecipeStep(number=1, content="Take out the ingredients"),
        RecipeStep(number=2, content="Cook the ingredients"),
        RecipeStep(number=3, content="Eat the meal")])
    recipe1.ingredient_assoc.extend([
        RecipeIngredient(ingredient=Ingredient(name="Canned tomatoes"), amount=1, units="can"),
        RecipeIngredient(ingredient=Ingredient(name="Cumin powder"), amount=2, units="Tbsp")])
    recipe1.comments.extend([
        Comment(
            user=user2,
            content="This is gross",
            submitted_on=datetime(2021, 1, 20, 12, 0, 0, 0, pytz.UTC)),
        Comment(
            user=user1,
            content="That's just, like, your opinion, man",
            submitted_on=datetime(2021, 1, 21, 16, 15, 0, 0, pytz.UTC)),
        Comment(
            user=user3,
            content="Simmer dean",
            submitted_on=datetime(2021, 1, 22, 5, 30, 0, 0, pytz.UTC))])

    """
    Recipe 2
    """
    recipe2 = Recipe(
        user=user2,
        name="Test Recipe 2",
        prep_time_minutes=25,
        cook_time_minutes=50,
        submitted_on=date(2021, 1, 21))
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
        Comment(
            user=user2,
            content="Now this is a meal",
            submitted_on=datetime(2021, 1, 24, 4, 30, 0, 0, pytz.UTC)),
        Comment(
            user=user3,
            content="He might have you beat @user1",
            submitted_on=datetime(2021, 1, 24, 8, 45, 0, 0, pytz.UTC)),
        Comment(
            user=user1,
            content="Okay, this IS better",
            submitted_on=datetime(2021, 1, 24, 19, 10, 0, 0, pytz.UTC))
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
    assert user1["name"] == "TestUser1"
    assert user1["email"] == "testuser1@gmail.com"
    assert "password" not in user1.keys()
    assert user1["recipes"] == [1]
    assert user1["comments"] == [2, 6]
    assert user1["joined_on"] == "2000-06-23"

    user2 = json_data["users"][1]
    assert user2["name"] == "TestUser2"
    assert user2["email"] == "TU2@gmail.com"
    assert "password" not in user2.keys()
    assert user2["recipes"] == [2]
    assert user2["comments"] == [1, 4]
    assert user2["joined_on"] == "1992-10-05"

    user3 = json_data["users"][2]
    assert user3["name"] == "TestUser3"
    assert user3["email"] == "TestUser3@gmail.com"
    assert "password" not in user3.keys()
    assert user3["recipes"] == []
    assert user3["comments"] == [3, 5]
    assert user3["joined_on"] == "2021-01-20"

def test_get_nonexistent_user(empty_db_client):
    rv = empty_db_client.get('/users/nonexistentuser/')
    assert rv.status_code == 404
    assert rv.get_data() == b"User nonexistentuser not found"

def test_get_existing_user(populated_db_client):
    rv = populated_db_client.get('/users/TestUser1/')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert len(json_data) == 6
    assert json_data["user_id"] == 1
    assert json_data["name"] == "TestUser1"
    assert json_data["email"] == "testuser1@gmail.com"
    assert json_data["joined_on"] == "2000-06-23"
    assert json_data["recipes"] == [1]
    assert json_data["comments"] == [2, 6]


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
    assert recipe1["submitted_on"] == "2021-01-20"

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
    assert recipe1["comments"][0]["user"] == "TestUser2"
    assert recipe1["comments"][0]["content"] == "This is gross"
    assert recipe1["comments"][0]["submitted_on"] == "2021-01-20T12:00:00"
    assert recipe1["comments"][1]["user"] == "TestUser1"
    assert recipe1["comments"][1]["content"] == "That's just, like, your opinion, man"
    assert recipe1["comments"][1]["submitted_on"] == "2021-01-21T16:15:00"
    assert recipe1["comments"][2]["user"] == "TestUser3"
    assert recipe1["comments"][2]["content"] == "Simmer dean"
    assert recipe1["comments"][2]["submitted_on"] == "2021-01-22T05:30:00"

    """
    Recipe 2
    """
    recipe2 = recipes[1]
    assert recipe2["name"] == "Test Recipe 2"
    assert recipe2["prep_time_minutes"] == 25
    assert recipe2["cook_time_minutes"] == 50
    assert recipe2["submitted_on"] == "2021-01-21"

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
    assert recipe2["comments"][0]["user"] == "TestUser2"
    assert recipe2["comments"][0]["content"] == "Now this is a meal"
    assert recipe2["comments"][0]["submitted_on"] == "2021-01-24T04:30:00"
    assert recipe2["comments"][1]["user"] == "TestUser3"
    assert recipe2["comments"][1]["content"] == "He might have you beat @user1"
    assert recipe2["comments"][1]["submitted_on"] == "2021-01-24T08:45:00"
    assert recipe2["comments"][2]["user"] == "TestUser1"
    assert recipe2["comments"][2]["content"] == "Okay, this IS better"
    assert recipe2["comments"][2]["submitted_on"] == "2021-01-24T19:10:00"

def test_get_recipes_for_nonexistent_user(empty_db_client):
    rv = empty_db_client.get('/users/TestUser1/recipes/')
    assert rv.status_code == 404
    assert rv.get_data() == b"User TestUser1 not found"

def test_get_recipes_for_existing_user(populated_db_client):
    rv = populated_db_client.get('/users/TestUser1/recipes/')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert len(json_data) == 3
    assert json_data["user_id"] == 1
    assert json_data["total_recipes"] == len(json_data["recipes"]) == 1
    recipe1 = json_data["recipes"][0]
    assert recipe1["id"] == 1
    assert recipe1["name"] == "Test Recipe 1"
    assert recipe1["submitted_on"] == "2021-01-20"


"""
Comments
"""

def test_get_comments_for_existing_user(populated_db_client):
    rv = populated_db_client.get('/users/TestUser3/comments/')
    assert rv.status_code == 200
    json_data = rv.get_json()
    print("test_get_comments_for_existing_user: {}".format(json_data))
    assert len(json_data) == 3
    assert json_data["user_id"] == 3
    assert json_data["total_comments"] == len(json_data["comments"]) == 2

    comment1 = json_data["comments"][0]
    assert comment1["id"] == 3
    assert comment1["recipe_id"] == 1
    assert comment1["content"] == "Simmer dean"
    assert comment1["submitted_on"] == "2021-01-22T05:30:00"

    comment2 = json_data["comments"][1]
    assert comment2["id"] == 5
    assert comment2["recipe_id"] == 2
    assert comment2["content"] == "He might have you beat @user1"
    assert comment2["submitted_on"] == "2021-01-24T08:45:00"

def test_get_comments_for_nonexistent_user(empty_db_client):
    rv = empty_db_client.get('/users/TestUser1/comments/')
    assert rv.status_code == 404
    assert rv.get_data() == b"User TestUser1 not found"


