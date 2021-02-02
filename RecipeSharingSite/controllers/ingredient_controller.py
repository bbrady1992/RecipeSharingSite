from RecipeSharingSite.models.ingredient import Ingredient
from RecipeSharingSite import db


class IngredientController:
    """
    Returns 
    None: requested user does not exist
    Map with comment data: requested user exists
    """
    @staticmethod
    def get_recipes_that_use_ingredient(ingredient_id):
        return None

    @staticmethod
    def get_all_ingredients():
        return None


