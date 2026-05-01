"""
bill_routes.py
--------------
Flask route handlers for billing/receipt API endpoints.
Provides the POST /generate-bill endpoint.
"""

from flask import Blueprint, request, jsonify
from backend.services.bill_service import generate_bill_summary

# Create a Blueprint for billing routes
bill_bp = Blueprint("bill", __name__)


@bill_bp.route("/generate-bill", methods=["POST"])
def generate_bill():
    """
    POST /generate-bill
    -------------------
    Generates a structured bill/receipt summary from customer + order data.
    
    Request Body (JSON):
        {
            "customer": { "name": "...", "mobile": "...", "address": "..." },
            "order": {
                "order_number": "QB-1001",
                "items": [...],
                "subtotal": 500,
                "gst": 25,
                "total": 525
            }
        }
    
    Response:
        200: { "status": "success", "data": {bill summary} }
        400: { "status": "error", "message": "..." }
    """
    data = request.get_json()

    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400

    customer = data.get("customer", {})
    order = data.get("order", {})

    if not customer or not order:
        return jsonify({
            "status": "error",
            "message": "Both customer and order data are required"
        }), 400

    # Generate the bill summary via service layer
    bill = generate_bill_summary(customer, order)

    return jsonify({
        "status": "success",
        "message": "Bill generated successfully",
        "data": bill
    }), 200
