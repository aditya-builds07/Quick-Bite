"""
config.py
---------
Centralized UI configuration and theme constants for the QuickBite frontend.
All colors, fonts, sizes, and design tokens are defined here.

This file follows the DESIGN_GUIDE.md specifications exactly.
Changing values here will update the entire application's look and feel.
"""


# ══════════════════════════════════════════════════════════════════
# 🎨 COLOR PALETTE
# ══════════════════════════════════════════════════════════════════

class Colors:
    """All color tokens used across the application."""

    # Primary brand colors
    PRIMARY = "#FF6B35"          # Main brand orange
    PRIMARY_DARK = "#E55A2B"     # Hover / active state
    PRIMARY_LIGHT = "#FF8C5A"    # Highlights, badges

    # Background colors (dark theme)
    BG_MAIN = "#1A1A2E"          # Main window background
    BG_CARD = "#16213E"          # Card background
    BG_SURFACE = "#0F3460"       # Elevated surfaces
    BG_INPUT = "#1E2A4A"         # Input field background
    BG_HOVER = "#1F2B50"         # Hover state for cards

    # Text colors
    TEXT_PRIMARY = "#FFFFFF"      # Primary text (white)
    TEXT_SECONDARY = "#A0AEC0"   # Muted / secondary text
    TEXT_ACCENT = "#FF6B35"      # Accent text, prices

    # Status colors
    SUCCESS = "#48BB78"          # Success green
    WARNING = "#F6AD55"          # Warning amber
    ERROR = "#FC8181"            # Error red
    INFO = "#63B3ED"             # Info blue

    # Border colors
    BORDER = "#2D3748"           # Default border
    BORDER_FOCUS = "#FF6B35"     # Focused input border

    # Special
    DIVIDER = "#2D3748"          # Divider lines
    SHADOW = "#0D1117"           # Shadow color


# ══════════════════════════════════════════════════════════════════
# 🔤 TYPOGRAPHY
# ══════════════════════════════════════════════════════════════════

class Fonts:
    """Font configurations for different text elements."""

    # Font family
    FAMILY = "Segoe UI"

    # Font tuples for Tkinter (family, size, weight)
    TITLE = (FAMILY, 28, "bold")         # App title
    HEADING = (FAMILY, 22, "bold")       # Page headings
    SUBHEADING = (FAMILY, 16, "bold")    # Card titles
    BODY = (FAMILY, 13)                  # Regular body text
    BODY_BOLD = (FAMILY, 13, "bold")     # Bold body text
    PRICE = (FAMILY, 18, "bold")         # Price display
    BUTTON = (FAMILY, 13, "bold")        # Button text
    CAPTION = (FAMILY, 11)               # Small captions
    SMALL = (FAMILY, 10)                 # Extra small text
    EMOJI = (FAMILY, 36)                 # Food emoji display
    LOGO_EMOJI = (FAMILY, 52)            # Logo emoji (large)


# ══════════════════════════════════════════════════════════════════
# 📐 SPACING & SIZING
# ══════════════════════════════════════════════════════════════════

class Spacing:
    """Consistent spacing tokens."""

    XS = 4
    SM = 8
    MD = 16
    LG = 24
    XL = 32
    XXL = 48


class Sizing:
    """Standard sizes for UI elements."""

    # Window dimensions
    WINDOW_WIDTH = 1100
    WINDOW_HEIGHT = 720

    # Card dimensions
    CARD_WIDTH = 220
    CARD_PADDING = 16

    # Button dimensions
    BTN_PAD_X = 24
    BTN_PAD_Y = 12

    # Border radius (simulated through styling)
    RADIUS_CARD = 12
    RADIUS_BTN = 8
    RADIUS_INPUT = 8

    # Input field height
    INPUT_HEIGHT = 40


# ══════════════════════════════════════════════════════════════════
# 🏷️ APP CONSTANTS
# ══════════════════════════════════════════════════════════════════

class AppConfig:
    """Application-level constants."""

    APP_NAME = "QuickBite"
    APP_TAGLINE = "Taste the Speed!"
    APP_VERSION = "1.0.0"

    # Backend API base URL
    API_BASE_URL = "http://127.0.0.1:5000"

    # GST rate
    GST_RATE = 0.05  # 5%

    # Currency symbol
    CURRENCY = "₹"
