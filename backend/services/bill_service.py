"""
bill_service.py
---------------
Service layer for billing and receipt generation.
Combines customer and order data to create a formatted bill summary.
"""

from datetime import datetime


def generate_bill_summary(customer, order):
    """
    Generates a structured bill summary combining customer info and order details.
    
    This is used by the frontend to display a professional invoice-style receipt.
    
    Args:
        customer (dict): Customer record with name, mobile, address.
        order (dict): Order record with items, subtotal, gst, total.
    
    Returns:
        dict: A complete bill summary with all fields needed for the receipt.
    """
    bill = {
        "restaurant_name": "QuickBite",
        "restaurant_tagline": "Taste the Speed!",
        "bill_date": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "order_number": order.get("order_number", "N/A"),

        # Customer details
        "customer_name": customer.get("name", "N/A"),
        "customer_mobile": customer.get("mobile", "N/A"),
        "customer_address": customer.get("address", ""),

        # Order items (list of dicts: name, qty, price, item_total)
        "items": [
            {
                "name": item["name"],
                "quantity": item["quantity"],
                "unit_price": item["price"],
                "item_total": item["price"] * item["quantity"]
            }
            for item in order.get("items", [])
        ],

        # Financial summary
        "subtotal": order.get("subtotal", 0),
        "gst_percent": 5,
        "gst_amount": order.get("gst", 0),
        "grand_total": order.get("total", 0),

        # Status
        "status": "PAID",
        "payment_method": "Cash"
    }

    return bill
