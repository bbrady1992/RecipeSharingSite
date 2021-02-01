from RecipeSharingSite import db
from sqlalchemy_serializer import SerializerMixin

class RecipeStep(db.Model, SerializerMixin):
    __tablename__ = 'RecipeStep'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String, nullable=False)

    recipe_id = db.Column(db.Integer, db.ForeignKey('Recipe.id'))
    recipe = db.relationship('Recipe')

    serialize_only = (
        'id',
        'number',
        'content'
    )

    def __repr__(self):
        return '<Step %r>' % self.number

