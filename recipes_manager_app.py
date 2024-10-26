import customtkinter as ctk
from data_handler import save_recipes_to_json, load_recipes_from_json
from models import Recipe, Ingredient

class RecipesManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Recipes Manager")
        self.geometry("800x600")
        self.minsize(width=600, height=400)

        # Initialize recipes list
        # self.recipes = []  # This will store all the recipe objects
        self.recipes = load_recipes_from_json()  # This will store all the recipe objects

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
        self.view_recipes_button = ctk.CTkButton(menu_frame, text="View Recipes", command=lambda: self.show_frame("view_recipes_frame"))
        self.view_recipes_button.pack(side="left", padx=5, pady=5)

        self.add_recipe_button = ctk.CTkButton(menu_frame, text="Add Recipe", command=lambda: self.show_frame("add_recipe_frame"))
        self.add_recipe_button.pack(side="left", padx=5, pady=5)

        self.grocieries_button = ctk.CTkButton(menu_frame, text="Groceries", command=lambda: self.show_frame("groceries_frame"))
        self.grocieries_button.pack(side="right", padx=5, pady=5)

    def create_add_recipe_frame(self):

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
        cancel_button = ctk.CTkButton(self.frames["add_recipe_frame"], text="Cancel", command=lambda: self.show_frame("view_recipes_frame"))
        cancel_button.grid(row=5, column=0, columnspan=2, pady=5)

    def add_ingredient_entry(self):
        row = len(self.ingredients_entries)
        
        ingredient_entry = ctk.CTkEntry(self.ingredients_frame, width=200, height=30, placeholder_text="Ingredient")
        ingredient_entry.grid(row=row, column=0, padx=5, pady=5, sticky="ew")

        quantity_entry = ctk.CTkEntry(self.ingredients_frame, width=100, height=30, placeholder_text="Quantity")
        quantity_entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")

        unit_entry = ctk.CTkEntry(self.ingredients_frame, width=100, height=30, placeholder_text="Unit")
        unit_entry.grid(row=row, column=2, padx=5, pady=5, sticky="ew")

        self.ingredients_entries.append((ingredient_entry, quantity_entry, unit_entry))

    def create_groceries_frame(self):

        self.frames["groceries_frame"] = ctk.CTkFrame(self)
        self.frames["groceries_frame"].grid(row=1, column=0, padx=50, pady=50)

    def create_view_recipes_frame(self):
        # Reload the recipes from the JSON file
        self.recipes = load_recipes_from_json()
        # Create or refresh the frame for viewing recipes
        if "view_recipes_frame" in self.frames:
            # Destroy the existing frame before creating a new one
            self.frames["view_recipes_frame"].destroy()

        self.frames["view_recipes_frame"] = ctk.CTkFrame(self)
        self.frames["view_recipes_frame"].grid(row=1, column=0, padx=50, pady=50)

        self.frames["view_recipes_frame"].grid_rowconfigure(0, weight=1)
        self.frames["view_recipes_frame"].grid_columnconfigure(0, weight=1)
            
        # Add a title label
        title_label = ctk.CTkLabel(self.frames["view_recipes_frame"], text="Recipes List", font=ctk.CTkFont(size=18))
        title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Create a scrollable frame for the recipe list
        recipes_frame = ctk.CTkScrollableFrame(self.frames["view_recipes_frame"])
        recipes_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        recipes_frame.configure(width=600, height=350)
        recipes_frame.grid_columnconfigure(0, weight=1)

        # Add a back button to return to the main menu or other frames
        back_button = ctk.CTkButton(self.frames["view_recipes_frame"], text="Back", command=lambda: self.show_frame("add_recipe_frame"))
        back_button.grid(row=2, column=0, padx=10, pady=10)

        # Populate the scrollable frame with recipe details
        for i, recipe in enumerate(self.recipes):
            # Display recipe name and servings
            recipe_label = ctk.CTkLabel(recipes_frame, text=f"{recipe.name} (servings: {recipe.servings})", font=ctk.CTkFont(size=14, weight="bold"))
            recipe_label.grid(row=i*2, column=0, sticky="ew", padx=5, pady=5)

            # servings_label = ctk.CTkLabel(recipes_frame, text=f"(servings: {recipe.servings})", font=ctk.CTkFont(size=14, weight="bold"))
            # servings_label.grid(row=i*2+1, column=0, sticky="ew", padx=5, pady=5)

            # Display each ingredient in the recipe
            ingredients_text = "\n".join([f"{ing.name}: {ing.quantity} {ing.unit}" for ing in recipe.ingredients])
            ingredients_label = ctk.CTkLabel(recipes_frame, text=ingredients_text)
            ingredients_label.grid(row=i*2+1, column=0, sticky="ew", padx=20, pady=5)

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

        self.reset_form()

    def reset_form(self):
        # Clear the recipe name field
        self.recipe_name_entry.delete(0, 'end')

        # Remove all ingredient entries from the UI and clear the list
        for ingredient_entry, quantity_entry, unit_entry in self.ingredients_entries:
            ingredient_entry.destroy()
            quantity_entry.destroy()
            unit_entry.destroy()

        # Reset the ingredients_entries list
        self.ingredients_entries = []

        # Add a new blank ingredient entry to start fresh
        self.add_ingredient_entry()

    def show_frame(self, frame_name):
        # Destroy and recreate the frame to ensure it's always updated
        if frame_name == "view_recipes_frame":
            self.create_view_recipes_frame()
        # Create the frame if it doesn't exist
        elif frame_name not in self.frames:
            if frame_name == "add_recipe_frame":
                self.create_add_recipe_frame()
            elif frame_name == "groceries_frame":
                self.create_groceries_frame()

        # Hide all frames
        for frame in self.frames.values():
            frame.grid_remove()  # Hide all frames

        # Show the requested frame
        self.frames[frame_name].grid(sticky="nsew")  # Show the requested frame