"""
run.py
------
Single entry point to start both the Flask backend and Tkinter frontend.

How it works:
1. Starts the Flask API server in a background daemon thread.
2. Waits briefly for the server to initialize.
3. Launches the Tkinter GUI on the main thread.

Usage:
    python run.py
"""

import threading
import time
import sys
import os

# Add the project root to Python path so imports work correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    """Main entry point – starts backend and frontend."""

    print("=" * 50)
    print("🍔 QuickBite – Online Food Ordering System")
    print("=" * 50)

    # ── Step 1: Start Flask backend in a background thread ────────
    print("\n[1/2] Starting Flask backend server...")
    from backend.app import start_server

    # Daemon thread will automatically stop when the main program exits
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Give the server a moment to boot up
    time.sleep(1.5)
    print("  ✓ Backend running at http://127.0.0.1:5000")

    # ── Step 2: Start Tkinter frontend on the main thread ─────────
    print("[2/2] Launching QuickBite GUI...")
    print("  ✓ Application ready!\n")

    from frontend.main import QuickBiteApp
    app = QuickBiteApp()
    app.run()

    print("\n👋 QuickBite closed. Goodbye!")


if __name__ == "__main__":
    main()
