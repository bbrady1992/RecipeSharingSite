from RecipeSharingSite.models.comment import Comment
from RecipeSharingSite.models.user import User


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

        results = Comment.query.filter_by(user_id=user.id).all()

        def unpack_comment(c):
            return {
                "id": c.id,
                "recipe_id": c.recipe_id,
                "content": c.content,
                "submitted_on": c.submitted_on.isoformat()
            }
        comments = list(map(unpack_comment, results))

        return {
            "user_id": user.id,
            "total_comments": len(comments),
            "comments": comments
        }
