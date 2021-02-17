from flask import Blueprint, request, jsonify
from flask_api import status
from RecipeSharingSite.controllers.recipe_controller import RecipeController

recipe_API = Blueprint('recipe_API', __name__)


@recipe_API.route('/recipes')
def get_all_recipe_ids():
    recipes = RecipeController.get_all_recipes()
    return jsonify(recipes), status.HTTP_200_OK


@recipe_API.route('/recipes/<recipe_id>')
def get_recipe(recipe_id):
    recipe = RecipeController.get_recipe(recipe_id)
    if recipe is None:
        return "Recipe with ID {} not found".format(recipe_id), status.HTTP_404_NOT_FOUND
    return jsonify(recipe), status.HTTP_200_OK


@recipe_API.route('/recipes', methods=['POST'])
def post_recipe():
    return "", status.HTTP_501_NOT_IMPLEMENTED


@recipe_API.route('/recipes/<recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    return "", status.HTTP_501_NOT_IMPLEMENTED


@recipe_API.route('/recipes/<recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    if not RecipeController.recipe_exists(recipe_id):
        return 'Recipe with ID {} not found'.format(recipe_id), status.HTTP_404_NOT_FOUND
    if not RecipeController.delete_recipe(recipe_id):
        return 'Unable to delete recipe from database', status.HTTP_503_SERVICE_UNAVAILABLE
    return '', status.HTTP_204_NO_CONTENT


@recipe_API.route('/recipes/<recipe_id>/comments')
def get_comments_for_recipe(recipe_id):
    if not RecipeController.recipe_exists(recipe_id):
        return 'Recipe with ID {} not found'.format(recipe_id), status.HTTP_404_NOT_FOUND
    return jsonify(RecipeController.get_comments_for_recipe(recipe_id)), status.HTTP_200_OK


@recipe_API.route('/recipes/<recipe_id>/comments', methods=['POST'])
def post_comment_on_recipe(recipe_id):
    def post_comment_request_valid(request_data):
        if request_data is None:
            return False
        keys = request_data.keys()
        return 'user_id' in keys and 'content' in keys

    if not RecipeController.recipe_exists(recipe_id):
        return f'Recipe with ID {recipe_id} not found', status.HTTP_404_NOT_FOUND
    json_data = request.get_json()
    if not post_comment_request_valid(json_data):
        return '', status.HTTP_400_BAD_REQUEST

    new_comment = RecipeController.post_comment_on_recipe(recipe_id, json_data.get('user_id'), json_data.get('content'))
    return jsonify(new_comment), status.HTTP_201_CREATED



