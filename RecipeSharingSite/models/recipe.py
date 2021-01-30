from RecipeSharingSite import db

class Recipe(db.Model):
    __tablename__ = 'Recipe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    prep_time_minutes = db.Column(db.Integer)
    cook_time_minutes = db.Column(db.Integer)
    # TODO (bbrady) - reevaluate lazy=subquery
    #ingredients = db.relationship('Ingredient', secondary=RecipeIngredient, lazy='subquery', backref=db.backref('Recipe', lazy=True))
    ingredients = db.relationship("RecipeIngredient", back_populates="recipe")
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    user = db.relationship('User')
    steps = db.relationship("RecipeStep", backref="Recipe", lazy="dynamic", cascade="all,delete")
    comments = db.relationship("Comment", backref="Recipe", lazy="dynamic", cascade="all,delete")


    def __repr__(self):
        return '<Recipe %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "prep_time_minutes": self.prep_time_minutes,
            "cook_time_minutes": self.cook_time_minutes,
            "user_id": self.user_id,
            # TODO (bbrady) - fix ingredient serialization after m2m relatinoship
            "ingredients": [i.serialize() for i in self.ingredients],
            "steps": [item.serialize() for item in self.steps]
        }


