"""
food_card.py
------------
Reusable food item card component for the menu page.
Displays food emoji, name, price, quantity selector, and Add to Cart button.
"""

import tkinter as tk
from frontend.config import Colors, Fonts, Spacing, AppConfig


def create_food_card(parent, item, on_add_to_cart):
    """
    Creates a premium-styled food card widget.
    
    Args:
        parent: Parent Tkinter widget (typically a grid frame).
        item (dict): Menu item with keys: id, name, emoji, price, description.
        on_add_to_cart (callable): Callback when "Add to Cart" is clicked.
                                   Receives (item, quantity) as arguments.
    
    Returns:
        tk.Frame: The complete food card frame.
    """
    # Track quantity for this card
    quantity_var = tk.IntVar(value=1)

    # ── Card container ────────────────────────────────────────────
    card = tk.Frame(
        parent,
        bg=Colors.BG_CARD,
        highlightbackground=Colors.BORDER,
        highlightthickness=1,
        padx=Spacing.MD,
        pady=Spacing.MD
    )

    # ── Hover effects ─────────────────────────────────────────────
    def on_enter(e):
        card.configure(highlightbackground=Colors.PRIMARY)
    
    def on_leave(e):
        card.configure(highlightbackground=Colors.BORDER)
    
    card.bind("<Enter>", on_enter)
    card.bind("<Leave>", on_leave)

    # ── Food emoji (large, centered) ──────────────────────────────
    emoji_label = tk.Label(
        card,
        text=item.get("emoji", "🍽️"),
        font=Fonts.EMOJI,
        bg=Colors.BG_CARD
    )
    emoji_label.pack(pady=(8, 4))

    # ── Food name ─────────────────────────────────────────────────
    name_label = tk.Label(
        card,
        text=item.get("name", "Unknown"),
        font=Fonts.SUBHEADING,
        fg=Colors.TEXT_PRIMARY,
        bg=Colors.BG_CARD
    )
    name_label.pack(pady=(4, 2))

    # ── Description ───────────────────────────────────────────────
    desc_label = tk.Label(
        card,
        text=item.get("description", ""),
        font=Fonts.CAPTION,
        fg=Colors.TEXT_SECONDARY,
        bg=Colors.BG_CARD,
        wraplength=180
    )
    desc_label.pack(pady=(0, 8))

    # ── Price ─────────────────────────────────────────────────────
    price_label = tk.Label(
        card,
        text=f"{AppConfig.CURRENCY}{item.get('price', 0)}",
        font=Fonts.PRICE,
        fg=Colors.TEXT_ACCENT,
        bg=Colors.BG_CARD
    )
    price_label.pack(pady=(0, 10))

    # ── Quantity selector row ─────────────────────────────────────
    qty_frame = tk.Frame(card, bg=Colors.BG_CARD)
    qty_frame.pack(pady=(0, 8))

    def decrease_qty():
        current = quantity_var.get()
        if current > 1:
            quantity_var.set(current - 1)
            qty_display.configure(text=str(current - 1))

    def increase_qty():
        current = quantity_var.get()
        if current < 20:
            quantity_var.set(current + 1)
            qty_display.configure(text=str(current + 1))

    # Minus button
    minus_btn = tk.Label(
        qty_frame,
        text="  −  ",
        font=Fonts.BODY_BOLD,
        fg=Colors.TEXT_PRIMARY,
        bg=Colors.BG_SURFACE,
        cursor="hand2",
        padx=4,
        pady=2
    )
    minus_btn.pack(side="left", padx=2)
    minus_btn.bind("<Button-1>", lambda e: decrease_qty())
    minus_btn.bind("<Enter>", lambda e: minus_btn.configure(bg=Colors.PRIMARY_DARK))
    minus_btn.bind("<Leave>", lambda e: minus_btn.configure(bg=Colors.BG_SURFACE))

    # Quantity display
    qty_display = tk.Label(
        qty_frame,
        text="1",
        font=Fonts.BODY_BOLD,
        fg=Colors.TEXT_PRIMARY,
        bg=Colors.BG_INPUT,
        padx=14,
        pady=2
    )
    qty_display.pack(side="left", padx=2)

    # Plus button
    plus_btn = tk.Label(
        qty_frame,
        text="  +  ",
        font=Fonts.BODY_BOLD,
        fg=Colors.TEXT_PRIMARY,
        bg=Colors.BG_SURFACE,
        cursor="hand2",
        padx=4,
        pady=2
    )
    plus_btn.pack(side="left", padx=2)
    plus_btn.bind("<Button-1>", lambda e: increase_qty())
    plus_btn.bind("<Enter>", lambda e: plus_btn.configure(bg=Colors.PRIMARY_DARK))
    plus_btn.bind("<Leave>", lambda e: plus_btn.configure(bg=Colors.BG_SURFACE))

    # ── Add to Cart button ────────────────────────────────────────
    def handle_add():
        on_add_to_cart(item, quantity_var.get())
        # Reset quantity after adding
        quantity_var.set(1)
        qty_display.configure(text="1")
        # Flash success feedback
        add_btn.configure(text="✓ Added!", bg=Colors.SUCCESS)
        card.after(1000, lambda: add_btn.configure(
            text="Add to Cart", bg=Colors.PRIMARY
        ))

    add_btn = tk.Label(
        card,
        text="Add to Cart",
        font=Fonts.BUTTON,
        fg=Colors.TEXT_PRIMARY,
        bg=Colors.PRIMARY,
        cursor="hand2",
        padx=Spacing.LG,
        pady=Spacing.SM
    )
    add_btn.pack(pady=(4, 8), fill="x")
    add_btn.bind("<Button-1>", lambda e: handle_add())
    add_btn.bind("<Enter>", lambda e: add_btn.configure(bg=Colors.PRIMARY_DARK))
    add_btn.bind("<Leave>", lambda e: add_btn.configure(bg=Colors.PRIMARY))

    return card
