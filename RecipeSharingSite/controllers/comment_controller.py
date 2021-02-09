from RecipeSharingSite.models.comment import Comment
from RecipeSharingSite.models.user import User
from RecipeSharingSite import db


class CommentController:
    @staticmethod
    def get_comment(comment_id):
        comment = Comment.query.get(comment_id)
        if comment is None:
            return None
        return comment.to_dict()

    @staticmethod
    def delete_comment_with_id(comment_id):
        comment = Comment.query.get(comment_id)
        if comment is None:
            return None
        db.session.delete(comment)
        db.session.commit()
        return True


