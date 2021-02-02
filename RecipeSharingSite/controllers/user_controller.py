from RecipeSharingSite.models.user import User
from werkzeug.security import generate_password_hash
from datetime import date
from RecipeSharingSite import db


class UserController:
    @staticmethod
    def get_all_users():
        return {"users": [u.to_dict() for u in User.query.all()]}

    """
    Returns a dictionary of user data if the user exists
    Returns none if the user does not exist 
    """
    @staticmethod
    def get_user_info_for(user_id):
        user = User.query.get(user_id)
        if user is None:
            return None
        return user.to_dict()


    """
    Returns None is the user couldn't be added (an exception occurred)
    Returns a dictionary of the new User data if add succeeded
    """
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
            db.session.rollback()
            db.session.flush()
            return None


    """
    Assumes user exists
    Returns True if user deleted
    Returns False is user couldn't be deleted (Exception occurred)
    """
    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        db.session.delete(user)
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            return False


    """
    Assumes user exists
    Returns dictionary containing comment data for user
    """
    @staticmethod
    def get_comments_made_by_user(user_id):
        user = User.query.get(user_id)
        return {"comments": [c.to_dict() for c in user.comments]}



    @staticmethod
    def user_exists(user_id):
        return True if User.query.get(user_id) is not None else False


