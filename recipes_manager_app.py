import customtkinter as ctk
from tkinter import messagebox
from data_handler import save_recipes_to_json, load_recipes_from_json
from models import Recipe, Ingredient

class RecipesManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Recipes Manager")
        self.geometry("600x700")
        self.minsize(width=600, height=700)

        # Initialize recipes list
        # self.recipes = []
        self.recipes = load_recipes_from_json()

        self.frames = {}
        self.ingredients_entries = [] 

        self.create_menu_frame()

        self.show_frame("view_recipes_frame")

    def create_menu_frame(self):
        menu_frame = ctk.CTkFrame(self)
        menu_frame.grid(row=0, column=0, sticky="ew")
        
        self.grid_columnconfigure(0, weight=1)  

        self.view_recipes_button = ctk.CTkButton(menu_frame, text="View Recipes", command=lambda: self.show_frame("view_recipes_frame"))
        self.view_recipes_button.pack(side="left", padx=5, pady=5)

        self.add_recipe_button = ctk.CTkButton(menu_frame, text="Add Recipe", command=lambda: self.show_frame("add_recipe_frame"))
        self.add_recipe_button.pack(side="left", padx=5, pady=5)

        self.grocieries_button = ctk.CTkButton(menu_frame, text="Groceries", command=lambda: self.show_frame("groceries_frame"))
        self.grocieries_button.pack(side="right", padx=5, pady=5)

    def create_add_recipe_frame(self):

        self.frames["add_recipe_frame"] = ctk.CTkFrame(self)
        self.frames["add_recipe_frame"].grid(row=1, column=0, padx=50, pady=50)

        self.frames["add_recipe_frame"].grid_rowconfigure(0, weight=1)
        self.frames["add_recipe_frame"].grid_columnconfigure(0, weight=1)

        recipe_name_label = ctk.CTkLabel(self.frames["add_recipe_frame"], font=ctk.CTkFont(size=16, weight="bold"), text="Recipe Details")
        recipe_name_label.grid(row=0, column=0, padx=5, pady=5)

        # Frame for recipe details entry
        self.recipe_details_frame = ctk.CTkFrame(self.frames["add_recipe_frame"])
        self.recipe_details_frame.grid(row=1, column=0, columnspan=2, pady=5)

        # Frame for ingredients entry
        self.ingredients_frame = ctk.CTkFrame(self.frames["add_recipe_frame"])
        self.ingredients_frame.grid(row=2, column=0, columnspan=2, pady=5)

        self.add_recipe_entry()
        self.add_ingredient_entry()

        # Button to add more ingredients
        add_ingredient_button = ctk.CTkButton(self.frames["add_recipe_frame"], text="Add Ingredient", command=self.add_ingredient_entry)
        add_ingredient_button.grid(row=3, column=0, columnspan=2, pady=5)

        # Add a save button for the form
        save_button = ctk.CTkButton(self.frames["add_recipe_frame"], text="Save Recipe", command=self.save_recipe)
        save_button.grid(row=4, column=0, columnspan=2, pady=5)

        # Add a cancel button to clear fields
        cancel_button = ctk.CTkButton(self.frames["add_recipe_frame"], text="Cancel", command=self.reset_form)
        cancel_button.grid(row=5, column=0, columnspan=2, pady=5)

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
        title_label = ctk.CTkLabel(self.frames["view_recipes_frame"], text="Recipes List", font=ctk.CTkFont(size=16, weight="bold"))
        title_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        # Create a frame for the recipe list
        recipes_frame = ctk.CTkScrollableFrame(self.frames["view_recipes_frame"])
        recipes_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        recipes_frame.configure(width=600, height=470)
        recipes_frame.grid_columnconfigure(0, weight=1)

        # Add a back button to return to the main menu or other frames
        back_button = ctk.CTkButton(self.frames["view_recipes_frame"], text="Back", command=lambda: self.show_frame("add_recipe_frame"))
        back_button.grid(row=2, column=0, padx=5, pady=5)

        # Populate the frame with recipe details
        for i, recipe in enumerate(self.recipes):
            # Display recipe name and servings
            recipe_label = ctk.CTkLabel(recipes_frame, text=f"{recipe.name} (servings: {recipe.servings})", font=ctk.CTkFont(size=14, weight="bold"))
            recipe_label.grid(row=i*2, column=0, sticky="ew", padx=5, pady=5)

            # Display each ingredient in the recipe
            ingredients_text = "\n".join([f"{ing.name}: {ing.quantity} {ing.unit}" for ing in recipe.ingredients])
            ingredients_label = ctk.CTkLabel(recipes_frame, text=ingredients_text)
            ingredients_label.grid(row=i*2+1, column=0, sticky="ew", padx=20, pady=5)

            delete_button = ctk.CTkButton(recipes_frame, text="Delete", command=lambda idx=i: self.delete_recipe(idx))
            delete_button.grid(row=i*2, column=1, sticky="ew", padx=5, pady=5)

    def create_groceries_frame(self):
        # Create or refresh the frame for viewing the grocery list
        if "groceries_frame" in self.frames:
            # Destroy the existing frame before creating a new one
            self.frames["groceries_frame"].destroy()
            
        self.frames["groceries_frame"] = ctk.CTkFrame(self)
        self.frames["groceries_frame"].grid(row=1, column=0, padx=50, pady=50)

        self.frames["groceries_frame"].grid_rowconfigure(0, weight=1)
        self.frames["groceries_frame"].grid_columnconfigure(0, weight=1)
        
        # Add a title label
        title_label = ctk.CTkLabel(self.frames["groceries_frame"], text="Select Recipes", font=ctk.CTkFont(size=16, weight="bold"))
        title_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        # Create a frame for the recipe list
        recipes_frame = ctk.CTkScrollableFrame(self.frames["groceries_frame"])
        recipes_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        recipes_frame.grid_columnconfigure(0, weight=1)

        # A dictionary to keep track of selected recipes
        self.selected_recipes = {}

        # Populate the frame with recipe checkboxes
        for i, recipe in enumerate(self.recipes):
            # Create a checkbox for each recipe
            var = ctk.BooleanVar()
            self.selected_recipes[recipe.name] = var

            recipe_checkbox = ctk.CTkCheckBox(
                recipes_frame,
                text=f"{recipe.name} (Servings: {recipe.servings})",
                variable=var
            )
            recipe_checkbox.grid(row=i, column=0, sticky="w", padx=5, pady=5)
        
        # Add a button to generate the grocery list
        generate_button = ctk.CTkButton(self.frames["groceries_frame"], text="Generate Grocery List", command=self.generate_grocery_list)
        generate_button.grid(row=2, column=0, padx=5, pady=5)

        # Create a frame to display the generated grocery list
        self.grocery_list_frame = ctk.CTkScrollableFrame(self.frames["groceries_frame"])
        self.grocery_list_frame.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
        self.grocery_list_frame.grid_columnconfigure(0, weight=1)

        # Add a button to print the grocery list to a file
        print_button = ctk.CTkButton(self.frames["groceries_frame"], text="Print", command=self.print_grocery_list)
        print_button.grid(row=4, column=0, padx=5, pady=5)

    def generate_grocery_list(self):
        # Dictionary to store ingredients
        grocery_list = {}

        # Iterate over selected recipes
        for recipe in self.recipes:
            if self.selected_recipes[recipe.name].get():
                # For each selected recipe, add ingredients to the grocery list
                for ingredient in recipe.ingredients:
                    if ingredient.name in grocery_list:
                        # Add to the existing quantity if the ingredient is already in the list
                        grocery_list[ingredient.name]["quantity"] += int(ingredient.quantity)
                    else:
                        # Add a new entry for the ingredient
                        grocery_list[ingredient.name] = {
                            "quantity": int(ingredient.quantity),
                            "unit": ingredient.unit
                        }

        # Clear the previous grocery list frame
        for widget in self.grocery_list_frame.winfo_children():
            widget.destroy()

        # Display the grocery list in the grocery_list_frame
        for i, (ingredient, details) in enumerate(grocery_list.items()):
            ingredient_label = ctk.CTkLabel(
                self.grocery_list_frame,
                text=f"{ingredient}: {details['quantity']} {details['unit']}",
                font=ctk.CTkFont(size=14)
            )
            ingredient_label.grid(row=i, column=0, sticky="w", padx=5, pady=5)

    def print_grocery_list(self):
        # Dictionary to store ingredients
        grocery_list = {}

        # Iterate over selected recipes
        for recipe in self.recipes:
            if self.selected_recipes[recipe.name].get():
                # For each selected recipe, add ingredients to the grocery list
                for ingredient in recipe.ingredients:
                    if ingredient.name in grocery_list:
                        # Add to the existing quantity if the ingredient is already in the list
                        grocery_list[ingredient.name]["quantity"] += int(ingredient.quantity)
                    else:
                        # Add a new entry for the ingredient
                        grocery_list[ingredient.name] = {
                            "quantity": int(ingredient.quantity),
                            "unit": ingredient.unit
                        }

        # Create a formatted string for the grocery list
        grocery_list_str = ""
        for ingredient, details in grocery_list.items():
            grocery_list_str += f"{ingredient}: {details['quantity']} {details['unit']}\n"

        # Write the formatted grocery list to a text file
        with open("grocery_list.txt", "w") as file:
            file.write("Grocery List:\n")
            file.write(grocery_list_str)

        print("Grocery list saved to 'grocery_list.txt'.")
    
    def add_ingredient_entry(self):
        row = len(self.ingredients_entries)
        
        ingredient_entry = ctk.CTkEntry(self.ingredients_frame, width=200, height=30, placeholder_text="Ingredient")
        ingredient_entry.grid(row=row, column=0, padx=5, pady=5, sticky="ew")

        quantity_entry = ctk.CTkEntry(self.ingredients_frame, width=100, height=30, placeholder_text="Quantity")
        quantity_entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")

        unit_entry = ctk.CTkEntry(self.ingredients_frame, width=100, height=30, placeholder_text="Unit")
        unit_entry.grid(row=row, column=2, padx=5, pady=5, sticky="ew")

        self.ingredients_entries.append((ingredient_entry, quantity_entry, unit_entry))

    def add_recipe_entry(self):
        self.recipe_name_entry = ctk.CTkEntry(self.recipe_details_frame, width=310, height=30, placeholder_text="Recipe Name")
        self.recipe_name_entry.grid(row=1, column=0, padx=5, pady=5)

        self.servings_entry = ctk.CTkEntry(self.recipe_details_frame, width=100, height=30, placeholder_text="Servings")
        self.servings_entry.grid(row=1, column=1, padx=5, pady=5)

    def save_recipe(self):
        recipe_name = self.recipe_name_entry.get()
        servings = self.servings_entry.get()

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

    def delete_recipe(self, index):
        # Confirm deletion
        confirm = messagebox.askokcancel("Confirm Deletion", f"Are you sure you want to delete '{self.recipes[index].name}'?")
        if confirm:
            # Remove the recipe from the list
            deleted_recipe = self.recipes.pop(index)
            
            # Save the updated recipes list to JSON
            save_recipes_to_json(self.recipes)

            # Refresh the view
            print(f"Recipe '{deleted_recipe.name}' deleted successfully!")
            self.show_frame("view_recipes_frame")

    def reset_form(self):
        # Clear the recipe name field
        self.recipe_name_entry.delete(0, 'end')
        self.servings_entry.delete(0, 'end')

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
        elif frame_name == "groceries_frame":
                self.create_groceries_frame()
        # Create the frame if it doesn't exist
        elif frame_name not in self.frames:
            if frame_name == "add_recipe_frame":
                self.create_add_recipe_frame()
        
        # Hide all frames
        for frame in self.frames.values():
            frame.grid_remove()

        # Show the requested frame
        self.frames[frame_name].grid(sticky="nsew")