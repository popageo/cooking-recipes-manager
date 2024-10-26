import customtkinter as ctk
from data_handler import save_recipes_to_json
from models import Recipe, Ingredient

class RecipesManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Recipes Manager")
        self.geometry("800x600")
        self.minsize(width=600, height=400)

        # Initialize recipes list
        self.recipes = []  # This will store all the recipe objects

        # Create frames for different functionalities
        self.frames = {}
        self.ingredients_entries = [] 

        self.create_menu_frame()
        # self.create_add_recipe_frame()

        self.show_frame("add_recipe_frame")

    def create_menu_frame(self):
        menu_frame = ctk.CTkFrame(self)
        menu_frame.grid(row=0, column=0, sticky="ew")
        
        self.grid_columnconfigure(0, weight=1)  

        # Add buttons to the menu frame
        self.view_recipes_button = ctk.CTkButton(menu_frame, text="View Recipes")
        self.view_recipes_button.pack(side="left", padx=5, pady=5)

        self.add_recipe_button = ctk.CTkButton(menu_frame, text="Add Recipe", command=lambda: self.show_frame("add_recipe_frame"))
        self.add_recipe_button.pack(side="left", padx=5, pady=5)

        self.grocieries_button = ctk.CTkButton(menu_frame, text="Groceries")
        self.grocieries_button.pack(side="right", padx=5, pady=5)

    def create_add_recipe_frame(self):
        self.add_recipe_button.pack_forget()

        self.frames["add_recipe_frame"] = ctk.CTkFrame(self)
        self.frames["add_recipe_frame"].grid(row=1, column=0, padx=50, pady=50)

        # Configure row weights to allow expansion if needed
        self.frames["add_recipe_frame"].grid_rowconfigure(0, weight=1)
        self.frames["add_recipe_frame"].grid_columnconfigure(0, weight=1)

        recipe_name_label = ctk.CTkLabel(self.frames["add_recipe_frame"], font=ctk.CTkFont(size=16), text="Enter recipe details")
        recipe_name_label.grid(row=0, column=0, padx=5, pady=5)

        self.recipe_name_entry = ctk.CTkEntry(self.frames["add_recipe_frame"], width=420, height=30, placeholder_text="Enter recipe name")
        self.recipe_name_entry.grid(row=1, column=0, padx=5, pady=5)

        # self.servings_entry = ctk.CTkEntry(self.frames["add_recipe_frame"], width=100, height=30, placeholder_text="Servings")
        # self.servings_entry.grid(row=1, column=1, padx=5, pady=5)

        # Frame for ingredients
        self.ingredients_frame = ctk.CTkFrame(self.frames["add_recipe_frame"])
        self.ingredients_frame.grid(row=2, column=0, columnspan=2, pady=5)

        # Add the first pair of ingredient and quantity entries
        self.add_ingredient_entry()

        # Button to add more ingredients
        add_ingredient_button = ctk.CTkButton(self.frames["add_recipe_frame"], text="Add Ingredient", command=self.add_ingredient_entry)
        add_ingredient_button.grid(row=3, column=0, columnspan=2, pady=5)

        # Add a save button for the form
        save_button = ctk.CTkButton(self.frames["add_recipe_frame"], text="Save Recipe", command=self.save_recipe)
        save_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Add a cancel button to go back or clear fields
        cancel_button = ctk.CTkButton(self.frames["add_recipe_frame"], text="Cancel")
        cancel_button.grid(row=5, column=0, columnspan=2, pady=5)

        # self.grid_rowconfigure(1, weight=1)

    def add_ingredient_entry(self):
        row = len(self.ingredients_entries)
        
        ingredient_entry = ctk.CTkEntry(self.ingredients_frame, width=200, height=30, placeholder_text="Ingredient")
        ingredient_entry.grid(row=row, column=0, padx=5, pady=5, sticky="ew")

        quantity_entry = ctk.CTkEntry(self.ingredients_frame, width=100, height=30, placeholder_text="Quantity")
        quantity_entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")

        unit_entry = ctk.CTkEntry(self.ingredients_frame, width=100, height=30, placeholder_text="Unit")
        unit_entry.grid(row=row, column=2, padx=5, pady=5, sticky="ew")

        # Add the pair to the list for later access
        self.ingredients_entries.append((ingredient_entry, quantity_entry, unit_entry))

    def create_groceries_frame(self):
        self.grocieries_button.pack_forget()

        self.frames["groceries_frame"] = ctk.CTkFrame(self)
        self.frames["groceries_frame"].grid(row=1, column=0, padx=50, pady=50)

    def save_recipe(self):
        recipe_name = self.recipe_name_entry.get()
        servings = 1 # self.servings_entry.get()

        if not recipe_name or not servings:
            print("Please enter recipe name and servings.")
            return

        ingredients = []
        for ingredient_entry, quantity_entry, unit_entry in self.ingredients_entries:
            ingredient_name = ingredient_entry.get()
            quantity = quantity_entry.get()
            unit = unit_entry.get()

            if ingredient_name and quantity and unit:
                ingredient = Ingredient(ingredient_name, quantity, unit)
                ingredients.append(ingredient)

        # new_recipe = Recipe(name=recipe_name, servings=servings)
        new_recipe = Recipe(recipe_name, servings)
        new_recipe.ingredients = ingredients
        self.recipes.append(new_recipe)

        save_recipes_to_json(self.recipes)

        print(f"Recipe '{recipe_name}' saved successfully!")

    # def save_recipe(self):
    #     # Gather the recipe details
    #     recipe_name = self.recipe_name_entry.get()
    #     ingredients = []

    #     # Collect all ingredients and their details
    #     for ingredient_entry, quantity_entry, unit_entry in self.ingredients_entries:
    #         ingredient = ingredient_entry.get()
    #         quantity = quantity_entry.get()
    #         unit = unit_entry.get()
    #         if ingredient and quantity and unit:
    #             ingredients.append({
    #                 "ingredient": ingredient,
    #                 "quantity": quantity,
    #                 "unit": unit
    #             })

    #     # Create the recipe dictionary
    #     recipe_data = {
    #         "name": recipe_name,
    #         "ingredients": ingredients
    #     }

    #     # Load existing recipes, add the new one, and save them back to the JSON file
    #     try:
    #         with open('recipes.json', 'r') as f:
    #             recipes = json.load(f)
    #     except (FileNotFoundError, json.JSONDecodeError):
    #         recipes = []

    #     recipes.append(recipe_data)

    #     # Save the updated list to the JSON file
    #     with open('recipes.json', 'w') as f:
    #         json.dump(recipes, f, indent=4)

    #     print("Recipe saved successfully!")

    def show_frame(self, frame_name):
        self.create_add_recipe_frame()
        # self.create_groceries_frame()
        for frame in self.frames.values():
            frame.grid_remove()  # Hide all frames
        self.frames[frame_name].grid(sticky="nsew")  # Show the requested frame