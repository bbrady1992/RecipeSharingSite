from RecipeSharingSite import db


class Comment(db.Model):
    __tablename__ = 'Comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    submitted_on = db.Column(db.DateTime, nullable=False)

    # Made on a recipe
    recipe_id = db.Column(db.Integer, db.ForeignKey('Recipe.id'))
    recipe = db.relationship('Recipe')

    # Made by a user
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    user = db.relationship('User')

    def __repr__(self):
        return '<Comment %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "recipe_id": self.recipe_id,
            "user_id": self.user_id
        }

