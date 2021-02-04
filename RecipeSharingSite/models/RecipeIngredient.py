from RecipeSharingSite import db
from sqlalchemy_serializer import SerializerMixin

class RecipeIngredient(db.Model, SerializerMixin):
    __tablename__ = 'RecipeIngredient'

    recipe_id = db.Column(db.Integer, db.ForeignKey('Recipe.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('Ingredient.id'), primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    units = db.Column(db.String)

    ingredient = db.relationship('Ingredient', backref=db.backref('recipe_assoc'))

    serialize_only = (
        'ingredient.name',
        'amount',
        'units'
    )

    def __repr__(self):
        return '<RecipeIngredient %r-%r>' % (self.recipe_id, self.ingredient_id)

