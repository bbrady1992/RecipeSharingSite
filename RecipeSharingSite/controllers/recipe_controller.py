from RecipeSharingSite.models.recipe import Recipe


class RecipeController:
    @staticmethod
    def get_all_recipes():
        return {"recipes": [r.serialize() for r in Recipe.query.all()]}