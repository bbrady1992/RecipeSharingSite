from RecipeSharingSite import db
from sqlalchemy_serializer import SerializerMixin

class User(db.Model, SerializerMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(35), unique=True, nullable=False)
    name = db.Column(db.String(25), unique=True, nullable=False) # NO SPACES!
    password = db.Column(db.String(64), nullable=False)
    joined_on = db.Column(db.Date, nullable=False)
    recipes = db.relationship("Recipe", backref="User", lazy="dynamic")
    comments = db.relationship("Comment", backref="User", lazy="dynamic")

    serialize_only = (
        'id',
        'email',
        'name',
        'joined_on',
        'recipes.id',
        'comments.id'
    )

    def __repr__(self):
        return '<User %r>' % self.name
