from RecipeSharingSite import db

class RecipeIngredient(db.Model):
    __tablename__ = 'RecipeIngredient'

    recipe_id = db.Column(db.Integer, db.ForeignKey('Recipe.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('Ingredient.id'), primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    units = db.Column(db.String)

    recipe = db.relationship('Recipe', backref=db.backref('ingredient_assoc'))
    ingredient = db.relationship('Ingredient', backref=db.backref('recipe_assoc'))


    def __repr__(self):
        return '<RecipeIngredient %r-%r>' % self.recipe_id, self.ingredient_id

    def serialize(self):
        return {
            "ingredient": self.ingredient.name,
            "amount": self.amount,
            "units": self.units
        }
