import mysql.connector
import sys  # Import sys module to use sys.exit()

# Initialize and connect to mysql
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='cf-python',
        passwd='password'
    )
    cursor = conn.cursor()
    print("Database connection successful!")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    sys.exit(1)  # Exit the script with an error code

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

cursor.execute("USE task_database")

cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
               id INT AUTO_INCREMENT PRIMARY KEY,
               name VARCHAR(50),
               ingredients VARCHAR(255),
               cooking_time INT,
               difficulty VARCHAR(20)
)''')

def main_menu(conn, cursor):
    choice = ""
    while(choice != "quit"):
        print("\n===================================================")
        print("  What would you like to do? Pick a choice below!  ")
        print("===================================================\n")
        print("1. Create a new recipe")
        print("2. Search for recipe by ingredient")
        print("3. Update an existing recipe")
        print("4. Delete a recipe\n")
        print("Type 'quit' to exit the program\n")
        choice = input("Your choice: ").strip().lower()
        print()

        if choice in ["1", "2", "3", "4"]:
            if choice == "1":
                create_recipe(conn, cursor)
            elif choice == "2":
                search_recipe(conn, cursor)
            elif choice == "3":
                update_recipe(conn, cursor)
            elif choice == "4":
                delete_recipe(conn, cursor)
        elif choice == "quit":
            print("=======================================")
            print("  Thank you for using the recipe app!  ")
            print("=======================================")
            break
        else:
            print("==================================================")
            print("Choice invalid! Pleae enter 1, 2, 3, 4, or 'quit'.")
            print("==================================================")
            print("...returning to main menu\n\n")

    conn.close()

# Calculate recipe difficulty
def calculate_difficulty(cooking_time, ingredients):
    num_ingredients = len(ingredients.split(","))
    if cooking_time < 10 and num_ingredients < 4:
        return "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        return "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        return "Intermediate"
    elif cooking_time >= 10 and num_ingredients >= 4:
        return "Hard"

# Recipe display
def format_recipe_display(recipe):
    print(f"\n{recipe[0]}. Recipe: {recipe[1].title()}")
    print(f"   Time: {recipe[3]} mins")
    print("   Ingredients:")
    for ingredient in recipe[2].split(", "):
        print(f"   - {ingredient.title()}")
    print(f"   Difficulty: {recipe[4]}") 

def sanitize_ingredients(ingredients):
    # Split by comma, trim spaces, and remove empty entries
    return ', '.join([ingredient.strip() for ingredient in ingredients.split(',') if ingredient.strip()])

# Create recipe
def create_recipe(conn, cursor):
    name = input("Enter recipe name: ")

    # Input validation for cooking time
    while True:
        try:
            cooking_time = int(input("Enter cooking time in minutes: "))
            if cooking_time < 0:  # Optional: Ensure cooking time is non-negative
                print("Cooking time cannot be negative. Please enter a valid number.")
                continue
            break  # Exit the loop if input is valid
        except ValueError:
            print("Invalid input! Please enter a number for cooking time.")

    ingredients = input("Enter the ingredients (comma-separated): ")
    difficulty = calculate_difficulty(cooking_time, ingredients)

    # Sanitize the ingredients input
    sanitized_ingredients = sanitize_ingredients(ingredients)

    insert_query = '''
    INSERT INTO Recipes(name, ingredients, cooking_time, difficulty)
    VALUES (%s, %s, %s, %s)
    '''
    cursor.execute(insert_query, (name, ingredients, cooking_time, difficulty))

    conn.commit()
    print("\nRecipe added successfully!")

# Search for recipe by ingredient
def search_recipe(conn, cursor):
    #Extract all ingredients from the Recipes table
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()

    all_ingredients = set() # Use of set to avoid duplicates

    # Process results and split each string of ingredients into individual items
    for row in results:
        ingredients_str = row [0]
        ingredients_list = [ingredient.strip().lower() for ingredient in ingredients_str.split(',')]
        all_ingredients.update(ingredients_list)

    all_ingredients = sorted(list(all_ingredients)) # Convert set to a sorted list

    # Display the list of unique ingredients
    print("Available ingredients: ")
    for idx, ingredient in enumerate(all_ingredients, 1):
        print(f"{idx}. {ingredient.title()}") # Display ingredients with numbers
    
    # Get user's selection
    while True:
        try:
            choice = int(input(f"Pick an ingredient by number (1-{len(all_ingredients)}): "))
            if 1 <= choice <= len(all_ingredients):
                search_ingredient = all_ingredients[choice - 1]  # Get the selected ingredient
                break
            else:
                print(f"Please enter a number between 1 and {len(all_ingredients)}.")
        except ValueError:
            print("Invalid input, please enter a number.")

    # Search for recipes containing the selected ingredient
    search_query = '''
    SELECT * FROM Recipes WHERE ingredients LIKE %s
    '''

    # Use %search_ingredient% to find recipes containing the ingredient anywhere in the string
    cursor.execute(search_query, ('%' + search_ingredient + '%',))
    results = cursor.fetchall()

    # Display the results
    if results:
        print(f"\nRecipes containing '{search_ingredient}':")
        for recipe in results:
            format_recipe_display(recipe)
    
    else:
        print(f"No recipes found with the ingredient: {search_ingredient}")

# Update recipes
def update_recipe(conn, cursor):
    # Fetch and display all recipes
    cursor.execute("SELECT id, name, ingredients, cooking_time, difficulty FROM Recipes")
    recipes = cursor.fetchall()

    if not recipes:
        print("No recipes available to update.")
        return
    
    print("Available recipes: ")
    for recipe in recipes:
        format_recipe_display(recipe) 

    # Get the recipe id to update
    while True:
        try:
            recipe_id = int(input("\nEnter the ID of the recipe you want to update: "))
            if any(recipe[0] == recipe_id for recipe in recipes):
                break
            else:
                print("\nInvalid ID, please select a valid recipe ID.")
        except ValueError:
            print("\nPlease enter a valid number.")
    
    # Select column to update
    print("\nWhat would you like to update?")
    print("  1. Name")
    print("  2. Cooking Time")
    print("  3. Ingredients")
    while True:
        column_choice = input("\nEnter your choice (1-3): ").strip()
        if column_choice in ["1", "2", "3"]:
            break
        print("\nInvalid choice, please enter 1, 2, or 3.")

    # Collect the new value and prepare the update query
    if column_choice == "1":  # Update recipe name
        new_value = input("\nEnter the new recipe name: ").strip()
        query = "UPDATE Recipes SET name = %s WHERE id = %s"
        cursor.execute(query, (new_value, recipe_id))

    elif column_choice == "2":  # Update cooking time
        new_cooking_time = int(input("\nEnter the new cooking time in minutes: "))
        # Update cooking time
        query = "UPDATE Recipes SET cooking_time = %s WHERE id = %s"
        cursor.execute(query, (new_cooking_time, recipe_id))
        
        # Fetch current ingredients to recalculate difficulty
        cursor.execute("SELECT ingredients FROM Recipes WHERE id = %s", (recipe_id,))
        ingredients = cursor.fetchone()[0]
        
        # Recalculate difficulty
        new_difficulty = calculate_difficulty(new_cooking_time, ingredients)
        # Update difficulty in the database
        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (new_difficulty, recipe_id))

    elif column_choice == "3":  # Update ingredients
        new_ingredients = input("Enter the new ingredients (comma-separated): ").strip()
        sanitized_ingredients = sanitize_ingredients(new_ingredients)
        
        # Update ingredients
        query = "UPDATE Recipes SET ingredients = %s WHERE id = %s"
        cursor.execute(query, (sanitized_ingredients, recipe_id))
        
        # Fetch current cooking time to recalculate difficulty
        cursor.execute("SELECT cooking_time FROM Recipes WHERE id = %s", (recipe_id,))
        cooking_time = cursor.fetchone()[0]
        
        # Recalculate difficulty
        new_difficulty = calculate_difficulty(cooking_time, sanitized_ingredients)
        # Update difficulty in the database
        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (new_difficulty, recipe_id))

    # Commit changes
    conn.commit()
    print("\nRecipe updated successfully!")
    cursor.execute("SELECT * FROM Recipes WHERE id = %s", (recipe_id,))
    updated_recipe = cursor.fetchone()
    format_recipe_display(updated_recipe)

# Delete recipe
def delete_recipe(conn, cursor):
    # Fetch and display all recipes
    cursor.execute("SELECT id, name FROM Recipes")
    recipes = cursor.fetchall()
    
    if not recipes:
        print("\nNo recipes available to delete.")
        return

    # Display the list of recipes with IDs
    print("Available recipes:")
    for recipe in recipes:
        print(f"{recipe[0]}. {recipe[1]}")

    # Get the recipe ID to delete
    while True:
        try:
            recipe_id = int(input("\nEnter the ID of the recipe you want to delete: "))
            if any(recipe[0] == recipe_id for recipe in recipes):
                break
            else:
                print("\nInvalid ID, please select a valid recipe ID.")
        except ValueError:
            print("\nPlease enter a valid number.")

    # Execute the DELETE query
    delete_query = "DELETE FROM Recipes WHERE id = %s"
    cursor.execute(delete_query, (recipe_id,))

    # Commit changes
    conn.commit()
    print("\nRecipe deleted successfully!")

if __name__ == "__main__":
    main_menu(conn, cursor)
    print("Script has completed.")