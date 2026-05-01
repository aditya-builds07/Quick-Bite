"""
menu_page.py - Food menu dashboard page.
Displays food items in a grid layout with cards, quantity selectors, and cart functionality.
"""
import tkinter as tk
from frontend.config import Colors, Fonts, Spacing, AppConfig
from frontend.components.nav_bar import create_nav_bar
from frontend.components.food_card import create_food_card
from frontend import api_client


class MenuPage(tk.Frame):
    """Food menu dashboard with card grid layout."""

    def __init__(self, parent, cart, on_view_cart, on_back):
        """
        Args:
            parent: Parent Tkinter container.
            cart (dict): Shared cart dictionary {item_id: item_dict}.
            on_view_cart (callable): Navigate to cart page.
            on_back (callable): Navigate back to customer page.
        """
        super().__init__(parent, bg=Colors.BG_MAIN)
        self.cart = cart
        self.on_view_cart = on_view_cart
        self.on_back = on_back
        self._build_ui()

    def _build_ui(self):
        """Constructs the menu page UI."""
        # Navigation bar with cart button
        cart_count = sum(item["quantity"] for item in self.cart.values())
        create_nav_bar(self, "Food Menu", cart_count=cart_count,
                       on_back=self.on_back, on_cart=self.on_view_cart)

        # Page header
        header = tk.Frame(self, bg=Colors.BG_MAIN, padx=Spacing.LG, pady=Spacing.MD)
        header.pack(fill="x")
        tk.Label(header, text="🍽️  Choose Your Favorites",
                 font=Fonts.HEADING, fg=Colors.TEXT_PRIMARY,
                 bg=Colors.BG_MAIN).pack(side="left")

        # Status label for feedback
        self.status_label = tk.Label(
            header, text="", font=Fonts.CAPTION,
            fg=Colors.SUCCESS, bg=Colors.BG_MAIN
        )
        self.status_label.pack(side="right")

        # Scrollable area for food cards
        container = tk.Frame(self, bg=Colors.BG_MAIN)
        container.pack(fill="both", expand=True, padx=Spacing.MD)

        canvas = tk.Canvas(container, bg=Colors.BG_MAIN, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, bg=Colors.BG_MAIN)

        self.scroll_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)

        # Fetch menu from API and create cards
        self._load_menu_items()

        # Bottom bar with View Cart button
        bottom = tk.Frame(self, bg=Colors.BG_CARD, pady=Spacing.SM)
        bottom.pack(fill="x", side="bottom")

        self.cart_summary = tk.Label(
            bottom, text=self._get_cart_summary(),
            font=Fonts.BODY, fg=Colors.TEXT_SECONDARY, bg=Colors.BG_CARD
        )
        self.cart_summary.pack(side="left", padx=Spacing.LG)

        view_cart_btn = tk.Label(
            bottom, text="  🛒 View Cart  →  ", font=Fonts.BUTTON,
            fg=Colors.TEXT_PRIMARY, bg=Colors.PRIMARY,
            cursor="hand2", padx=Spacing.LG, pady=Spacing.SM
        )
        view_cart_btn.pack(side="right", padx=Spacing.LG)
        view_cart_btn.bind("<Button-1>", lambda e: self.on_view_cart())
        view_cart_btn.bind("<Enter>", lambda e: view_cart_btn.configure(bg=Colors.PRIMARY_DARK))
        view_cart_btn.bind("<Leave>", lambda e: view_cart_btn.configure(bg=Colors.PRIMARY))

    def _load_menu_items(self):
        """Fetches menu from API and renders food cards in a grid."""
        menu_items = api_client.fetch_menu()

        if not menu_items:
            tk.Label(self.scroll_frame, text="⚠ Could not load menu. Is the server running?",
                     font=Fonts.BODY, fg=Colors.WARNING,
                     bg=Colors.BG_MAIN).pack(pady=40)
            return

        # Create a grid of food cards (3 columns)
        cols = 3
        for idx, item in enumerate(menu_items):
            row = idx // cols
            col = idx % cols
            card = create_food_card(self.scroll_frame, item, self._add_to_cart)
            card.grid(row=row, column=col, padx=Spacing.SM,
                      pady=Spacing.SM, sticky="nsew")

        # Make columns expand evenly
        for c in range(cols):
            self.scroll_frame.columnconfigure(c, weight=1)

    def _add_to_cart(self, item, quantity):
        """Adds an item to the cart or updates its quantity."""
        item_id = item["id"]
        if item_id in self.cart:
            self.cart[item_id]["quantity"] += quantity
        else:
            self.cart[item_id] = {
                "id": item["id"],
                "name": item["name"],
                "emoji": item.get("emoji", "🍽️"),
                "price": item["price"],
                "quantity": quantity
            }
        # Update status and cart summary
        self.status_label.configure(text=f"✓ {item['name']} added to cart!")
        self.cart_summary.configure(text=self._get_cart_summary())
        self.after(2000, lambda: self.status_label.configure(text=""))

    def _get_cart_summary(self):
        """Returns a summary string for the cart."""
        count = sum(item["quantity"] for item in self.cart.values())
        total = sum(item["price"] * item["quantity"] for item in self.cart.values())
        if count == 0:
            return "Cart is empty"
        return f"{count} item(s) • {AppConfig.CURRENCY}{total}"
