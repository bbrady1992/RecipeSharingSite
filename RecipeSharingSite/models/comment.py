from RecipeSharingSite import db
from sqlalchemy_serializer import SerializerMixin


class Comment(db.Model, SerializerMixin):
    __tablename__ = 'Comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    submitted_on = db.Column(db.DateTime, nullable=False)

    # Made on a recipe
    recipe_id = db.Column(db.Integer, db.ForeignKey('Recipe.id'))
    recipe = db.relationship('Recipe')

    # Made by a user
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    user = db.relationship('User')

    serialize_only = (
        'id',
        'content',
        'submitted_on',
        'recipe_id',
        'user_id'
    )
    datetime_format = '%Y-%m-%dT%H:%M:%SZ'

    def __repr__(self):
        return '<Comment %r>' % self.id

