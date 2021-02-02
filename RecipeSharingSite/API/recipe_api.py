from flask import Blueprint, request, jsonify
from flask_api import status
from RecipeSharingSite.controllers.recipe_controller import RecipeController

recipe_API = Blueprint('recipe_API', __name__)


@recipe_API.route('/recipes/')
def get_all_recipe_ids():
    recipes = RecipeController.get_all_recipes()
    return jsonify(recipes), status.HTTP_200_OK


@recipe_API.route('/recipes/<recipe_id>/')
def get_recipe(recipe_id):
    recipe = RecipeController.get_recipe(recipe_id)
    if recipe is None:
        return "Recipe {} not found".format(recipe_id), status.HTTP_404_NOT_FOUND
    return jsonify(recipe), status.HTTP_200_OK


@recipe_API.route('/recipes/', methods=['POST'])
def post_recipe():
    return "", status.HTTP_501_NOT_IMPLEMENTED


@recipe_API.route('/recipes/<recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    return "", status.HTTP_501_NOT_IMPLEMENTED


@recipe_API.route('/recipes/<recipes_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    return "", status.HTTP_501_NOT_IMPLEMENTED


@recipe_API.route('/recipes/<user_id>/')
def get_recipes_submitted_by(user_id):
    return "", status.HTTP_501_NOT_IMPLEMENTED
