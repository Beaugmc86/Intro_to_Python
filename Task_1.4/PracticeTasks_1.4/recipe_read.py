import pickle

with open("recipe_binary.bin", "rb") as my_file:
    recipe = pickle.load(my_file)

print("---- Recipe details ----")
print("Name: " + recipe["Name"])
print("Ingredients: " + str(recipe["Ingredients"]))
print("Cooking Time: " + recipe["Cooking_time"])
print("Difficulty: " + recipe["Difficulty"])