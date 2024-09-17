import pickle

# Define function to display recipe
def display_recipe(recipe):
    print(f"\nRecipe: {recipe['name'].title()}")
    print(f"  Time: {recipe['cooking_time']} mins")
    print("  Ingredients:")
    for ingredient in recipe["ingredients"]:
        print(f"  - {ingredient.title()}")
    print(f"  Difficulty: {recipe['difficulty']}")

# Define function to search for recipes with specific ingredient.
def search_ingredient(data):
    all_ingredients = data["all_ingredients"]

    # Display fill ingredients list
    print("\nIngredients List ")
    print("------------------")
    for i, ingredient in enumerate(all_ingredients):
        print(f"{i+1}.) {ingredient.title()}")

    # Validate user input for selecting an ingredient
    try:
        # Get user input for ingredient choice
        ingredient_number = int(input("\nEnter the number of the ingredient to search: "))
        
        # Check if the input is within valid range
        if 1 <= ingredient_number <= len(all_ingredients):
            ingredient_searched = all_ingredients[ingredient_number-1]
        else:
            print(f"Please enter a number between 1 and {len(all_ingredients)}.")
            return  # Exit the function if the input is invalid
        
        # Find recipes containing the chosen ingredient
        recipes_with_ingredient = [recipe for recipe in data["recipes_list"] if ingredient_searched in recipe["ingredients"]]
        num_recipes = len(recipes_with_ingredient)

        # Display count of found recipes
        recipe_word = "Recipe(s)"

        decoration = "-" * (len(f"{num_recipes} {recipe_word} found containing {ingredient_searched.title()}") + 2)
        print(f"\n{decoration}")
        print(f" {num_recipes} {recipe_word} found containing {ingredient_searched.title()} ")
        print(f"{decoration}")

        # Display each found recipes
        for recipe in recipes_with_ingredient:
            display_recipe(recipe)

    # Handle Errors
    except ValueError:
        print("Invalid input! Please enter a number.")
    except IndexError:
        print("No such ingredient number.")

# Main Script - Propt user for filename
filename = input("Enter the filename of your recipe data: ")

# Load data from the file and search for recipes
try:
    with open(filename, "rb") as file:
        data = pickle.load(file)
except FileNotFoundError:
    print("File not found. Please check the filename and try again.")
else:
    search_ingredient(data)
