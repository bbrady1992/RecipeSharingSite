from RecipeSharingSite.API.API import API

if __name__ == '__main__':
    #from . import create_app
    #app = create_app()
    from . import app
    app.register_blueprint(API)
    app.run()
