"""
menu_routes.py
--------------
Flask route handlers for menu-related API endpoints.
Provides the GET /menu endpoint for fetching all menu items.
"""

from flask import Blueprint, jsonify
from backend.services.menu_service import get_all_menu_items

# Create a Blueprint for menu routes (modular Flask routing)
menu_bp = Blueprint("menu", __name__)


@menu_bp.route("/menu", methods=["GET"])
def fetch_menu():
    """
    GET /menu
    ---------
    Returns the complete restaurant menu as a JSON array.
    
    Response:
        200: { "status": "success", "data": [...menu items...] }
    """
    items = get_all_menu_items()
    return jsonify({
        "status": "success",
        "data": items,
        "count": len(items)
    }), 200
