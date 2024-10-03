# Import packages and methods
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import re

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
            print("\nError: Recipe name cannot be longer than 50 characters.")
        elif not name.replace(" ", "").isalpha():
            print("\nError: Recipe name can only contain letters.")
        else:
            break
    
    # Prompt user for cooking time and validate
    while True:
        cooking_time = input("Enter recipe cooking time in minutes: ")
        if not cooking_time.isnumeric():
            print("\nError: Cooking time must be a number.")
        else:
            cooking_time = int(cooking_time)
            break
        
    # Prompt user for ingredients
    ingredients = []
    n = int(input("How many ingredients would you like to enter?: "))

    for i in range(n):
        ingredient = input(f'Enter ingredient {i+1}: ').strip().title()
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

    print("\nRecipe successfully added!")

# View all recipes
def view_all_recipes():
    # Query to retrieve all recipes in database as a list
    recipes_list = session.query(Recipe).all()

    # Check if list is empty
    if not recipes_list:
        print("\nNo recipes found in the database.")
        return None
    
    # Call __str__ method to print all recipes
    for recipe in recipes_list:
        print(recipe)

# Search by ingredient
def search_by_ingredients():
    # Query to check for table entries
    recipe_count = session.query(Recipe).count()
    if recipe_count == 0:
        print("\nNo recipes found in the database.")
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
    selected_ingredients = input("\nEnter the numbers of ingredients you'd like to search, separated by spaces: ")

    # Validate user's input
    try:
        selected_indices = [int(i) for i in selected_ingredients.split()]
    except ValueError:
        print("\nInput invalid. Please enter numbers separated by spaces.")
        return None
    
    if any(i < 1 or i > len(all_ingredients) for i in selected_indices):
        print("\nError: Selection invalid. Please enter numbers from the displayed options.")
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
    # Use 'or_' to combine the conditions so that all ingredients must be present
    from sqlalchemy import or_
    matching_recipes = session.query(Recipe).filter(or_(*conditions)).all()

    if not matching_recipes:
        print("\nNo recipes found including all your selected ingredients.")
    else:
        for recipe in matching_recipes:
            print(recipe)

# Edit recipe
def edit_recipe():
    # Check if recipe exists
    recipe_count = session.query(Recipe).count()
    if recipe_count == 0:
        print("\nRecipe does not exist in database.")
        return None
    
    # Retrieve id and name of each recipe
    results = session.query(Recipe.id, Recipe.name).all()

    # Display recipes to user
    print("\nAvailable recipes:")
    for recipe in results:
        print(f"{recipe.id}. {recipe.name}")

    # Prompt user to select recipe by ID to update
    selected_id = input("\nEnter the ID number of the recipe you would like to update: ")
    if not selected_id.isnumeric() or int(selected_id) not in [r.id for r in results]:
        print("\nError: Recipe must be selected by its ID. Please try again.")
        return None
    
    # Retrieve recipe of selected ID
    recipe_to_edit = session.query(Recipe).filter_by(id=int(selected_id)).one()

    # Print the selected recipe details
    print("\nRecipe details:")
    print(f"1. Name: {recipe_to_edit.name}")
    print(f"2. Ingredients: {recipe_to_edit.ingredients}")
    print(f"3. Cooking Time: {recipe_to_edit.cooking_time} minutes")

    # Prompt user for field to update
    choice = input("\nEnter the number of the field 1, 2, or 3 to update: ")
    if choice not in ["1", "2", "3"]:
        print("\nInvalid choice. Please choose 1, 2, or 3.")
        return None
    
    # Update attribute based on user's choice
    if choice == "1":
        new_name = input("\nEnter new recipe name: ")
        # re.match("^[A-Za-z ]+$", new_name) allows for spaces in updated recipe names
        if len(new_name) > 50 or not re.match("^[A-Za-z ]+$", new_name):
            print("\nError: Recipe's new name must be letters only and no longer than 50 characters.")
            return None
        recipe_to_edit.name = new_name

    elif choice == "2":
        new_ingredients = []
        n = int(input("\nHow many ingredients are in this recipe?: "))

        for i in range(n):
            ingredient = input(f"Enter ingredient {i+1}: ")
            new_ingredients.append(ingredient)

        recipe_to_edit.ingredients = ", ".join(new_ingredients)

    if choice == "3":
        new_time = input("\nEnter the new cooking time in minutes: ")
        if not new_time.isnumeric():
            print("\nError: Cooking time must be entered as a number.")
            return None
        recipe_to_edit.cooking_time = int(new_time)
    
    # Recalculate difficulty of updated recipe
    recipe_to_edit.calculate_difficulty()

    session.commit()

    print("\nRecipe has been updated successfully!")

def delete_recipe():
    # Check if recipe exists
    recipe_count = session.query(Recipe).count()
    if recipe_count == 0:
        print("\nRecipe does not exist in database.")
        return None
    
    # Retrieve id and name of each recipe
    results = session.query(Recipe.id, Recipe.name).all()

    # Display recipes to user
    print("\nAvailable recipes:")
    for recipe in results:
        print(f"{recipe.id}. {recipe.name}")

    # Prompt user to select recipe by ID to update
    selected_id = input("Enter the ID of the recipe you would like to delete: ")
    if not selected_id.isnumeric() or int(selected_id) not in [r.id for r in results]:
        print("\nError: Recipe must be selected by its ID. Please try again.")
        return None
    
    # Convert input to integer
    selected_id = int(selected_id)

    # Retrieve recipe of selected ID
    recipe_to_delete = session.query(Recipe).filter_by(id=selected_id).one()

    # Confirm deletion
    choice = input(f"Are you sure you want to delete recipe '{recipe_to_delete.name}'? Enter 'Y' or 'N': ")

    # Action based on user choice
    if choice == 'N' or choice == 'n':
        print("\nRecipe not deleted.")
        return None
    
    elif choice == 'Y' or choice == 'y':
        session.delete(recipe_to_delete)
        session.commit()
        print("\nRecipe has been deleted.")

    else:
        print("\nInvalid choice. You must enter 'Y' or 'N'.")
        return None

# Define main_menu function
def main_menu():
    while True:
        print("\n-----------------------")
        print("Welcome to Recipe App!")
        print("-----------------------")
        print("\nMain Menu:")
        print("1. Create a new recipe")
        print("2. View all recipes")
        print("3. Search for a recipe by ingredient")
        print("4. Update an existing recipe")
        print("5. Delete a recipe")
        print("6. Exit")

        choice = input("\nEnter your choice: ")

        if choice == '1':
            create_recipe()
        elif choice == '2':
            view_all_recipes()
        elif choice == '3':
            search_by_ingredients()
        elif choice == '4':
            edit_recipe()
        elif choice == '5':
            delete_recipe()
        elif choice == '6':
            print("Exiting program.")
            print("\n-------------------------------")
            print("Thank you for using Recipe App!")
            print("-------------------------------\n")
            break
        else:
            print("\nInvalid choice. Please try again.")

    # Close the session before exiting
    session.close()
    print("Session closed.")

# Call the main_menu function
main_menu()
    
