"""
cart_item.py - Reusable cart item row component.
"""
import tkinter as tk
from frontend.config import Colors, Fonts, Spacing, AppConfig


def create_cart_item(parent, item, on_update_qty, on_remove):
    """Creates a cart item row with quantity controls and remove button."""
    item_id = item["id"]
    qty = item["quantity"]
    price = item["price"]

    row = tk.Frame(parent, bg=Colors.BG_CARD, padx=Spacing.MD, pady=Spacing.SM)
    row.pack(fill="x", pady=2)

    # Left: emoji + name
    left = tk.Frame(row, bg=Colors.BG_CARD)
    left.pack(side="left", fill="y")

    tk.Label(left, text=item.get("emoji", "🍽️"), font=(Fonts.FAMILY, 20),
             bg=Colors.BG_CARD).pack(side="left", padx=(0, 8))

    info = tk.Frame(left, bg=Colors.BG_CARD)
    info.pack(side="left")
    tk.Label(info, text=item.get("name", "Item"), font=Fonts.BODY_BOLD,
             fg=Colors.TEXT_PRIMARY, bg=Colors.BG_CARD).pack(anchor="w")
    tk.Label(info, text=f"{AppConfig.CURRENCY}{price} each", font=Fonts.CAPTION,
             fg=Colors.TEXT_SECONDARY, bg=Colors.BG_CARD).pack(anchor="w")

    # Right: total price + remove
    right = tk.Frame(row, bg=Colors.BG_CARD)
    right.pack(side="right", fill="y")

    total_lbl = tk.Label(right, text=f"{AppConfig.CURRENCY}{price * qty}",
                         font=Fonts.BODY_BOLD, fg=Colors.TEXT_ACCENT, bg=Colors.BG_CARD, padx=8)
    total_lbl.pack(side="right", padx=(8, 0))

    rm = tk.Label(right, text="  ✕  ", font=Fonts.CAPTION, fg=Colors.ERROR,
                  bg=Colors.BG_CARD, cursor="hand2")
    rm.pack(side="right", padx=4)
    rm.bind("<Button-1>", lambda e: on_remove(item_id))

    # Center: qty controls
    center = tk.Frame(row, bg=Colors.BG_CARD)
    center.pack(side="right", padx=Spacing.MD)
    qty_var = tk.IntVar(value=qty)

    def dec():
        v = qty_var.get()
        if v > 1:
            qty_var.set(v - 1)
            ql.configure(text=str(v - 1))
            on_update_qty(item_id, v - 1)
            total_lbl.configure(text=f"{AppConfig.CURRENCY}{price * (v - 1)}")

    def inc():
        v = qty_var.get()
        if v < 20:
            qty_var.set(v + 1)
            ql.configure(text=str(v + 1))
            on_update_qty(item_id, v + 1)
            total_lbl.configure(text=f"{AppConfig.CURRENCY}{price * (v + 1)}")

    m = tk.Label(center, text=" − ", font=Fonts.BODY_BOLD, fg=Colors.TEXT_PRIMARY,
                 bg=Colors.BG_SURFACE, cursor="hand2", padx=6, pady=2)
    m.pack(side="left", padx=2)
    m.bind("<Button-1>", lambda e: dec())

    ql = tk.Label(center, text=str(qty), font=Fonts.BODY_BOLD, fg=Colors.TEXT_PRIMARY,
                  bg=Colors.BG_INPUT, padx=12, pady=2)
    ql.pack(side="left", padx=2)

    p = tk.Label(center, text=" + ", font=Fonts.BODY_BOLD, fg=Colors.TEXT_PRIMARY,
                 bg=Colors.BG_SURFACE, cursor="hand2", padx=6, pady=2)
    p.pack(side="left", padx=2)
    p.bind("<Button-1>", lambda e: inc())

    tk.Frame(parent, bg=Colors.DIVIDER, height=1).pack(fill="x", padx=Spacing.MD)
    return row
