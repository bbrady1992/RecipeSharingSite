from RecipeSharingSite.models.user import User


class UserController:
    @staticmethod
    def get_all_users():
        return User.query.all()
