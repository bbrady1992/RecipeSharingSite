from flask import Flask
from RecipeSharingSite.API.API import API

app = Flask(__name__)
app.register_blueprint(API)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
