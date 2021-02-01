from RecipeSharingSite.models.comment import Comment
from RecipeSharingSite.models.user import User
from RecipeSharingSite import db


class CommentController:
    """
    Returns 
    None: requested user does not exist
    Map with comment data: requested user exists
    """
    @staticmethod
    def get_comments_for_user(requested_user):
        user = User.query.filter_by(name=requested_user).first()
        if user is None:
            return None

        return {"comments": [c.to_dict() for c in user.comments]}

    @staticmethod
    def delete_comment_with_id(comment_id):
        comment = Comment.query.get(comment_id)
        if comment is None:
            return None
        db.session.delete(comment)
        db.session.commit()
        return True


