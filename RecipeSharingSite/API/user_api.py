from flask import Blueprint, request, jsonify
from flask_api import status
from RecipeSharingSite.controllers.user_controller import UserController

user_API = Blueprint('user_API', __name__)


@user_API.route('/users/')
def get_list_of_users():
    users = UserController.get_all_users()
    return jsonify(users), status.HTTP_200_OK

@user_API.route('/users/', methods=['POST'])
def add_user():
    def user_data_is_valid(request_data):
        keys = request_data.keys()
        return 'name' in keys and 'email' in keys and 'password' in keys

    json_data = request.get_json()
    if not user_data_is_valid(json_data):
        return '', status.HTTP_400_BAD_REQUEST
    added_user = UserController.add_user(json_data['name'], json_data['email'], json_data['password'])
    if added_user is None:
        return 'Unable to add user to database at this time', status.HTTP_503_SERVICE_UNAVAILABLE
    return jsonify(added_user), status.HTTP_201_CREATED


@user_API.route('/users/<user_id>')
def get_user_information(user_id):
    user = UserController.get_user_info_for(user_id)
    if user is None:
        return 'User with ID {} not found'.format(user_id), status.HTTP_404_NOT_FOUND
    return jsonify(user), status.HTTP_200_OK


@user_API.route('/users/<user_id>', methods=['PUT'])
def update_user_information(user_id):
    def user_update_request_valid(request_data):
        if request_data is None:
            return False
        keys = request_data.keys()
        return 'name' in keys or 'email' in keys

    json_data = request.get_json()
    if not user_update_request_valid(json_data):
        return '', status.HTTP_400_BAD_REQUEST

    if not UserController.user_exists(user_id):
        return 'User with ID {} not found'.format(user_id), status.HTTP_404_NOT_FOUND

    update_status, updated_user = UserController.update_user_information(user_id, json_data.get('name'), json_data.get('email'))
    if updated_user is None:
        return 'Unable to update user information in database at this time', status.HTTP_503_SERVICE_UNAVAILABLE
    elif update_status == 'NO_UPDATE':
        return '', status.HTTP_204_NO_CONTENT
    return jsonify(updated_user), status.HTTP_200_OK



@user_API.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if not UserController.user_exists(user_id):
        return 'User with ID {} not found'.format(user_id), status.HTTP_404_NOT_FOUND

    if UserController.delete_user(user_id):
        return '', status.HTTP_204_NO_CONTENT
    else:
        return 'Unable to delete user from database at this time', status.HTTP_503_SERVICE_UNAVAILABLE


@user_API.route('/users/<user_id>/comments')
def get_comments_made_by_user(user_id):
    if not UserController.user_exists(user_id):
        return 'User with ID {} not found'.format(user_id), status.HTTP_404_NOT_FOUND
    return jsonify(UserController.get_comments_made_by_user(user_id)), status.HTTP_200_OK

@user_API.route('/users/<user_id>/recipes')
def get_recipes_submitted_by_user(user_id):
    if not UserController.user_exists(user_id):
        return 'User with ID {} not found'.format(user_id), status.HTTP_404_NOT_FOUND
    return jsonify(UserController.get_recipes_submitted_by_user(user_id)), status.HTTP_200_OK


