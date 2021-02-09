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


    @staticmethod
    def comment_exists(comment_id):
        return Comment.query.get(comment_id) is not None


    @staticmethod
    def update_comment_information(comment_id, new_content=None):
        comment = Comment.query.get(comment_id)
        comment_updated = False
        if new_content is not None and new_content != comment.content:
            comment.content = new_content
            comment_updated = True
        if comment_updated:
            db.session.commit()
        return comment_updated, comment.to_dict()



