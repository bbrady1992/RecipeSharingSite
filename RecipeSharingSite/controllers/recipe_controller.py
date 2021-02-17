from RecipeSharingSite.models.recipe import Recipe
from RecipeSharingSite.models.user import User
from RecipeSharingSite.models.comment import Comment
from RecipeSharingSite import db
from datetime import datetime
import pytz


class RecipeController:
    @staticmethod
    def get_all_recipes():
        return {"recipe_ids": [{'id': r.id} for r in Recipe.query.all()]}


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
            db.session.rollback()
            db.session.flush()
            return False

    @staticmethod
    def recipe_exists(recipe_id):
        return True if Recipe.query.get(recipe_id) is not None else False

    @staticmethod
    def get_comments_for_recipe(recipe_id):
        recipe = Recipe.query.get(recipe_id)
        return {'comment_ids': [{'id': c.id} for c in recipe.comments]}

    @staticmethod
    def post_comment_on_recipe(recipe_id, user_id, content):
        recipe = Recipe.query.get(recipe_id)
        user = User.query.get(user_id)
        new_comment = Comment(user=user, content=content, submitted_on=datetime.now(pytz.UTC))
        recipe.comments.extend([new_comment])
        db.session.commit()
        return new_comment.to_dict()

