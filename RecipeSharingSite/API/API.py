from flask import Blueprint, request, jsonify
from flask_api import status
from RecipeSharingSite.controllers.user_controller import UserController
from RecipeSharingSite.controllers.recipe_controller import RecipeController
from RecipeSharingSite.controllers.comment_controller import CommentController

API = Blueprint('API', __name__)


# TODO (bbrady) - remove this stub when API is implemented
def endpoint_stub(route, method, *args):
    return "{} {} ({})".format(method, route, args)


"""
User API 
"""
@API.route('/users/')
def get_all_users():
    users = UserController.get_all_users()
    return jsonify(users)


@API.route('/users/', methods=['POST'])
def add_user():
    return endpoint_stub('/users/', request.method)


@API.route('/users/<user_name>/')
def get_user_information(user_name):
    user_info = UserController.get_user_info_for(user_name)
    if user_info is None:
        return "User {} not found".format(user_name), status.HTTP_404_NOT_FOUND
    return jsonify(user_info), status.HTTP_200_OK


@API.route('/users/<user_name>/', methods=['PUT'])
def update_user_information(user_name):
    return endpoint_stub('/users/<user_name>', request.method, user_name)


@API.route('/users/<user_name>/', methods=['DELETE'])
def delete_user(user_name):
    return endpoint_stub('/users/<user_name>', request.method, user_name)

@API.route('/users/<user_name>/comments/')
def get_comments_for_user(user_name):
    results = CommentController.get_comments_for_user(user_name)
    if results is None:
        return "User {} not found".format(user_name), status.HTTP_404_NOT_FOUND
    return jsonify(results), status.HTTP_200_OK

@API.route('/users/<user_name>/recipes/')
def get_recipes_for_user(user_name):
    results = RecipeController.get_recipes_for_user(user_name)
    if results is None:
        return "User {} not found".format(user_name), status.HTTP_404_NOT_FOUND
    return jsonify(results), status.HTTP_200_OK


"""
Recipes API
"""
@API.route('/recipes/')
def get_all_recipes():
    recipes = RecipeController.get_all_recipes()
    return jsonify(recipes), status.HTTP_200_OK

@API.route('/recipes/<recipe_id>/')
def get_recipe(recipe_id):
    recipe = RecipeController.get_recipe(recipe_id)
    if recipe is None:
        return "Recipe {} not found".format(recipe_id), status.HTTP_404_NOT_FOUND
    return jsonify(recipe), status.HTTP_200_OK


@API.route('/recipes/<recipe_id>/', methods=['PUT'])
def update_recipe(recipe_id):
    return endpoint_stub('/recipes/', request, recipe_id)


@API.route('/recipes/<recipe_id>/', methods=['DELETE'])
def delete_recipe(recipe_id):
    return endpoint_stub('/recipes/', request, recipe_id)


"""
Ingredients API
"""
@API.route('/ingredients/')
def get_all_ingredients():
    return endpoint_stub('/ingredients/', request.method)


@API.route('/ingredients/<ingredient_id>')
def get_recipes_that_use_ingredient(ingredient_id):
    return endpoint_stub('/ingredients/<ingredient_id>', request.method, ingredient_id)


"""
Comments API
"""
@API.route('/comments/')
def get_all_comments():
    return endpoint_stub('/comments/', request.method)


@API.route('/comments/', methods=['POST'])
def add_comment():
    return endpoint_stub('/comments/', request.method)


@API.route('/comments/<comment_id>')
def get_comment(comment_id):
    return endpoint_stub('/comments/<comment_id>', request.method, comment_id)


@API.route('/comments/<comment_id>', methods=['PUT'])
def update_comment(comment_id):
    return endpoint_stub('/comments/<comment_id>', request.method, comment_id)


@API.route('/comments/<comment_id>/', methods=['DELETE'])
def delete_comment(comment_id):
    comment_deleted = CommentController.delete_comment_with_id(comment_id)
    if comment_deleted is None:
        return "Comment {} not found".format(comment_id), status.HTTP_404_NOT_FOUND
    return "", status.HTTP_204_NO_CONTENT
