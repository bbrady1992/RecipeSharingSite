from RecipeSharingSite.models.user import User


class UserController:
    @staticmethod
    def get_all_users():
        return {"users": [u.serialize() for u in User.query.all()]}
