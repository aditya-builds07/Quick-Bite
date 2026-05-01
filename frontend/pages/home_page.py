"""
home_page.py - Welcome/landing screen for QuickBite.
Features: Brand logo, tagline, animated Start Order button.
"""
import tkinter as tk
from frontend.config import Colors, Fonts, Spacing


class HomePage(tk.Frame):
    """
    Home / Welcome screen.
    Displays the QuickBite brand with a prominent 'Start Order' CTA.
    """

    def __init__(self, parent, on_start_order):
        """
        Args:
            parent: Parent Tkinter container.
            on_start_order (callable): Callback when 'Start Order' is clicked.
        """
        super().__init__(parent, bg=Colors.BG_MAIN)
        self.on_start_order = on_start_order
        self._build_ui()

    def _build_ui(self):
        """Constructs the home page UI elements."""
        # Center container
        center = tk.Frame(self, bg=Colors.BG_MAIN)
        center.place(relx=0.5, rely=0.45, anchor="center")

        # Decorative top line
        tk.Label(center, text="━━━━━━━━━━━━━━━━━━━━━━━━",
                 font=(Fonts.FAMILY, 10), fg=Colors.BORDER,
                 bg=Colors.BG_MAIN).pack(pady=(0, 20))

        # Logo emoji
        tk.Label(center, text="🍔", font=(Fonts.FAMILY, 72),
                 bg=Colors.BG_MAIN).pack(pady=(0, 10))

        # App name
        tk.Label(center, text="QuickBite", font=(Fonts.FAMILY, 42, "bold"),
                 fg=Colors.PRIMARY, bg=Colors.BG_MAIN).pack(pady=(0, 5))

        # Tagline
        tk.Label(center, text="Taste the Speed!", font=(Fonts.FAMILY, 16),
                 fg=Colors.TEXT_SECONDARY, bg=Colors.BG_MAIN).pack(pady=(0, 8))

        # Subtitle
        tk.Label(center, text="Premium Food Ordering Experience",
                 font=Fonts.CAPTION, fg=Colors.TEXT_SECONDARY,
                 bg=Colors.BG_MAIN).pack(pady=(0, 30))

        # Decorative line
        tk.Label(center, text="━━━━━━━━━━━━━━━━━━━━━━━━",
                 font=(Fonts.FAMILY, 10), fg=Colors.BORDER,
                 bg=Colors.BG_MAIN).pack(pady=(0, 30))

        # Start Order button
        btn = tk.Label(
            center, text="  🚀  Start Order  ", font=(Fonts.FAMILY, 16, "bold"),
            fg=Colors.TEXT_PRIMARY, bg=Colors.PRIMARY,
            cursor="hand2", padx=40, pady=14
        )
        btn.pack(pady=(0, 20))
        btn.bind("<Button-1>", lambda e: self.on_start_order())
        btn.bind("<Enter>", lambda e: btn.configure(bg=Colors.PRIMARY_DARK))
        btn.bind("<Leave>", lambda e: btn.configure(bg=Colors.PRIMARY))

        # Version info
        tk.Label(center, text="v1.0.0  •  Restaurant Management System",
                 font=Fonts.SMALL, fg=Colors.DIVIDER,
                 bg=Colors.BG_MAIN).pack(pady=(10, 0))

        # Bottom decoration
        bottom = tk.Frame(self, bg=Colors.BG_MAIN)
        bottom.place(relx=0.5, rely=0.92, anchor="center")
        tk.Label(bottom, text="🍕  🍔  🥪  🍟  🍝  🥤  ☕  🍨",
                 font=(Fonts.FAMILY, 18), bg=Colors.BG_MAIN).pack()
