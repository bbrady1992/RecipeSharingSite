from RecipeSharingSite.models.user import User


class UserController:
    @staticmethod
    def get_all_users():
        return {"users": [u.serialize() for u in User.query.all()]}

    @staticmethod
    def get_user_info_for(user_name):
        user = User.query.filter_by(name=user_name).first()
        if user is None:
            return None
        return {
            "user_id": user.id,
            "name": user.name,
            "email": user.email,
            "joined_on": user.joined_on.isoformat(),
            "recipes": [r.id for r in user.recipes],
            "comments": [c.id for c in user.comments]
        }
