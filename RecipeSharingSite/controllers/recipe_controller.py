from RecipeSharingSite.models.recipe import Recipe
from RecipeSharingSite.models.user import User
from RecipeSharingSite import db


class RecipeController:
    @staticmethod
    def get_all_recipes():
        return {"recipe_ids": [{'id': r.id} for r in Recipe.query.all()]}

    @staticmethod
    def get_recipes_for_user(requested_user):
        user = User.query.filter_by(name=requested_user).first()
        if user is None:
            return None

        return {"recipes": [r.to_dict() for r in user.recipes]}

    @staticmethod
    def get_recipe(recipe_id):
        recipe = Recipe.query.get(recipe_id)
        if recipe is None:
            return None

        return recipe.to_dict()


    @staticmethod
    def delete_recipe(recipe_id):
        recipe = Recipe.query.get(recipe_id)
        db.session.delete(recipe)
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("Exception string = '{}'".format(str(e)))
            db.session.rollback()
            db.session.flush()
            return False

    @staticmethod
    def recipe_exists(recipe_id):
        return True if Recipe.query.get(recipe_id) is not None else False
