"""
cart_page.py - Shopping cart page.
Shows selected items with quantity controls, subtotal, GST, and grand total.
"""
import tkinter as tk
from frontend.config import Colors, Fonts, Spacing, AppConfig
from frontend.components.nav_bar import create_nav_bar
from frontend.components.cart_item import create_cart_item


class CartPage(tk.Frame):
    """Shopping cart with item management and price summary."""

    def __init__(self, parent, cart, on_proceed_billing, on_back):
        """
        Args:
            parent: Parent Tkinter container.
            cart (dict): Shared cart dictionary {item_id: item_dict}.
            on_proceed_billing (callable): Navigate to billing page.
            on_back (callable): Navigate back to menu.
        """
        super().__init__(parent, bg=Colors.BG_MAIN)
        self.cart = cart
        self.on_proceed_billing = on_proceed_billing
        self.on_back = on_back
        self._build_ui()

    def _build_ui(self):
        """Constructs the cart page UI."""
        create_nav_bar(self, "Your Cart", on_back=self.on_back)

        if not self.cart:
            self._show_empty_cart()
            return

        # Main content area
        content = tk.Frame(self, bg=Colors.BG_MAIN)
        content.pack(fill="both", expand=True, padx=Spacing.LG, pady=Spacing.MD)

        # Left: Cart items list
        left = tk.Frame(content, bg=Colors.BG_MAIN)
        left.pack(side="left", fill="both", expand=True, padx=(0, Spacing.MD))

        tk.Label(left, text=f"🛒  Cart Items ({len(self.cart)})",
                 font=Fonts.SUBHEADING, fg=Colors.TEXT_PRIMARY,
                 bg=Colors.BG_MAIN).pack(anchor="w", pady=(0, Spacing.SM))

        items_frame = tk.Frame(left, bg=Colors.BG_CARD,
                               highlightbackground=Colors.BORDER, highlightthickness=1)
        items_frame.pack(fill="both", expand=True)

        # Scrollable items container
        canvas = tk.Canvas(items_frame, bg=Colors.BG_CARD, highlightthickness=0)
        self.items_inner = tk.Frame(canvas, bg=Colors.BG_CARD)
        self.items_inner.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.items_inner, anchor="nw")
        canvas.pack(fill="both", expand=True)

        for item in self.cart.values():
            create_cart_item(self.items_inner, item,
                           self._update_quantity, self._remove_item)

        # Right: Price summary card
        right = tk.Frame(content, bg=Colors.BG_CARD, padx=Spacing.LG, pady=Spacing.LG,
                         highlightbackground=Colors.BORDER, highlightthickness=1, width=300)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        tk.Label(right, text="📋  Order Summary", font=Fonts.SUBHEADING,
                 fg=Colors.TEXT_PRIMARY, bg=Colors.BG_CARD).pack(anchor="w", pady=(0, 16))

        tk.Frame(right, bg=Colors.DIVIDER, height=1).pack(fill="x", pady=8)

        # Calculate totals
        subtotal = sum(i["price"] * i["quantity"] for i in self.cart.values())
        gst = round(subtotal * AppConfig.GST_RATE, 2)
        grand_total = round(subtotal + gst, 2)

        # Subtotal row
        row1 = tk.Frame(right, bg=Colors.BG_CARD)
        row1.pack(fill="x", pady=4)
        tk.Label(row1, text="Subtotal", font=Fonts.BODY,
                 fg=Colors.TEXT_SECONDARY, bg=Colors.BG_CARD).pack(side="left")
        tk.Label(row1, text=f"{AppConfig.CURRENCY}{subtotal}",
                 font=Fonts.BODY, fg=Colors.TEXT_PRIMARY,
                 bg=Colors.BG_CARD).pack(side="right")

        # GST row
        row2 = tk.Frame(right, bg=Colors.BG_CARD)
        row2.pack(fill="x", pady=4)
        tk.Label(row2, text="GST (5%)", font=Fonts.BODY,
                 fg=Colors.TEXT_SECONDARY, bg=Colors.BG_CARD).pack(side="left")
        tk.Label(row2, text=f"{AppConfig.CURRENCY}{gst}",
                 font=Fonts.BODY, fg=Colors.TEXT_PRIMARY,
                 bg=Colors.BG_CARD).pack(side="right")

        tk.Frame(right, bg=Colors.DIVIDER, height=1).pack(fill="x", pady=8)

        # Grand total
        row3 = tk.Frame(right, bg=Colors.BG_CARD)
        row3.pack(fill="x", pady=4)
        tk.Label(row3, text="Grand Total", font=Fonts.PRICE,
                 fg=Colors.TEXT_PRIMARY, bg=Colors.BG_CARD).pack(side="left")
        tk.Label(row3, text=f"{AppConfig.CURRENCY}{grand_total}",
                 font=Fonts.PRICE, fg=Colors.TEXT_ACCENT,
                 bg=Colors.BG_CARD).pack(side="right")

        # Items count
        total_items = sum(i["quantity"] for i in self.cart.values())
        tk.Label(right, text=f"{total_items} item(s) total",
                 font=Fonts.CAPTION, fg=Colors.TEXT_SECONDARY,
                 bg=Colors.BG_CARD).pack(pady=(8, 16))

        # Proceed to Billing button
        bill_btn = tk.Label(
            right, text="  Proceed to Billing  →  ", font=Fonts.BUTTON,
            fg=Colors.TEXT_PRIMARY, bg=Colors.PRIMARY,
            cursor="hand2", pady=Spacing.SM
        )
        bill_btn.pack(fill="x", pady=(8, 0))
        bill_btn.bind("<Button-1>", lambda e: self.on_proceed_billing())
        bill_btn.bind("<Enter>", lambda e: bill_btn.configure(bg=Colors.PRIMARY_DARK))
        bill_btn.bind("<Leave>", lambda e: bill_btn.configure(bg=Colors.PRIMARY))

    def _show_empty_cart(self):
        """Shows empty cart message."""
        center = tk.Frame(self, bg=Colors.BG_MAIN)
        center.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(center, text="🛒", font=(Fonts.FAMILY, 52),
                 bg=Colors.BG_MAIN).pack(pady=(0, 10))
        tk.Label(center, text="Your cart is empty",
                 font=Fonts.HEADING, fg=Colors.TEXT_SECONDARY,
                 bg=Colors.BG_MAIN).pack(pady=(0, 8))
        tk.Label(center, text="Go back to the menu to add items",
                 font=Fonts.BODY, fg=Colors.TEXT_SECONDARY,
                 bg=Colors.BG_MAIN).pack(pady=(0, 20))

        back_btn = tk.Label(center, text="  ← Back to Menu  ",
                            font=Fonts.BUTTON, fg=Colors.TEXT_PRIMARY,
                            bg=Colors.PRIMARY, cursor="hand2",
                            padx=Spacing.LG, pady=Spacing.SM)
        back_btn.pack()
        back_btn.bind("<Button-1>", lambda e: self.on_back())

    def _update_quantity(self, item_id, new_qty):
        """Updates item quantity in the cart."""
        if item_id in self.cart:
            self.cart[item_id]["quantity"] = new_qty

    def _remove_item(self, item_id):
        """Removes an item from the cart and refreshes the page."""
        if item_id in self.cart:
            del self.cart[item_id]
        # Rebuild the page
        for widget in self.winfo_children():
            widget.destroy()
        self._build_ui()
