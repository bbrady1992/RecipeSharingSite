from RecipeSharingSite import db

class RecipeStep(db.Model):
    __tablename__ = 'RecipeStep'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String, nullable=False)

    recipe_id = db.Column(db.Integer, db.ForeignKey('Recipe.id'))
    recipe = db.relationship('Recipe')

    def __init__(self, number, content):
        self.number = number
        self.content = content


    def __repr__(self):
        return '<Step %r>' % self.number

    def serialize(self):
        return {
            "number": self.number,
            "content": self.content
        }

