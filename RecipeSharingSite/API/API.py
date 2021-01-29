from flask import Blueprint, request, jsonify
from flask_api import status

API = Blueprint('API', __name__)


# TODO (bbrady) - remove this stub when API is implemented
def endpoint_stub(route, method, *args):
    return "{} {} ({})".format(method, route, args)


"""
User API 
"""
@API.route('/users/')
def get_all_users():
    return endpoint_stub('/users/', request.method)


@API.route('/users/', methods=['POST'])
def add_user():
    return endpoint_stub('/users/', request.method)


@API.route('/users/<user_name>/')
def get_user_information(user_name):
    return endpoint_stub('/users/<user_name>', request.method, user_name)


@API.route('/users/<user_name>/', methods=['PUT'])
def update_user_information(user_name):
    return endpoint_stub('/users/<user_name>', request.method, user_name)


@API.route('/users/<user_name>/', methods=['DELETE'])
def delete_user(user_name):
    return endpoint_stub('/users/<user_name>', request.method, user_name)


"""
Recipes API
"""
@API.route('/recipes/')
def get_all_recipes():
    return endpoint_stub('/recipes/', request.method)

@API.route('/recipes/<recipe_id>/')
def get_recipe(recipe_id):
    return endpoint_stub('/recipes/', request, recipe_id)


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


@API.route('/comments/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    return endpoint_stub('/comments/<comment_id>', request.method, comment_id)
