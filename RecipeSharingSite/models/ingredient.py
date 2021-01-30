from RecipeSharingSite import db


class Ingredient(db.Model):
    __tablename__ = 'Ingredient'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    recipes = db.relationship("RecipeIngredient", back_populates="ingredient")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Ingredient %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }