"""
nav_bar.py
----------
Reusable navigation bar component for QuickBite.
Displays the app logo, current page title, and a cart badge.
Used at the top of every page (except the home screen).
"""

import tkinter as tk
from frontend.config import Colors, Fonts, Spacing


def create_nav_bar(parent, title_text, cart_count=0, on_back=None, on_cart=None):
    """
    Creates and returns a styled navigation bar frame.
    
    Args:
        parent: Parent Tkinter widget.
        title_text (str): The current page title to display.
        cart_count (int): Number of items in cart (shown as badge).
        on_back (callable): Callback for back/home button click.
        on_cart (callable): Callback for cart button click.
    
    Returns:
        tk.Frame: The complete navigation bar frame.
    """
    # ── Main nav container ────────────────────────────────────────
    nav_frame = tk.Frame(
        parent,
        bg=Colors.BG_CARD,
        height=60,
        padx=Spacing.LG,
        pady=Spacing.SM
    )
    nav_frame.pack(fill="x", side="top")
    nav_frame.pack_propagate(False)

    # ── Left side: Back button + Logo ─────────────────────────────
    left_section = tk.Frame(nav_frame, bg=Colors.BG_CARD)
    left_section.pack(side="left", fill="y")

    if on_back:
        back_btn = tk.Label(
            left_section,
            text="◀",
            font=Fonts.BODY_BOLD,
            fg=Colors.TEXT_SECONDARY,
            bg=Colors.BG_CARD,
            cursor="hand2",
            padx=8
        )
        back_btn.pack(side="left", padx=(0, 8))
        back_btn.bind("<Button-1>", lambda e: on_back())
        back_btn.bind("<Enter>", lambda e: back_btn.configure(fg=Colors.PRIMARY))
        back_btn.bind("<Leave>", lambda e: back_btn.configure(fg=Colors.TEXT_SECONDARY))

    # Brand logo
    logo_label = tk.Label(
        left_section,
        text="🍔 QuickBite",
        font=(Fonts.FAMILY, 16, "bold"),
        fg=Colors.PRIMARY,
        bg=Colors.BG_CARD
    )
    logo_label.pack(side="left")

    # ── Center: Page title ────────────────────────────────────────
    title_label = tk.Label(
        nav_frame,
        text=title_text,
        font=(Fonts.FAMILY, 14, "bold"),
        fg=Colors.TEXT_PRIMARY,
        bg=Colors.BG_CARD
    )
    title_label.pack(side="left", expand=True)

    # ── Right side: Cart badge ────────────────────────────────────
    if on_cart:
        cart_frame = tk.Frame(nav_frame, bg=Colors.BG_CARD)
        cart_frame.pack(side="right")

        cart_btn = tk.Label(
            cart_frame,
            text=f"🛒 Cart",
            font=Fonts.BODY_BOLD,
            fg=Colors.TEXT_PRIMARY,
            bg=Colors.BG_SURFACE,
            padx=12,
            pady=6,
            cursor="hand2"
        )
        cart_btn.pack(side="left")
        cart_btn.bind("<Button-1>", lambda e: on_cart())
        cart_btn.bind("<Enter>", lambda e: cart_btn.configure(bg=Colors.PRIMARY))
        cart_btn.bind("<Leave>", lambda e: cart_btn.configure(bg=Colors.BG_SURFACE))

        if cart_count > 0:
            badge = tk.Label(
                cart_frame,
                text=str(cart_count),
                font=(Fonts.FAMILY, 10, "bold"),
                fg=Colors.TEXT_PRIMARY,
                bg=Colors.PRIMARY,
                padx=6,
                pady=2
            )
            badge.pack(side="left", padx=(4, 0))

    return nav_frame
