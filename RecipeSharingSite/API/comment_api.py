from flask import Blueprint, request, jsonify
from flask_api import status
from RecipeSharingSite.controllers.comment_controller import CommentController

comment_API = Blueprint('comment_API', __name__)


@comment_API.route('/comments/<comment_id>')
def get_comment(comment_id):
    comment = CommentController.get_comment(comment_id)
    if comment is None:
        return 'Comment with ID {} not found'.format(comment_id), status.HTTP_404_NOT_FOUND
    return jsonify(comment), status.HTTP_200_OK


@comment_API.route('/comments/<recipe_id>', methods=['POST'])
def post_comment_on_recipe(recipe_id):
    return "", status.HTTP_501_NOT_IMPLEMENTED


@comment_API.route('/comments/<comment_id>', methods=['PUT'])
def update_comment(comment_id):
    return "", status.HTTP_501_NOT_IMPLEMENTED


@comment_API.route('/comments/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    return "", status.HTTP_501_NOT_IMPLEMENTED
