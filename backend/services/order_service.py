"""
order_service.py
----------------
Service layer for order-related operations.
Handles creating and retrieving orders from orders.json.
"""

import json
import os
import uuid
from datetime import datetime

# Path to the orders data file
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")


def _read_orders():
    """
    Internal helper: reads all orders from JSON file.
    
    Returns:
        list: List of order dictionaries.
    """
    try:
        with open(ORDERS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _write_orders(orders):
    """
    Internal helper: writes orders list back to JSON file.
    
    Args:
        orders (list): List of order dictionaries to save.
    """
    with open(ORDERS_FILE, "w", encoding="utf-8") as file:
        json.dump(orders, file, indent=4, ensure_ascii=False)


def create_order(customer_id, customer_name, items):
    """
    Creates a new order and saves it to orders.json.
    
    Args:
        customer_id (str): ID of the customer placing the order.
        customer_name (str): Name of the customer.
        items (list): List of ordered items, each with:
                      {id, name, price, quantity}
    
    Returns:
        dict: The complete order record with calculated totals.
    """
    orders = _read_orders()

    # Calculate financial totals
    subtotal = sum(item["price"] * item["quantity"] for item in items)
    gst = round(subtotal * 0.05, 2)        # 5% GST
    total = round(subtotal + gst, 2)

    # Generate a unique order number (e.g., QB-1001)
    order_number = f"QB-{1001 + len(orders)}"

    # Build the order record
    order = {
        "order_id": str(uuid.uuid4())[:8],
        "order_number": order_number,
        "customer_id": customer_id,
        "customer_name": customer_name,
        "items": items,
        "subtotal": subtotal,
        "gst": gst,
        "total": total,
        "status": "Confirmed",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    orders.append(order)
    _write_orders(orders)
    return order


def get_all_orders():
    """
    Returns all saved orders, newest first.
    
    Returns:
        list: List of all order dictionaries.
    """
    orders = _read_orders()
    # Return in reverse chronological order
    return list(reversed(orders))
