from flask import Blueprint, request, jsonify
from flask_api import status

from RecipeSharingSite.models.user import User
from RecipeSharingSite.models.recipe import Recipe
from RecipeSharingSite.models.recipe import RecipeStep
from RecipeSharingSite import db

API = Blueprint('API', __name__)

@API.route('/recipes/')
def recipes():
    return '/recipes/ API Endpoint'

@API.route('/recipes/add', methods=['POST'])
def recipes_add():
    # TODO (bbrady) - remove this stubbed data and add actual logic
    new_recipe = Recipe("Beef stew", "10", "60")
    step_1 = RecipeStep(1, "Open the can of beef stew with a can opener", new_recipe)
    step_2 = RecipeStep(2, "Pour out the contents of the can and gorge like a pyig", new_recipe)
    new_recipe.steps.append(step_1)
    new_recipe.steps.append(step_2)
    db.session.add(new_recipe)
    db.session.commit()
    return '/recipes/add API Endpoint'

@API.route('/recipes/<recipe_id>', methods=['GET', 'PUT', 'DELETE'])
def recipes_recipe_id(recipe_id):
    if request.method == 'DELETE':
        recipe_to_delete = Recipe.query.filter_by(id=recipe_id).first()
        if recipe_to_delete is not None:
            db.session.delete(recipe_to_delete)
            db.session.commit()
            return "Deleted recipe {}: {}".format(recipe_to_delete.id, recipe_to_delete.name), status.HTTP_200_OK
        else:
            return "Recipe with ID {} not found".format(recipe_id), status.HTTP_404_NOT_FOUND


    else:
        return "Method {} not yet supported".format(request.method), status.HTTP_204_NO_CONTENT

@API.route('/users/')
def users_get():
    # TODO (bbrady) - remove this stubbed data one I've figured out the "correct" way to jsonify SQLAlchemy result sets
    me = User("Ben Brady", "benbrady1992@gmail.com", "passwordPlaceholder")
    db.session.add(me)
    db.session.commit()
    return '/users/ API Endpoint'

@API.route('/users/<user_name>', methods=['GET', 'PUT'])
def users_user_name(user_name):
    return '{} /users/{} API Endpoint'.format(request.method, user_name)

@API.route('/users/<user_name>/recipes')
def users_user_name_recipes(user_name):
    return '/users/{}/recipes API Endpoint'.format(user_name)
