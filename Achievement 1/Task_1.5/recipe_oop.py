class Recipe:
    # Class variable to store all unique ingredients for all recipes
    all_ingredients = set()

    # Initiailization method
    def __init__(self, name, cooking_time):
        self.name = name
        self.ingredients = []
        self.cooking_time = cooking_time
        self.difficulty = None
    
    # Method to calc difficulty of recipe based on cooking time and number of ingredients.
    def calculate_difficulty(self):
        num_ingredients = len(self.ingredients)
        if self.cooking_time < 10:
            self.difficulty = "Easy" if num_ingredients < 4 else "Medium"
        else:
            self.difficulty = "Intermediate" if num_ingredients < 4 else "Hard"

    # Method to add ingredients to recipe and update all ingredients list
    def add_ingredients(self, *args):
        for ingredient in args:
            self.ingredients.append(ingredient)
            self.update_all_ingredients(ingredient)
        self.calculate_difficulty()

    # Getter method for name of recipe
    def get_name(self):
        return self.name
    
    # Setter method for name of recipe
    def set_name(self, name):
        self.name = name

    # Getter method for recipe cooking time
    def get_cooking_time(self):
        return self.cooking_time
    
    # Setter method for recipe cooking time and calc difficulty
    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time
        self.calculate_difficulty()

    # Getter method to return list of recipe ingredients
    def get_ingredients(self):
        return self.ingredients
    
    # Getter method to return difficulty if it has not already been calculated
    def get_difficulty(self):
        if self.difficulty is None:
            self.calculate_difficulty()
        return self.difficulty
    
    # Method to check if ingredient is in the recipe
    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients
    
    # Method to update class variable with any new ingredients
    def update_all_ingredients(self, ingredient):
        Recipe.all_ingredients.add(ingredient)

    # String representation that prints out the recipe.
    def __str__(self):
        ingredients_str = ', '.join(self.ingredients)
        return (
            f"Recipe: {self.name}\n"
            f"Cooking Time: {self.cooking_time} mins\n"
            f"Ingredients: {ingredients_str}\n"
            f"Difficulty: {self.difficulty}\n"
        )
    
def recipe_search(recipes, search_term):
    for recipe in recipes:
        if recipe.search_ingredient(search_term):
            print(recipe)

# Display Recipes
print("---------")
print(" Recipes")  
print("---------\n")        

tea = Recipe("Tea", 5)
tea.add_ingredients("Tea Leaves", "Sugar", "Water")
print(tea)

coffee = Recipe("Coffee", 5)
coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
print(coffee)

cake = Recipe("Cake", 50)
cake.add_ingredients("Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk")
print(cake)

banana_smoothie = Recipe("Banana Smoothie", 5)
banana_smoothie.add_ingredients("Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")
print(banana_smoothie)


# Creating a list of recipes and searching for an ingredient
recipes_list = [tea, coffee, cake, banana_smoothie]


# Searching for recipes containing specific ingredients
print("----------------------------------")
print(" Recipes with searched ingredients")
print("----------------------------------")

print("---------------------")
print("Recipes with Water:")
print("---------------------")
recipe_search(recipes_list, "Water")

print("---------------------")
print("Recipes with Sugar:")
print("---------------------")
recipe_search(recipes_list, "Sugar")

print("---------------------")
print("Recipes with Bananas:")
print("---------------------")
recipe_search(recipes_list, "Bananas")