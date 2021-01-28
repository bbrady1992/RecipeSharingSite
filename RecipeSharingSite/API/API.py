from flask import Blueprint, request, jsonify
from flask_api import status

API = Blueprint('API', __name__)

@API.route('/recipes/')
def recipes():
    return '/recipes/ API Endpoint'

@API.route('/recipes/add', methods=['POST'])
def recipes_add():
    return '/recipes/add API Endpoint'

@API.route('/recipes/<recipe_id>', methods=['GET', 'PUT', 'DELETE'])
def recipes_recipe_id(recipe_id):
    return "/recipes/{} API Endpoint ({})".format(recipe_id, request.method), status.HTTP_204_NO_CONTENT

@API.route('/users/')
def users_get():
    return '/users/ API Endpoint'

@API.route('/users/<user_name>', methods=['GET', 'PUT'])
def users_user_name(user_name):
    return '{} /users/{} API Endpoint'.format(request.method, user_name)

@API.route('/users/<user_name>/recipes')
def users_user_name_recipes(user_name):
    return '/users/{}/recipes API Endpoint'.format(user_name)
