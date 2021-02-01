from RecipeSharingSite import db
from sqlalchemy_serializer import SerializerMixin


class Ingredient(db.Model, SerializerMixin):
    __tablename__ = 'Ingredient'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    recipes = db.relationship('Recipe', secondary='RecipeIngredient')

    serialize_only = (
        'id',
        'name',
        'recipes.id'
    )

    def __repr__(self):
        return '<Ingredient %r>' % self.name
