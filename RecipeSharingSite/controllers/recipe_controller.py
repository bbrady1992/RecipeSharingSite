from RecipeSharingSite.models.recipe import Recipe


class RecipeController:
    @staticmethod
    def get_all_recipes():
        return Recipe.query.all()