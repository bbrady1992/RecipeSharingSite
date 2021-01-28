from RecipeSharingSite import db

class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True)
    prep_time_minutes = db.Column(db.Integer)
    cook_time_minutes = db.Column(db.Integer)
    # TODO (bbrady) - add ingredient list
    # TODO (bbrady) - add recipe steps

    def __init__(self, name, prep_time_minutes, cook_time_minutes):
        self.name = name
        self.prep_time_minutes = prep_time_minutes
        self.cook_time_minutes = cook_time_minutes

    def __repr__(self):
        return '<Recipe {}>'.format(self.name);
