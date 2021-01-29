from RecipeSharingSite import db

RecipeIngredient = db.Table(
    'RecipeIngredient',
    db.Column('recipe_id', db.Integer, db.ForeignKey('Recipe.id'), primary_key=True),
    db.Column('ingredient_id', db.ForeignKey('Ingredient.id'), primary_key=True),
    db.Column('amount', db.Float, nullable=False),
    db.Column('units', db.String)
)