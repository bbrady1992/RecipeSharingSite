from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app(database_uri = None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key-goes-here'  # TODO (bbrady) - figure out what this is
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' if database_uri is None else database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    """
    All data models need to be imported before the db.create_all() call. Add them here
    """
    from RecipeSharingSite.models.comment import Comment
    from RecipeSharingSite.models.ingredient import Ingredient
    from RecipeSharingSite.models.recipe import Recipe
    from RecipeSharingSite.models.recipestep import RecipeStep
    from RecipeSharingSite.models.user import User
    from RecipeSharingSite.models.RecipeIngredient import RecipeIngredient

    with app.app_context():
        db.create_all()

    from RecipeSharingSite.API.recipe_api import recipe_API
    from RecipeSharingSite.API.comment_api import comment_API
    from RecipeSharingSite.API.user_api import user_API
    app.register_blueprint(recipe_API)
    app.register_blueprint(comment_API)
    app.register_blueprint(user_API)

    return app
