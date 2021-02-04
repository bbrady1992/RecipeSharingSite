from RecipeSharingSite.models.recipe import Recipe
from RecipeSharingSite.models.user import User


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
