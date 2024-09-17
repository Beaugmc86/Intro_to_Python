import pickle

# Define function to prompt user and input recipe.
def take_recipe():
    name = input("Enter your recipe name: ").strip()
    cooking_time = int(input("Enter the cooking time (in minutes): "))
    ingredients_input = input("Enter your ingredients, seperated by a comma: ").strip()
    ingredients = [ingredient.strip() for ingredient in ingredients_input.split(",") if ingredient.strip()]
    difficulty = calc_difficulty(cooking_time, len(ingredients))
    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients,
        "difficulty": difficulty
    }
    return recipe

# Define function to calculate recipe difficulty.
def calc_difficulty(cooking_time, num_ingredients):
    if cooking_time < 10 and num_ingredients < 4:
        return "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        return "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        return "Intermediate"
    else:
        return "Hard"
    
# Main Script - Prompt user for filename
filename = input("Please enter filename to save recipes: ")

# Load data and check if recipe already exists, if not one will be created.
try:
    with open(filename, "rb") as file:
        data = pickle.load(file)
except FileNotFoundError:
    data = {"recipes_list": [], "all_ingredients": []}
except Exception as e:
    print(f"An error occured: {e}")
    data = {"recipes_list": [], "all_ingredients": []}

recipes_list, all_ingredients = data["recipes_list"], data["all_ingredients"]

# Prompt user for how many recipes they'd like to enter and append recipe.
number_of_recipes = int(input("\nHow many recipes would you like to enter?: "))

for i in range(number_of_recipes):
    recipe = take_recipe()
    recipes_list.append(recipe)
    for ingredient in recipe["ingredients"]:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)

# Save updated data back to the file
data = {"recipes_list": recipes_list, "all_ingredients": all_ingredients}
    
with open(filename, "wb") as file:
    pickle.dump(data, file)

print("\nRecipes saved successfully!")