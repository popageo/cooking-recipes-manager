import customtkinter as ctk

class RecipesManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Recipes Manager")
        self.geometry("800x600")

        self.create_menu_frame()
        self.test()

    def create_menu_frame(self):
        menu_frame = ctk.CTkFrame(self)
        menu_frame.grid(row=0, column=0, sticky="ew")
        
        self.grid_columnconfigure(0, weight=1)  

        # Add buttons to the menu frame
        self.recipe_list_button = ctk.CTkButton(menu_frame, text="Recipes")
        self.recipe_list_button.pack(side="left", padx=5, pady=5)

        self.add_recipe_button = ctk.CTkButton(menu_frame, text="Add Recipe")
        self.add_recipe_button.pack(side="left", padx=5, pady=5)

        self.grocieries_button = ctk.CTkButton(menu_frame, text="Groceries")
        self.grocieries_button.pack(side="right", padx=5, pady=5)

    def test(self):
        test_frame = ctk.CTkFrame(self)
        test_frame.grid(row=1, column=0, sticky="nsew")
        
        self.grid_rowconfigure(1, weight=1)
        # self.grid_columnconfigure(0, weight=1)

        self.add_recipe_button.pack_forget()

app = RecipesManagerApp()
app.mainloop()