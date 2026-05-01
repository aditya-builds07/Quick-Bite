"""
app.py
------
Flask application entry point.
Initializes the Flask server and registers all route Blueprints.

This file is the heart of the backend – it creates the Flask app,
registers all API route modules, and provides a function to start the server.
"""

from flask import Flask
from backend.routes.menu_routes import menu_bp
from backend.routes.customer_routes import customer_bp
from backend.routes.order_routes import order_bp
from backend.routes.bill_routes import bill_bp


def create_app():
    """
    Factory function to create and configure the Flask application.
    
    This follows the Application Factory pattern – a Flask best practice
    that makes the app easier to test and configure.
    
    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)

    # ── Register Blueprints ───────────────────────────────────────
    # Each Blueprint handles a group of related API endpoints.
    # This keeps our code modular and organized.
    app.register_blueprint(menu_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(bill_bp)

    # ── Root Health-Check Endpoint ────────────────────────────────
    @app.route("/", methods=["GET"])
    def health_check():
        """
        GET /
        Simple health-check endpoint to verify the server is running.
        """
        return {
            "status": "running",
            "app": "QuickBite API",
            "version": "1.0.0"
        }, 200

    return app


def start_server():
    """
    Starts the Flask development server on port 5000.
    Called from run.py in a background thread.
    """
    app = create_app()
    # use_reloader=False is important when running in a thread
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)


# Allow running this file directly for testing the backend
if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)
