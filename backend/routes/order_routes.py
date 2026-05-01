"""
order_routes.py
---------------
Flask route handlers for order-related API endpoints.
Provides POST /add-order and GET /orders endpoints.
"""

from flask import Blueprint, request, jsonify
from backend.services.order_service import create_order, get_all_orders

# Create a Blueprint for order routes
order_bp = Blueprint("order", __name__)


@order_bp.route("/add-order", methods=["POST"])
def add_order():
    """
    POST /add-order
    ---------------
    Creates a new food order with calculated totals and saves to orders.json.
    
    Request Body (JSON):
        {
            "customer_id": "abc12345",
            "customer_name": "John Doe",
            "items": [
                {"id": 1, "name": "Pizza", "price": 249, "quantity": 2},
                {"id": 6, "name": "Cold Drink", "price": 59, "quantity": 1}
            ]
        }
    
    Response:
        201: { "status": "success", "data": {order record with totals} }
        400: { "status": "error", "message": "..." }
    """
    data = request.get_json()

    # Validate request data
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400

    customer_id = data.get("customer_id", "")
    customer_name = data.get("customer_name", "")
    items = data.get("items", [])

    if not customer_name:
        return jsonify({"status": "error", "message": "Customer name is required"}), 400
    if not items or len(items) == 0:
        return jsonify({"status": "error", "message": "At least one item is required"}), 400

    # Create the order via the service layer
    order = create_order(customer_id, customer_name, items)

    return jsonify({
        "status": "success",
        "message": "Order placed successfully",
        "data": order
    }), 201


@order_bp.route("/orders", methods=["GET"])
def fetch_orders():
    """
    GET /orders
    -----------
    Returns all saved orders in reverse chronological order.
    
    Response:
        200: { "status": "success", "data": [...orders...] }
    """
    orders = get_all_orders()
    return jsonify({
        "status": "success",
        "data": orders,
        "count": len(orders)
    }), 200
