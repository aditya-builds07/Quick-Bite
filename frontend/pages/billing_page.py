"""
billing_page.py - Invoice and billing page.
Generates the final bill with customer details, items, GST, and receipt.
"""
import tkinter as tk
from frontend.config import Colors, Fonts, Spacing, AppConfig
from frontend.components.nav_bar import create_nav_bar
from frontend.components.receipt import create_receipt
from frontend import api_client


class BillingPage(tk.Frame):
    """Billing/Invoice page with receipt generation."""

    def __init__(self, parent, customer_data, cart, on_new_order, on_back):
        """
        Args:
            parent: Parent Tkinter container.
            customer_data (dict): Customer info {name, mobile, address, id}.
            cart (dict): Cart items {item_id: item_dict}.
            on_new_order (callable): Start a new order (reset).
            on_back (callable): Go back to cart.
        """
        super().__init__(parent, bg=Colors.BG_MAIN)
        self.customer_data = customer_data
        self.cart = cart
        self.on_new_order = on_new_order
        self.on_back = on_back
        self.bill_data = None
        self.order_data = None
        self._build_ui()

    def _build_ui(self):
        """Constructs the billing page UI."""
        create_nav_bar(self, "Billing & Invoice", on_back=self.on_back)

        # Main scrollable area
        container = tk.Frame(self, bg=Colors.BG_MAIN)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg=Colors.BG_MAIN, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.content = tk.Frame(canvas, bg=Colors.BG_MAIN)
        self.content.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas.bind_all("<MouseWheel>",
            lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        # Header section
        header = tk.Frame(self.content, bg=Colors.BG_MAIN, padx=Spacing.LG)
        header.pack(fill="x", pady=Spacing.MD)
        tk.Label(header, text="📋  Order Summary & Invoice",
                 font=Fonts.HEADING, fg=Colors.TEXT_PRIMARY,
                 bg=Colors.BG_MAIN).pack(side="left")

        self.status_label = tk.Label(header, text="", font=Fonts.BODY,
                                     fg=Colors.SUCCESS, bg=Colors.BG_MAIN)
        self.status_label.pack(side="right")

        # Two-column layout
        cols = tk.Frame(self.content, bg=Colors.BG_MAIN, padx=Spacing.LG)
        cols.pack(fill="both", expand=True)

        # Left column: Customer + Order details
        left = tk.Frame(cols, bg=Colors.BG_MAIN)
        left.pack(side="left", fill="both", expand=True, padx=(0, Spacing.SM))

        # Customer details card
        cust_card = tk.Frame(left, bg=Colors.BG_CARD, padx=Spacing.MD, pady=Spacing.MD,
                             highlightbackground=Colors.BORDER, highlightthickness=1)
        cust_card.pack(fill="x", pady=(0, Spacing.SM))
        tk.Label(cust_card, text="👤  Customer Details", font=Fonts.SUBHEADING,
                 fg=Colors.TEXT_PRIMARY, bg=Colors.BG_CARD).pack(anchor="w", pady=(0, 8))
        tk.Label(cust_card, text=f"Name: {self.customer_data.get('name', 'N/A')}",
                 font=Fonts.BODY, fg=Colors.TEXT_SECONDARY,
                 bg=Colors.BG_CARD).pack(anchor="w")
        tk.Label(cust_card, text=f"Mobile: {self.customer_data.get('mobile', 'N/A')}",
                 font=Fonts.BODY, fg=Colors.TEXT_SECONDARY,
                 bg=Colors.BG_CARD).pack(anchor="w")
        if self.customer_data.get("address"):
            tk.Label(cust_card, text=f"Address: {self.customer_data['address']}",
                     font=Fonts.BODY, fg=Colors.TEXT_SECONDARY,
                     bg=Colors.BG_CARD).pack(anchor="w")

        # Order items card
        items_card = tk.Frame(left, bg=Colors.BG_CARD, padx=Spacing.MD, pady=Spacing.MD,
                              highlightbackground=Colors.BORDER, highlightthickness=1)
        items_card.pack(fill="x", pady=(0, Spacing.SM))
        tk.Label(items_card, text="🍽️  Ordered Items", font=Fonts.SUBHEADING,
                 fg=Colors.TEXT_PRIMARY, bg=Colors.BG_CARD).pack(anchor="w", pady=(0, 8))

        # Table header
        th = tk.Frame(items_card, bg=Colors.BG_SURFACE, padx=8, pady=4)
        th.pack(fill="x", pady=(0, 4))
        tk.Label(th, text="Item", font=Fonts.BODY_BOLD, fg=Colors.TEXT_PRIMARY,
                 bg=Colors.BG_SURFACE, width=16, anchor="w").pack(side="left")
        tk.Label(th, text="Qty", font=Fonts.BODY_BOLD, fg=Colors.TEXT_PRIMARY,
                 bg=Colors.BG_SURFACE, width=5).pack(side="left")
        tk.Label(th, text="Price", font=Fonts.BODY_BOLD, fg=Colors.TEXT_PRIMARY,
                 bg=Colors.BG_SURFACE, width=8).pack(side="left")
        tk.Label(th, text="Total", font=Fonts.BODY_BOLD, fg=Colors.TEXT_PRIMARY,
                 bg=Colors.BG_SURFACE, width=8, anchor="e").pack(side="right")

        subtotal = 0
        for item in self.cart.values():
            itotal = item["price"] * item["quantity"]
            subtotal += itotal
            tr = tk.Frame(items_card, bg=Colors.BG_CARD, padx=8, pady=3)
            tr.pack(fill="x")
            tk.Label(tr, text=f"{item.get('emoji','')} {item['name']}",
                     font=Fonts.BODY, fg=Colors.TEXT_PRIMARY,
                     bg=Colors.BG_CARD, width=16, anchor="w").pack(side="left")
            tk.Label(tr, text=str(item["quantity"]), font=Fonts.BODY,
                     fg=Colors.TEXT_SECONDARY, bg=Colors.BG_CARD, width=5).pack(side="left")
            tk.Label(tr, text=f"{AppConfig.CURRENCY}{item['price']}",
                     font=Fonts.BODY, fg=Colors.TEXT_SECONDARY,
                     bg=Colors.BG_CARD, width=8).pack(side="left")
            tk.Label(tr, text=f"{AppConfig.CURRENCY}{itotal}", font=Fonts.BODY_BOLD,
                     fg=Colors.TEXT_ACCENT, bg=Colors.BG_CARD, width=8,
                     anchor="e").pack(side="right")

        # Totals
        tk.Frame(items_card, bg=Colors.DIVIDER, height=1).pack(fill="x", pady=6)
        gst = round(subtotal * AppConfig.GST_RATE, 2)
        grand = round(subtotal + gst, 2)

        for label, val, bold in [("Subtotal", subtotal, False),
                                  ("GST (5%)", gst, False),
                                  ("Grand Total", grand, True)]:
            tr = tk.Frame(items_card, bg=Colors.BG_CARD, padx=8, pady=2)
            tr.pack(fill="x")
            f = Fonts.PRICE if bold else Fonts.BODY
            c = Colors.TEXT_ACCENT if bold else Colors.TEXT_SECONDARY
            tk.Label(tr, text=label, font=f, fg=c, bg=Colors.BG_CARD).pack(side="left")
            tk.Label(tr, text=f"{AppConfig.CURRENCY}{val}", font=f,
                     fg=c, bg=Colors.BG_CARD).pack(side="right")

        # Right column: Actions + Receipt placeholder
        right = tk.Frame(cols, bg=Colors.BG_MAIN, width=320)
        right.pack(side="right", fill="y", padx=(Spacing.SM, 0))
        right.pack_propagate(False)

        # Action buttons card
        actions = tk.Frame(right, bg=Colors.BG_CARD, padx=Spacing.MD, pady=Spacing.MD,
                           highlightbackground=Colors.BORDER, highlightthickness=1)
        actions.pack(fill="x", pady=(0, Spacing.SM))
        tk.Label(actions, text="⚡  Actions", font=Fonts.SUBHEADING,
                 fg=Colors.TEXT_PRIMARY, bg=Colors.BG_CARD).pack(anchor="w", pady=(0, 12))

        # Generate Bill button
        self.gen_btn = tk.Label(
            actions, text="  📄 Generate Bill  ", font=Fonts.BUTTON,
            fg=Colors.TEXT_PRIMARY, bg=Colors.PRIMARY,
            cursor="hand2", pady=Spacing.SM
        )
        self.gen_btn.pack(fill="x", pady=(0, 8))
        self.gen_btn.bind("<Button-1>", lambda e: self._generate_bill())
        self.gen_btn.bind("<Enter>", lambda e: self.gen_btn.configure(bg=Colors.PRIMARY_DARK))
        self.gen_btn.bind("<Leave>", lambda e: self.gen_btn.configure(bg=Colors.PRIMARY))

        # Print Receipt button (UI only)
        self.print_btn = tk.Label(
            actions, text="  🖨️ Print Receipt  ", font=Fonts.BUTTON,
            fg=Colors.TEXT_PRIMARY, bg=Colors.BG_SURFACE,
            cursor="hand2", pady=Spacing.SM
        )
        self.print_btn.pack(fill="x", pady=(0, 8))
        self.print_btn.bind("<Button-1>", lambda e: self._print_receipt())

        # New Order button
        new_btn = tk.Label(
            actions, text="  🔄 New Order  ", font=Fonts.BUTTON,
            fg=Colors.TEXT_PRIMARY, bg=Colors.SUCCESS,
            cursor="hand2", pady=Spacing.SM
        )
        new_btn.pack(fill="x")
        new_btn.bind("<Button-1>", lambda e: self.on_new_order())

        # Receipt display area
        self.receipt_frame = tk.Frame(right, bg=Colors.BG_MAIN)
        self.receipt_frame.pack(fill="both", expand=True)

    def _generate_bill(self):
        """Generates the bill via API and shows the receipt."""
        items_list = [
            {"id": i["id"], "name": i["name"], "price": i["price"],
             "quantity": i["quantity"]}
            for i in self.cart.values()
        ]

        # Place the order first
        self.order_data = api_client.place_order(
            self.customer_data.get("id", ""),
            self.customer_data.get("name", ""),
            items_list
        )

        if not self.order_data:
            self.status_label.configure(text="⚠ Failed to place order", fg=Colors.ERROR)
            return

        # Generate the bill summary
        self.bill_data = api_client.generate_bill(self.customer_data, self.order_data)

        if self.bill_data:
            self.status_label.configure(text="✓ Bill generated successfully!")
            self.gen_btn.configure(text="  ✓ Bill Generated  ", bg=Colors.SUCCESS)
            # Show receipt
            for w in self.receipt_frame.winfo_children():
                w.destroy()
            create_receipt(self.receipt_frame, self.bill_data).pack(
                fill="x", pady=Spacing.SM)
        else:
            self.status_label.configure(text="⚠ Failed to generate bill", fg=Colors.ERROR)

    def _print_receipt(self):
        """Simulates printing the receipt (UI feedback only)."""
        self.print_btn.configure(text="  ✓ Sent to Printer  ", bg=Colors.SUCCESS)
        self.after(2000, lambda: self.print_btn.configure(
            text="  🖨️ Print Receipt  ", bg=Colors.BG_SURFACE))
