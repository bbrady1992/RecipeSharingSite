from RecipeSharingSite.models.user import User
from werkzeug.security import generate_password_hash
from datetime import date
from RecipeSharingSite import db


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


    @staticmethod
    def add_user(name, email, password):
        new_user = User(
            name=name,
            email=email,
            password=generate_password_hash(password, method='sha256'),
            joined_on=date.today()
        )
        db.session.add(new_user)
        try:
            db.session.commit()
            return User.query.filter_by(name=name).first().to_dict()
        except Exception as e:
            print("Exception while adding user: '{}'".format(str(e)))

            db.session.rollback()
            db.session.flush()
            return None


