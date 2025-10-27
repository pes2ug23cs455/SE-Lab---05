
import json
import logging
from datetime import datetime

# Configure a basic logger to track runtime activity
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Global data store for all stock-related information
warehouse_data = {}


def addItem(item="unknown", qty=0, logs=None):  # pylint: disable=invalid-name
    """Insert or update product quantities in the warehouse record."""
    if logs is None:
        logs = []

    if not isinstance(item, str) or not isinstance(qty, int):
        logging.warning("Invalid argument types: item must be a string and qty must be an integer.")
        return

    warehouse_data[item] = warehouse_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Recorded {qty} units of {item}")


def removeItem(item, qty):  # pylint: disable=invalid-name
    """Decrease quantity of a product, removing it if stock reaches zero."""
    try:
        warehouse_data[item] -= qty
        if warehouse_data[item] <= 0:
            del warehouse_data[item]
    except KeyError:
        logging.warning("Attempted to remove a non-existent item: '%s'", item)
    except TypeError:
        logging.error("Invalid data type used when adjusting stock for '%s'.", item)


def getQty(item):  # pylint: disable=invalid-name
    """Return the available quantity of the requested product."""
    return warehouse_data.get(item, 0)


def loadData(file="inventory_data.json"):  # pylint: disable=invalid-name, global-statement
    """Import warehouse details from an external JSON file."""
    global warehouse_data
    try:
        with open(file, "r", encoding="utf-8") as source_file:
            warehouse_data = json.load(source_file)
    except FileNotFoundError:
        logging.warning("No existing inventory file found. Starting fresh.")


def saveData(file="inventory_data.json"):  # pylint: disable=invalid-name
    """Export the current stock details to a JSON file."""
    with open(file, "w", encoding="utf-8") as destination_file:
        json.dump(warehouse_data, destination_file, indent=4)


def printData():  # pylint: disable=invalid-name
    """Display a formatted summary of all inventory records."""
    print("=== Inventory Summary ===")
    for item, quantity in warehouse_data.items():
        print(f"{item}: {quantity}")


def checkLowItems(threshold=5):  # pylint: disable=invalid-name
    """Return a list of products that are below the provided stock limit."""
    return [item for item, quantity in warehouse_data.items() if quantity < threshold]

def main():
    addItem("apple", 10)
    addItem("banana", -2)
    addItem(123, "ten")  # invalid types, no check
    removeItem("apple", 3)
    removeItem("orange", 1)
    print("Apple stock:", getQty("apple"))
    print("Low items:", checkLowItems())
    saveData()
    loadData()
    printData()

main()
