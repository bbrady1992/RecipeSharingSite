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


@comment_API.route('/comments/<comment_id>', methods=['PUT'])
def update_comment(comment_id):
    def comment_update_request_valid(request_data):
        if request_data is None:
            return False
        return 'content' in request_data.keys()

    json_data = request.get_json()
    if not comment_update_request_valid(json_data):
        return '', status.HTTP_400_BAD_REQUEST

    if not CommentController.comment_exists(comment_id):
        return f'Comment with ID {comment_id} not found', status.HTTP_404_NOT_FOUND

    comment_updated, updated_comment = CommentController.update_comment_information(comment_id, json_data.get('content'))
    if updated_comment is None:
        return 'Unable to update comment information in database at this time', status.HTTP_503_SERVICE_UNAVAILABLE
    elif not comment_updated:
        return '', status.HTTP_204_NO_CONTENT
    return jsonify(updated_comment), status.HTTP_200_OK


@comment_API.route('/comments/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    if not CommentController.comment_exists(comment_id):
        return f'Comment with ID {comment_id} not found', status.HTTP_404_NOT_FOUND

    if CommentController.delete_comment(comment_id):
        return '', status.HTTP_204_NO_CONTENT
    else:
        return 'Unable to delete comment from database at this time', status.HTTP_503_SERVICE_UNAVAILABLE
