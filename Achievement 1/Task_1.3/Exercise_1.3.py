# Initialize lists for recipes and ingredients
recipes_list = []
ingredients_list = []

# Function to take user input for recipe variable names.
def take_recipe():
    name = str(input("Enter recipe name: "))
    cooking_time = int(input("Enter cooking time in minutes: "))
    ingredients = list(input("Enter ingredients: ").split(", "))
    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients
    }

    return recipe

# Prompt user for how many recipes they would like to enter.
n = int(input("How many recipes would you like to enter? " ))

# Iterate through number of use given recipes
for i in range(n):
    recipe = take_recipe()
    # Check if ingredient is in list, if not, add it to the list.
    for ingredient in recipe["ingredients"]:
        if not ingredient in ingredients_list:
            ingredients_list.append(ingredient)
        
    recipes_list.append(recipe)

# Iterate through recipes_list and assign difficulty.
for recipe in recipes_list:
    if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "Easy"
    elif recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4:
        recipe["difficulty"] = "Medium"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "Intermediate"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) >= 4:
        recipe["difficulty"] = "Hard"

# Display recipe info.
    print("----------------------------------------")
    print("Recipe: ", recipe["name"])
    print("Cooking time (min): ", recipe["cooking_time"])
    print("Ingredients: ", recipe["ingredients"])
    print("Difficulty: ", recipe["difficulty"])

# Display all ingredients in alphabetical order
def all_ingredients():
    print("Ingredients Available Across All Recipes")
    print("----------------------------------------")
    ingredients_list.sort()
    for ingredient in ingredients_list:
        print(ingredient)

all_ingredients()