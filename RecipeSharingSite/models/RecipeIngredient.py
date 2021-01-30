from RecipeSharingSite import db

class RecipeIngredient(db.Model):
    __tablename__ = 'RecipeIngredient'

    recipe_id = db.Column(db.Integer, db.ForeignKey('Recipe.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('Ingredient.id'), primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    units = db.Column(db.String)

    recipe = db.relationship("Recipe", back_populates="ingredients")
    ingredient = db.relationship("Ingredient", back_populates="recipes")

    def __init__(self, ingredient_id, amount, units):
        self.ingredient_id = ingredient_id
        self.amount = amount
        self.units = units


    def __repr__(self):
        return '<RecipeIngredient %r-%r>' % self.recipe_id, self.ingredient_id
