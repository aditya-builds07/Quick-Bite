"""
receipt.py - Reusable invoice/receipt display component.
"""
import tkinter as tk
from frontend.config import Colors, Fonts, Spacing, AppConfig


def create_receipt(parent, bill_data):
    """Creates a professional invoice-style receipt widget."""
    frame = tk.Frame(parent, bg="#FFFEF7", padx=Spacing.LG, pady=Spacing.LG,
                     highlightbackground=Colors.BORDER, highlightthickness=1)

    # Header
    tk.Label(frame, text="🍔 QuickBite", font=(Fonts.FAMILY, 20, "bold"),
             fg="#1A1A2E", bg="#FFFEF7").pack(pady=(0, 2))
    tk.Label(frame, text="Taste the Speed!", font=(Fonts.FAMILY, 10),
             fg="#666", bg="#FFFEF7").pack()
    tk.Label(frame, text="━" * 40, fg="#CCC", bg="#FFFEF7",
             font=(Fonts.FAMILY, 8)).pack(pady=6)

    # Bill info
    info = tk.Frame(frame, bg="#FFFEF7")
    info.pack(fill="x")
    tk.Label(info, text=f"Order: {bill_data.get('order_number', 'N/A')}",
             font=Fonts.CAPTION, fg="#333", bg="#FFFEF7").pack(side="left")
    tk.Label(info, text=bill_data.get("bill_date", ""),
             font=Fonts.CAPTION, fg="#333", bg="#FFFEF7").pack(side="right")

    tk.Label(frame, text="┄" * 40, fg="#CCC", bg="#FFFEF7",
             font=(Fonts.FAMILY, 8)).pack(pady=4)

    # Customer
    cust = tk.Frame(frame, bg="#FFFEF7")
    cust.pack(fill="x", pady=4)
    tk.Label(cust, text=f"Customer: {bill_data.get('customer_name', '')}",
             font=Fonts.BODY, fg="#333", bg="#FFFEF7").pack(anchor="w")
    tk.Label(cust, text=f"Mobile: {bill_data.get('customer_mobile', '')}",
             font=Fonts.CAPTION, fg="#666", bg="#FFFEF7").pack(anchor="w")

    tk.Label(frame, text="━" * 40, fg="#CCC", bg="#FFFEF7",
             font=(Fonts.FAMILY, 8)).pack(pady=4)

    # Column headers
    hdr = tk.Frame(frame, bg="#FFFEF7")
    hdr.pack(fill="x")
    tk.Label(hdr, text="Item", font=Fonts.BODY_BOLD, fg="#333",
             bg="#FFFEF7", width=18, anchor="w").pack(side="left")
    tk.Label(hdr, text="Qty", font=Fonts.BODY_BOLD, fg="#333",
             bg="#FFFEF7", width=5).pack(side="left")
    tk.Label(hdr, text="Price", font=Fonts.BODY_BOLD, fg="#333",
             bg="#FFFEF7", width=8).pack(side="left")
    tk.Label(hdr, text="Total", font=Fonts.BODY_BOLD, fg="#333",
             bg="#FFFEF7", width=8, anchor="e").pack(side="right")

    tk.Label(frame, text="┄" * 40, fg="#CCC", bg="#FFFEF7",
             font=(Fonts.FAMILY, 8)).pack(pady=2)

    # Items
    for it in bill_data.get("items", []):
        r = tk.Frame(frame, bg="#FFFEF7")
        r.pack(fill="x", pady=1)
        tk.Label(r, text=it["name"], font=Fonts.BODY, fg="#333",
                 bg="#FFFEF7", width=18, anchor="w").pack(side="left")
        tk.Label(r, text=str(it["quantity"]), font=Fonts.BODY, fg="#333",
                 bg="#FFFEF7", width=5).pack(side="left")
        tk.Label(r, text=f"{AppConfig.CURRENCY}{it['unit_price']}", font=Fonts.BODY,
                 fg="#333", bg="#FFFEF7", width=8).pack(side="left")
        tk.Label(r, text=f"{AppConfig.CURRENCY}{it['item_total']}", font=Fonts.BODY,
                 fg="#333", bg="#FFFEF7", width=8, anchor="e").pack(side="right")

    tk.Label(frame, text="━" * 40, fg="#CCC", bg="#FFFEF7",
             font=(Fonts.FAMILY, 8)).pack(pady=4)

    # Totals
    def total_row(label, value, bold=False, color="#333"):
        r = tk.Frame(frame, bg="#FFFEF7")
        r.pack(fill="x", pady=1)
        f = Fonts.BODY_BOLD if bold else Fonts.BODY
        tk.Label(r, text=label, font=f, fg=color, bg="#FFFEF7").pack(side="left")
        tk.Label(r, text=f"{AppConfig.CURRENCY}{value}", font=f,
                 fg=color, bg="#FFFEF7").pack(side="right")

    total_row("Subtotal", bill_data.get("subtotal", 0))
    total_row(f"GST ({bill_data.get('gst_percent', 5)}%)", bill_data.get("gst_amount", 0))
    tk.Label(frame, text="━" * 40, fg="#333", bg="#FFFEF7",
             font=(Fonts.FAMILY, 8)).pack(pady=2)
    total_row("Grand Total", bill_data.get("grand_total", 0), bold=True, color="#E55A2B")

    tk.Label(frame, text="┄" * 40, fg="#CCC", bg="#FFFEF7",
             font=(Fonts.FAMILY, 8)).pack(pady=6)

    # Footer
    tk.Label(frame, text="Payment: Cash  |  Status: PAID",
             font=Fonts.CAPTION, fg="#48BB78", bg="#FFFEF7").pack()
    tk.Label(frame, text="Thank you for ordering with QuickBite!",
             font=(Fonts.FAMILY, 10, "bold"), fg="#666", bg="#FFFEF7").pack(pady=(6, 0))

    return frame
