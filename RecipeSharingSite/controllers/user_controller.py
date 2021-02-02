from RecipeSharingSite.models.user import User


class UserController:
    @staticmethod
    def get_all_users():
        return {"users": [u.to_dict() for u in User.query.all()]}

    @staticmethod
    def get_user_info_for(user_id):
        user = User.query.get(user_id)
        if user is None:
            return None
        return user.to_dict()
