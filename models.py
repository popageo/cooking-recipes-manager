class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.name}"

    def __repr__(self):
        return f"Ingredient(name={self.name}, quantity={self.quantity}, unit={self.unit})"

class Recipe:
    def __init__(self, name, servings):
        self.name = name
        self.servings = servings
        self.ingredients = []

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def __str__(self):
        ingredients_list = ', '.join(str(ingredient) for ingredient in self.ingredients)
        return f"{self.name} (Serves {self.servings}): {ingredients_list}"

    def __repr__(self):
        return f"Recipe(name={self.name}, servings={self.servings}, ingredients={self.ingredients})"