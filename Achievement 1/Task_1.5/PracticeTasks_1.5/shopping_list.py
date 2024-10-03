class ShoppingList(object):
    # Initialize data attributes.
    def __init__(self, list_name):
        self.list_name = list_name
        self.shopping_list= []

    # Add item method.
    def add_item(self, item):
        if item not in self.shopping_list:
            self.shopping_list.append(item)
            print(f"{item} has been added to the list.")
        else:
            print(f"{item} is already in the list.")

    # Remove item method.
    def remove_item(self, item):
        if item in self.shopping_list:
            self.shopping_list.remove(item)
            print(f"{item} has been removed from list.")
        else:
            print(f"{item} is not in the list")

    # View list method.
    def view_list(self):
        print(f"Shopping List: ({self.list_name}):")
        for item in self.shopping_list:
            print(f" - {item}")

# Create an object called pet_store_list
pet_store_list = ShoppingList("Pet Store Shopping List")

# Add items to the list
pet_store_list.add_item("dog food")
pet_store_list.add_item("frisbee")
pet_store_list.add_item("bowl")
pet_store_list.add_item("collars")
pet_store_list.add_item("flea collars")

# Remove "flea collars" from the list
pet_store_list.remove_item("flea collars")

# Try adding "frisbee" again to the list
pet_store_list.add_item("frisbee")

# Display the entire shopping list
pet_store_list.view_list()