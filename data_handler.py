import json
from models import Recipe, Ingredient

def save_recipes_to_json(recipes, filename='recipes.json'):
    with open(filename, 'w') as f:
        json.dump([{
            'name': recipe.name,
            'servings': recipe.servings,
            'ingredients': [
                {'name': ingredient.name, 'quantity': ingredient.quantity, 'unit': ingredient.unit}
                for ingredient in recipe.ingredients
            ]
        } for recipe in recipes], f, indent=4)

def load_recipes_from_json(filename='recipes.json'):
    try:
        with open(filename, 'r') as f:
            recipes_data = json.load(f)
            recipes = []
            for data in recipes_data:
                recipe = Recipe(data['name'], data['servings'])
                for ing in data['ingredients']:
                    ingredient = Ingredient(ing['name'], ing['quantity'], ing['unit'])
                    recipe.add_ingredient(ingredient)
                recipes.append(recipe)
            return recipes
    except FileNotFoundError:
        return []