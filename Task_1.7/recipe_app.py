# Import packages and methods
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Connecting SQLAlchemy with the database
engine = create_engine("mysql://cf-python:password@localhost/task_database")

# Create Declarative Base
Base = declarative_base()

# Create session object to make changes to database
Session = sessionmaker(bind=engine)
session = Session()

# Define Recipe model
class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    # Quick info on the recipe
    def __repr__(self):
        return f"<Recipe ID: {self.id} - Name: {self.name} - Difficulty: {self.difficulty}>"
    
    # Full recipe printout
    def __str__(self):
        return (
            f"{'-'*5}\n"
            f"Recipe: {self.name}\n"
            f"Cooking Time: {self.cooking_time} minutes\n"
            f"Ingredients: {self.ingredients}\n"
            f"Difficulty: {self.difficulty}\n"
            f"{'-'*5}"
        )
    
    # Calculate_difficulty function of recipe
    def calculate_difficulty(self):
        num_ingredients = len(self.ingredients.split(", "))
        if self.cooking_time < 10 and num_ingredients < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and num_ingredients >= 4:
            self.difficulty = "Hard"

    # Return ingredients as a list
    def return_ingredients_as_list(self):
        if not self.ingredients:  # Check if ingredients string is empty
            return []
        else:
            return self.ingredients.split(', ')

# Create all defined tables in the database
Base.metadata.create_all(engine)

# Main operations of recipe app

# Create Recipe
def create_recipe():
    # Prompt user for recipe name and validate
    while True:
        name = input("Enter name of recipe: ")
        if len(name) > 50:
            print("Error: Recipe name cannot be longer than 50 characters.")
        elif not name.isalpha():
            print("Error: Recipe name can only contain letters.")
        else:
            break
    
    # Prompt user for cooking time and validate
    while True:
        cooking_time = input("Enter recipe cooking time in minutes: ")
        if not cooking_time.isnumeric():
            print("Error: Cooking time must be a number.")
        else:
            cooking_time = int(cooking_time)
            break
        
    # Prompt user for ingredients
    ingredients = []
    n = int(input("How many ingredients would you like to enter?: "))

    for i in range(n):
        ingredient = input(f'Enter ingredient {i+1}: ')
        ingredients.append(ingredient)

    # Convert ingredients list to string
    ing_string = ', '.join(ingredients)

    # Create new Recipe object
    recipe_entry = Recipe(
        name = name,
        cooking_time = cooking_time,
        ingredients = ing_string
    )

    # Calculate and set difficulty
    recipe_entry.calculate_difficulty()

    # Add recipe to session and commit to database
    session.add(recipe_entry)
    session.commit()

    print("Recipe successfully added!")

# View all recipes
def view_all_recipes():
    # Query to retrieve all recipes in database as a list
    recipes_list = session.query(Recipe).all()

    # Check if list is empty
    if not recipes_list:
        print("No recipes found in the database.")
        return None
    
    # Call __str__ method to print all recipes
    for recipe in recipes_list:
        print(recipe)

# Search by ingredient
def search_by_ingredients():
    # Query to check for table entries
    recipe_count = session.query(Recipe).count()
    if recipe_count == 0:
        print("No recipes found in the database.")
        return None
    
    # Query to retrieve ingredients column only
    results = session.query(Recipe.ingredients).all()

    # Initialize empty ingredients list
    all_ingredients = []

    # Split ingredients into list and append to all_ingredients
    for result in results:
        ingredients_list = result[0].split(", ")
        for ingredient in ingredients_list:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)

    # Display available ingredients and prompt user which to search
    print("\nIngredients available: ")
    for idx, ingredient in enumerate(all_ingredients, start=1):
        print(f"{idx}. {ingredient}")
    selected_ingredients = input("Enter the numbers of ingredients you'd like to search, separated by spaces: ")

    # Validate user's input
    try:
        selected_indices = [int(i) for i in selected_ingredients.split()]
    except ValueError:
        print("Input invalid. Please enter numbers separated by spaces.")
        return None
    
    if any(i < 1 or i > len(all_ingredients) for i in selected_indices):
        print("Error: Selection invalid. Please enter numbers from the displayed options.")
        return None
    
    # Make list of selected ingredients to search for
    search_ingredients = [all_ingredients[i-1] for i in selected_indices]

    # Initialize empty conditions list
    conditions = []

    # Loop through search_ingredients and create like() conditions
    for ing in search_ingredients:
        like_term = f'%{ing}%'
        conditions.append(Recipe.ingredients.like(like_term))

    # Retrieve recipes from the database using filter() with conditions
    # Use 'and_' to combine the conditions so that all ingredients must be present
    from sqlalchemy import and_
    matching_recipes = session.query(Recipe).filter(and_(*conditions)).all()

    if not matching_recipes:
        print("No recipes found including all your selected ingredients.")
    else:
        for recipe in matching_recipes:
            print(recipe)

# Edit recipe
def edit_recipe():
    # Check if recipe exists
    recipe_count = session.query(Recipe).count()
    if recipe_count == 0:
        print("Recipe does not exist in database.")
        return None
    
    # Retrieve id and name of each recipe
    results = session.query(Recipe.id, Recipe.name).all()

    # Display recipes to user
    print("\nAvailable recipes:")
    for recipe in results:
        print(f"ID: {recipe.id} - Name: {recipe.name}")

    # Prompt user to select recipe by ID to update
    selected_id = input("Enter the ID of the recipe you would like to update: ")
    if not selected_id.isnumeric() or int(selected_id) not in [r.id for r in results]:
        print("Error: Recipe must be selected by its ID. Please try again.")
        return None
    
    # Retrieve recipe of selected ID
    recipe_to_edit = session.query(Recipe).filter_by(id=int(selected_id)).one()

    # Print the selected recipe details
    print("Recipe details:")
    print(f"1. Name: {recipe_to_edit.name}")
    print(f"2. Ingredients: {recipe_to_edit.ingredients}")
    print(f"3. Cooking Time: {recipe_to_edit.cooking_time} minutes")

    # Prompt user for field to update
    choice = input("enter the number of the field 1, 2, or 3 to update: ")
    if choice not in ["1", "2", "3"]:
        print("Invalid choice. Please choose 1, 2, or 3.")
        return None
    
    # Update attribute based on user's choice
    if choice == "1":
        new_name = input("Enter new recipe name: ")
        if len(new_name) > 50 or not new_name.isalpha():
            print("Error: Recipe's new name must be letters only and no longer than 50 characters.")
            return None
        recipe_to_edit.name = new_name

    elif choice == "2":
        new_ingredients = []
        n = int(input("How many ingredients would you like to add?: "))

        for i in range(n):
            ingredient = input(f"Enter ingredient {i+1}: ")
            new_ingredients.append(ingredient)

        recipe_to_edit.ingredients = ", ".join(new_ingredients)

    if choice == "3":
        new_time = input("Enter the new cooking time in minutes: ")
        if not new_time.isnumeric():
            print("Error: Cooking time must be entered as a number.")
            return None
        recipe_to_edit.cooking_time = int(new_time)
    
    # Recalculate difficulty of updated recipe
    recipe_to_edit.calculate_difficulty()

    session.commit()

    print("Recipe has been updated successfully!")

# Define main_menu function
def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Create a new recipe")
        print("2. Search for a recipe by ingredient")
        print("3. Update an existing recipe")
        print("4. Delete a recipe")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            create_recipe()
        elif choice == '2':
            search_by_ingredients()
        elif choice == '3':
            update_recipe()
        elif choice == '4':
            delete_recipe()
        elif choice == '5':
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please try again.")

    # Close the session before exiting
    session.close()
    print("Session closed.")

# Call the main_menu function
main_menu()
    
