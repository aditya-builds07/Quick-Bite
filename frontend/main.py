"""
main.py - Tkinter application entry point for QuickBite.
Manages page navigation and shared application state (cart, customer data).
This is the controller that wires all pages together.
"""
import tkinter as tk
from frontend.config import Colors, Sizing, AppConfig
from frontend.pages.home_page import HomePage
from frontend.pages.customer_page import CustomerPage
from frontend.pages.menu_page import MenuPage
from frontend.pages.cart_page import CartPage
from frontend.pages.billing_page import BillingPage
from frontend import api_client


class QuickBiteApp:
    """
    Main application class.
    Handles window setup, page navigation, and shared state management.
    """

    def __init__(self):
        """Initializes the Tkinter root window and application state."""
        self.root = tk.Tk()
        self.root.title(f"{AppConfig.APP_NAME} – {AppConfig.APP_TAGLINE}")
        self.root.geometry(f"{Sizing.WINDOW_WIDTH}x{Sizing.WINDOW_HEIGHT}")
        self.root.configure(bg=Colors.BG_MAIN)
        self.root.minsize(900, 600)

        # Try to set the window icon (won't crash if unavailable)
        try:
            self.root.iconbitmap("assets/logo.ico")
        except Exception:
            pass

        # ── Shared Application State ──────────────────────────────
        self.cart = {}            # {item_id: {id, name, emoji, price, quantity}}
        self.customer_data = {}   # {id, name, mobile, address}

        # ── Page container (fills entire window) ──────────────────
        self.container = tk.Frame(self.root, bg=Colors.BG_MAIN)
        self.container.pack(fill="both", expand=True)

        # ── Start on the Home page ────────────────────────────────
        self._show_home()

    def _clear_container(self):
        """Removes all widgets from the main container."""
        for widget in self.container.winfo_children():
            widget.destroy()

    # ══════════════════════════════════════════════════════════════
    # PAGE NAVIGATION METHODS
    # ══════════════════════════════════════════════════════════════

    def _show_home(self):
        """Navigates to the Home / Welcome page."""
        self._clear_container()
        page = HomePage(self.container, on_start_order=self._show_customer)
        page.pack(fill="both", expand=True)

    def _show_customer(self):
        """Navigates to the Customer Details page."""
        self._clear_container()
        page = CustomerPage(
            self.container,
            on_proceed=self._on_customer_proceed,
            on_back=self._show_home
        )
        page.pack(fill="both", expand=True)

    def _on_customer_proceed(self, customer_info):
        """
        Called when customer form is submitted.
        Saves customer to backend and navigates to menu.
        """
        # Save customer via API
        saved = api_client.save_customer(
            customer_info["name"],
            customer_info["mobile"],
            customer_info.get("address", "")
        )
        if saved:
            self.customer_data = saved
        else:
            # Even if API fails, store locally so the flow continues
            self.customer_data = customer_info

        self._show_menu()

    def _show_menu(self):
        """Navigates to the Food Menu page."""
        self._clear_container()
        page = MenuPage(
            self.container,
            cart=self.cart,
            on_view_cart=self._show_cart,
            on_back=self._show_customer
        )
        page.pack(fill="both", expand=True)

    def _show_cart(self):
        """Navigates to the Cart page."""
        self._clear_container()
        page = CartPage(
            self.container,
            cart=self.cart,
            on_proceed_billing=self._show_billing,
            on_back=self._show_menu
        )
        page.pack(fill="both", expand=True)

    def _show_billing(self):
        """Navigates to the Billing / Invoice page."""
        self._clear_container()
        page = BillingPage(
            self.container,
            customer_data=self.customer_data,
            cart=self.cart,
            on_new_order=self._start_new_order,
            on_back=self._show_cart
        )
        page.pack(fill="both", expand=True)

    def _start_new_order(self):
        """Resets all state and goes back to home for a new order."""
        self.cart.clear()
        self.customer_data.clear()
        self._show_home()

    # ══════════════════════════════════════════════════════════════
    # RUN
    # ══════════════════════════════════════════════════════════════

    def run(self):
        """Starts the Tkinter main event loop."""
        self.root.mainloop()
