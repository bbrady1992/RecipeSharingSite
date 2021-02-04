from RecipeSharingSite import db
from sqlalchemy_serializer import SerializerMixin

class Recipe(db.Model, SerializerMixin):
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
    ingredients_raw = db.relationship('Ingredient', secondary='RecipeIngredient')
    ingredients = db.relationship('RecipeIngredient', backref=db.backref('recipe'), cascade='all,delete',passive_deletes=True)

    serialize_only = (
        'id',
        'name',
        'prep_time_minutes',
        'cook_time_minutes',
        'submitted_on',
        'user_id',
        'steps.number',
        'steps.content',
        'comments.id',
        'ingredients')



    def __repr__(self):
        return '<Recipe %r>' % self.name


