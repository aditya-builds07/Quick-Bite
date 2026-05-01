"""
customer_routes.py
------------------
Flask route handlers for customer-related API endpoints.
Provides the POST /customer endpoint for saving customer details.
"""

from flask import Blueprint, request, jsonify
from backend.services.customer_service import save_customer

# Create a Blueprint for customer routes
customer_bp = Blueprint("customer", __name__)


@customer_bp.route("/customer", methods=["POST"])
def add_customer():
    """
    POST /customer
    --------------
    Saves customer details (name, mobile, address) to customers.json.
    
    Request Body (JSON):
        {
            "name": "John Doe",
            "mobile": "9876543210",
            "address": "123 Main St"  (optional)
        }
    
    Response:
        201: { "status": "success", "data": {customer record} }
        400: { "status": "error", "message": "..." }
    """
    data = request.get_json()

    # Validate required fields
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400

    name = data.get("name", "").strip()
    mobile = data.get("mobile", "").strip()
    address = data.get("address", "").strip()

    # Name and mobile are required
    if not name:
        return jsonify({"status": "error", "message": "Customer name is required"}), 400
    if not mobile or len(mobile) < 10:
        return jsonify({"status": "error", "message": "Valid mobile number is required"}), 400

    # Save the customer via the service layer
    customer = save_customer(name, mobile, address)

    return jsonify({
        "status": "success",
        "message": "Customer saved successfully",
        "data": customer
    }), 201
