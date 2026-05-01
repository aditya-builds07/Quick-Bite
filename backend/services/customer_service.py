"""
customer_service.py
-------------------
Service layer for customer-related operations.
Handles saving and retrieving customer data from customers.json.
"""

import json
import os
import uuid
from datetime import datetime

# Path to the customers data file
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CUSTOMERS_FILE = os.path.join(DATA_DIR, "customers.json")


def _read_customers():
    """
    Internal helper: reads all customers from JSON file.
    
    Returns:
        list: List of customer dictionaries.
    """
    try:
        with open(CUSTOMERS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _write_customers(customers):
    """
    Internal helper: writes customer list back to JSON file.
    
    Args:
        customers (list): List of customer dictionaries to save.
    """
    with open(CUSTOMERS_FILE, "w", encoding="utf-8") as file:
        json.dump(customers, file, indent=4, ensure_ascii=False)


def save_customer(name, mobile, address=""):
    """
    Saves a new customer record to customers.json.
    
    Args:
        name (str): Customer's full name.
        mobile (str): Customer's mobile number.
        address (str): Customer's delivery address (optional).
    
    Returns:
        dict: The saved customer record with generated ID and timestamp.
    """
    customers = _read_customers()

    # Create a new customer record with a unique ID
    customer = {
        "id": str(uuid.uuid4())[:8],  # Short unique ID
        "name": name.strip(),
        "mobile": mobile.strip(),
        "address": address.strip(),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    customers.append(customer)
    _write_customers(customers)
    return customer


def get_all_customers():
    """
    Returns all saved customer records.
    
    Returns:
        list: List of all customer dictionaries.
    """
    return _read_customers()
