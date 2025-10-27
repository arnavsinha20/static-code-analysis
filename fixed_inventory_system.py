import json
from datetime import datetime


# Global variable for storing inventory data
stock_data = {}


def add_item(item="default", qty=0, logs=None):
    if logs is None:
        logs = []

    if not item or not isinstance(item, str):
        print(f"Warning: Invalid item name '{item}'")
        return

    if not isinstance(qty, int) or qty < 0:
        print(f"Warning: Invalid quantity '{qty}' for item '{item}'")
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")


def remove_item(item, qty):
    try:
        if item not in stock_data:
            raise KeyError(f"Item '{item}' not found in inventory")

        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError as e:
        print(f"Error removing item: {e}")
    except TypeError as e:
        print(f"Error with quantity type: {e}")


def get_qty(item):
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    global stock_data
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.load(f)
    except FileNotFoundError:
        print(
            f"Warning: File '{file}' not found. "
            f"Starting with empty inventory."
        )
        stock_data = {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{file}'")
        stock_data = {}


def save_data(file="inventory.json"):
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=2)
    except IOError as e:
        print(f"Error saving data: {e}")


def print_data():
    print("Items Report")
    for item_name, quantity in stock_data.items():
        print(f"{item_name} -> {quantity}")


def check_low_items(threshold=5):
    result = []
    for item_name, quantity in stock_data.items():
        if quantity < threshold:
            result.append(item_name)
    return result


def main():
    add_item("apple", 10)
    add_item("banana", -2)  # Will show warning for invalid quantity
    add_item(123, "ten")  # Will show warning for invalid types
    remove_item("apple", 3)
    remove_item("orange", 1)  # Will show error - item not found
    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")
    save_data()
    load_data()
    print_data()
    # Removed eval() - it's a dangerous security vulnerability
    print("Inventory operations completed")


if __name__ == "__main__":
    main()