"""
api_client.py
-------------
HTTP client module for communicating with the Flask backend API.
All frontend-to-backend communication goes through this module.

This acts as a clean abstraction layer – the frontend pages never
make HTTP calls directly. They call functions from this module instead.
"""

import requests
from frontend.config import AppConfig

# Base URL for all API calls
BASE_URL = AppConfig.API_BASE_URL


def fetch_menu():
    """
    Fetches the complete food menu from the backend.
    
    Calls: GET /menu
    
    Returns:
        list: List of menu item dictionaries, or empty list on error.
    """
    try:
        response = requests.get(f"{BASE_URL}/menu", timeout=5)
        if response.status_code == 200:
            return response.json().get("data", [])
    except requests.ConnectionError:
        print("[API] Error: Could not connect to backend server.")
    except Exception as e:
        print(f"[API] Error fetching menu: {e}")
    return []


def save_customer(name, mobile, address=""):
    """
    Sends customer details to the backend for storage.
    
    Calls: POST /customer
    
    Args:
        name (str): Customer name.
        mobile (str): Customer mobile number.
        address (str): Customer address (optional).
    
    Returns:
        dict or None: Saved customer record, or None on error.
    """
    try:
        payload = {
            "name": name,
            "mobile": mobile,
            "address": address
        }
        response = requests.post(f"{BASE_URL}/customer", json=payload, timeout=5)
        if response.status_code == 201:
            return response.json().get("data")
    except requests.ConnectionError:
        print("[API] Error: Could not connect to backend server.")
    except Exception as e:
        print(f"[API] Error saving customer: {e}")
    return None


def place_order(customer_id, customer_name, items):
    """
    Sends a new order to the backend.
    
    Calls: POST /add-order
    
    Args:
        customer_id (str): Customer's unique ID.
        customer_name (str): Customer's name.
        items (list): List of ordered items with id, name, price, quantity.
    
    Returns:
        dict or None: Created order record with totals, or None on error.
    """
    try:
        payload = {
            "customer_id": customer_id,
            "customer_name": customer_name,
            "items": items
        }
        response = requests.post(f"{BASE_URL}/add-order", json=payload, timeout=5)
        if response.status_code == 201:
            return response.json().get("data")
    except requests.ConnectionError:
        print("[API] Error: Could not connect to backend server.")
    except Exception as e:
        print(f"[API] Error placing order: {e}")
    return None


def generate_bill(customer, order):
    """
    Requests a bill/receipt summary from the backend.
    
    Calls: POST /generate-bill
    
    Args:
        customer (dict): Customer details.
        order (dict): Order details with items and totals.
    
    Returns:
        dict or None: Bill summary for receipt display, or None on error.
    """
    try:
        payload = {
            "customer": customer,
            "order": order
        }
        response = requests.post(f"{BASE_URL}/generate-bill", json=payload, timeout=5)
        if response.status_code == 200:
            return response.json().get("data")
    except requests.ConnectionError:
        print("[API] Error: Could not connect to backend server.")
    except Exception as e:
        print(f"[API] Error generating bill: {e}")
    return None


def fetch_orders():
    """
    Fetches all order history from the backend.
    
    Calls: GET /orders
    
    Returns:
        list: List of order dictionaries, or empty list on error.
    """
    try:
        response = requests.get(f"{BASE_URL}/orders", timeout=5)
        if response.status_code == 200:
            return response.json().get("data", [])
    except requests.ConnectionError:
        print("[API] Error: Could not connect to backend server.")
    except Exception as e:
        print(f"[API] Error fetching orders: {e}")
    return []
