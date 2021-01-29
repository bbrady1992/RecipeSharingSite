from RecipeSharingSite import db

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(35), unique=True, nullable=False)
    name = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    recipes = db.relationship("Recipe", backref="User", lazy="dynamic")
    comments = db.relationship("Comment", backref="User", lazy="dynamic")

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "recipes": [r.id for r in self.recipes],
            "comments": [c.id for c in self.comments]
        }
