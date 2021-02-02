import os
import tempfile
import pytest
import pytz
from datetime import date, datetime

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
    recipe1.ingredients.extend([
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
    recipe2.ingredients.extend([
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



