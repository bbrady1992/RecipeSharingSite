from RecipeSharingSite import db

class Recipe(db.Model):
    __tablename__ = 'Recipe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    prep_time_minutes = db.Column(db.Integer)
    cook_time_minutes = db.Column(db.Integer)
    submitted_on = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    user = db.relationship('User')
    steps = db.relationship("RecipeStep", backref="Recipe", lazy="dynamic", cascade="all,delete")
    comments = db.relationship("Comment", backref="Recipe", lazy="dynamic", cascade="all,delete")
    ingredients = db.relationship('Ingredient', secondary='RecipeIngredient')

    def __repr__(self):
        return '<Recipe %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "prep_time_minutes": self.prep_time_minutes,
            "cook_time_minutes": self.cook_time_minutes,
            "user_id": self.user_id,
            "ingredients": [ri.serialize() for ri in self.ingredient_assoc],
            "steps": [s.serialize() for s in self.steps],
            "comments": [{"id": c.id, "user": c.user.name, "content": c.content} for c in self.comments],
            "submitted_on": self.submitted_on.isoformat()
        }


