"""
menu_service.py
---------------
Service layer for menu-related operations.
Handles reading menu data from the JSON file.
"""

import json
import os

# Path to the menu data file (relative to this service file)
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
MENU_FILE = os.path.join(DATA_DIR, "menu.json")


def get_all_menu_items():
    """
    Reads and returns all menu items from menu.json.
    
    Returns:
        list: A list of dictionaries, each representing a menu item.
              Each item has: id, name, emoji, price, category, description.
    """
    try:
        with open(MENU_FILE, "r", encoding="utf-8") as file:
            menu_items = json.load(file)
        return menu_items
    except FileNotFoundError:
        # If the file doesn't exist, return an empty list
        return []
    except json.JSONDecodeError:
        # If the file has invalid JSON, return an empty list
        return []


def get_menu_item_by_id(item_id):
    """
    Fetches a single menu item by its ID.
    
    Args:
        item_id (int): The unique ID of the menu item.
    
    Returns:
        dict or None: The menu item dictionary if found, else None.
    """
    menu_items = get_all_menu_items()
    for item in menu_items:
        if item["id"] == item_id:
            return item
    return None
