from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'  # TODO (bbrady) - figure out what this is
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)

"""
All data models need to be imported before the db.create_all() call. Add them here
"""
from RecipeSharingSite.models.comment import Comment
from RecipeSharingSite.models.ingredient import Ingredient
from RecipeSharingSite.models.recipe import Recipe
from RecipeSharingSite.models.recipestep import RecipeStep
from RecipeSharingSite.models.user import User
from RecipeSharingSite.models.m2m_RecipeIngredient import RecipeIngredient
db.create_all()

from RecipeSharingSite.API.API import API as API_BP
app.register_blueprint(API_BP)
