from flask import Blueprint, request, jsonify
from flask_api import status
from  RecipeSharingSite.controllers.ingredient_controller import IngredientController

ingredient_API = Blueprint('ingredient_API', __name__)


@ingredient_API.route('/ingredients/')
def get_all_ingredients():
    return "", status.HTTP_501_NOT_IMPLEMENTED


@ingredient_API.route('/ingredients/recipes/<ingredient_id>')
def get_recipes_that_use_ingredient(ingredient_id):
    return "", status.HTTP_501_NOT_IMPLEMENTED


@ingredient_API.route('/ingredients/recipes/<recipe_id>')
def get_ingredients_used_in_recipe(recipe_id):
    return "", status.HTTP_501_NOT_IMPLEMENTED
