from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'  # TODO (bbrady) - figure out what this is
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)

from RecipeSharingSite.API.API import API as API_BP
app.register_blueprint(API_BP)
