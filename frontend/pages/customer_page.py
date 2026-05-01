"""
customer_page.py - Customer details form page.
Collects name, mobile, and optional address before proceeding to menu.
"""
import tkinter as tk
from frontend.config import Colors, Fonts, Spacing
from frontend.components.nav_bar import create_nav_bar


class CustomerPage(tk.Frame):
    """Customer details input form."""

    def __init__(self, parent, on_proceed, on_back):
        """
        Args:
            parent: Parent Tkinter container.
            on_proceed (callable): Called with (name, mobile, address) dict.
            on_back (callable): Called to go back to home.
        """
        super().__init__(parent, bg=Colors.BG_MAIN)
        self.on_proceed = on_proceed
        self.on_back = on_back
        self._build_ui()

    def _build_ui(self):
        """Constructs the customer form UI."""
        # Navigation bar
        create_nav_bar(self, "Customer Details", on_back=self.on_back)

        # Form card (centered)
        card = tk.Frame(self, bg=Colors.BG_CARD, padx=40, pady=32,
                        highlightbackground=Colors.BORDER, highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Card header
        tk.Label(card, text="👤  Enter Your Details", font=Fonts.HEADING,
                 fg=Colors.TEXT_PRIMARY, bg=Colors.BG_CARD).pack(pady=(0, 6))
        tk.Label(card, text="Please fill in your information to proceed",
                 font=Fonts.CAPTION, fg=Colors.TEXT_SECONDARY,
                 bg=Colors.BG_CARD).pack(pady=(0, 24))

        # Name field
        tk.Label(card, text="FULL NAME *", font=(Fonts.FAMILY, 10, "bold"),
                 fg=Colors.TEXT_SECONDARY, bg=Colors.BG_CARD,
                 anchor="w").pack(fill="x", pady=(0, 4))
        self.name_entry = tk.Entry(
            card, font=Fonts.BODY, bg=Colors.BG_INPUT, fg=Colors.TEXT_PRIMARY,
            insertbackground=Colors.TEXT_PRIMARY, relief="flat",
            highlightbackground=Colors.BORDER, highlightthickness=1, width=35
        )
        self.name_entry.pack(fill="x", ipady=8, pady=(0, 16))
        self.name_entry.insert(0, "")

        # Mobile field
        tk.Label(card, text="MOBILE NUMBER *", font=(Fonts.FAMILY, 10, "bold"),
                 fg=Colors.TEXT_SECONDARY, bg=Colors.BG_CARD,
                 anchor="w").pack(fill="x", pady=(0, 4))
        self.mobile_entry = tk.Entry(
            card, font=Fonts.BODY, bg=Colors.BG_INPUT, fg=Colors.TEXT_PRIMARY,
            insertbackground=Colors.TEXT_PRIMARY, relief="flat",
            highlightbackground=Colors.BORDER, highlightthickness=1, width=35
        )
        self.mobile_entry.pack(fill="x", ipady=8, pady=(0, 16))

        # Address field (optional)
        tk.Label(card, text="ADDRESS (OPTIONAL)", font=(Fonts.FAMILY, 10, "bold"),
                 fg=Colors.TEXT_SECONDARY, bg=Colors.BG_CARD,
                 anchor="w").pack(fill="x", pady=(0, 4))
        self.address_entry = tk.Entry(
            card, font=Fonts.BODY, bg=Colors.BG_INPUT, fg=Colors.TEXT_PRIMARY,
            insertbackground=Colors.TEXT_PRIMARY, relief="flat",
            highlightbackground=Colors.BORDER, highlightthickness=1, width=35
        )
        self.address_entry.pack(fill="x", ipady=8, pady=(0, 8))

        # Error label
        self.error_label = tk.Label(
            card, text="", font=Fonts.CAPTION, fg=Colors.ERROR,
            bg=Colors.BG_CARD
        )
        self.error_label.pack(pady=(4, 8))

        # Proceed button
        btn = tk.Label(
            card, text="  Proceed to Menu  →  ", font=Fonts.BUTTON,
            fg=Colors.TEXT_PRIMARY, bg=Colors.PRIMARY,
            cursor="hand2", padx=Spacing.LG, pady=Spacing.SM
        )
        btn.pack(pady=(8, 0))
        btn.bind("<Button-1>", lambda e: self._validate_and_proceed())
        btn.bind("<Enter>", lambda e: btn.configure(bg=Colors.PRIMARY_DARK))
        btn.bind("<Leave>", lambda e: btn.configure(bg=Colors.PRIMARY))

    def _validate_and_proceed(self):
        """Validates form inputs and calls on_proceed if valid."""
        name = self.name_entry.get().strip()
        mobile = self.mobile_entry.get().strip()
        address = self.address_entry.get().strip()

        if not name:
            self.error_label.configure(text="⚠ Please enter your name")
            return
        if not mobile or len(mobile) < 10 or not mobile.isdigit():
            self.error_label.configure(text="⚠ Please enter a valid 10-digit mobile number")
            return

        self.error_label.configure(text="")
        self.on_proceed({
            "name": name,
            "mobile": mobile,
            "address": address
        })
