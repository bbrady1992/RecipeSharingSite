from RecipeSharingSite.models.recipe import Recipe
from RecipeSharingSite.models.user import User


class RecipeController:
    @staticmethod
    def get_all_recipes():
        return {"recipes": [r.serialize() for r in Recipe.query.all()]}

    @staticmethod
    def get_recipes_for_user(requested_user):
        user = User.query.filter_by(name=requested_user).first()
        if user is None:
            return None

        def unpack_recipe(r):
            return {
                "id": r.id,
                "name": r.name,
                "submitted_on": r.submitted_on.isoformat()
            }
        recipes = list(map(unpack_recipe, user.recipes))

        return {
            "user_id": user.id,
            "total_recipes": len(recipes),
            "recipes": recipes
        }