from RecipeSharingSite import db

class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    prep_time_minutes = db.Column(db.Integer)
    cook_time_minutes = db.Column(db.Integer)
    steps = db.relationship("RecipeStep", backref="recipes", lazy="dynamic", cascade="all,delete")
    # TODO (bbrady) - add ingredient list

    def __init__(self, name, prep_time_minutes, cook_time_minutes):
        self.name = name
        self.prep_time_minutes = prep_time_minutes
        self.cook_time_minutes = cook_time_minutes

    def __repr__(self):
        return '<Recipe %r>' % self.name


class RecipeStep(db.Model):
    __tablename__ = 'recipe_steps'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String, nullable=False)

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    recipe = db.relationship('Recipe')

    def __init__(self, number, content, recipe):
        self.number = number
        self.content = content
        self.recipe = recipe

    def __repr__(self):
        return '<Step %r>' % self.number
