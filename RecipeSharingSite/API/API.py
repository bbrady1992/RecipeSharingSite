from flask import Blueprint, redirect, url_for, request
import json

API = Blueprint('API', __name__)

@API.route('/recipes/')
def recipes():
    return '/recipes/ API Endpoint'

@API.route('/recipes/<recipe_id>', methods=['GET', 'PUT', 'DELETE'])
def recipes_recipe_id(recipe_id):
    return '{} /recipes/{} API Endpoint'.format(request.method, recipe_id)

@API.route('/users/')
def users_get():
    return '/users/ API Endpoint'

@API.route('/users/<user_name>', methods=['GET', 'PUT'])
def users_user_name(user_name):
    return '{} /users/{} API Endpoint'.format(request.method, user_name)

@API.route('/users/<user_name>/recipes')
def users_user_name_recipes(user_name):
    return '/users/{}/recipes API Endpoint'.format(user_name)
