from RecipeSharingSite import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(35), unique=True, nullable=False)
    name = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User {}>'.format(self.name);

db.create_all()
