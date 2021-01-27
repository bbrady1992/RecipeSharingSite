from flask import Blueprint, redirect, url_for
import json

API = Blueprint('API', __name__)

@API.route('/recipes/')
def recipes_get():
    return '/recipes/ API Endpoint'

@API.route('/users/', methods = ['GET'])
def users_get():
    return '/users/ API Endpoint'

@API.route('/users/<user_name>', methods = ['GET'])
def specific_user_get(user_name):
    return '/users/' + user_name + ' API Endpoint'