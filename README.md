# QuickBite – Online Food Ordering & Admin Management System

# PROJECT OVERVIEW

QuickBite is a responsive web-based Online Food Ordering System with an Admin Management Panel.

This project is designed as a professional college mini project that looks like a real restaurant management platform instead of a basic student assignment.

The system includes:

- Customer Side
- Admin Side
- Product Management
- Cart System
- Billing System
- Order Summary
- Secure Admin Login
- Product Price Management
- JSON-based Mock Database

This project avoids SQL complexity and uses a lightweight modern architecture.

---

# TECHNOLOGY STACK

## Frontend

- HTML
- CSS
- JavaScript

UI/UX Design:

- Google Stitch MCP

Design Rules:

- Fully responsive
- Modern layout
- Professional dashboard style
- Premium food ordering UI
- No emojis
- Use icons + SVG only
- Use online food images

---

## Backend

- Python
- Flask

Backend Style:

- REST API structure
- Clean modular architecture

---

## Database

No SQL database used.

Use JSON files as Mock Database:

- menu.json
- orders.json
- customer.json
- admin.json

---

# CORE OBJECTIVES

- Create a professional restaurant ordering platform
- Build a responsive customer ordering system
- Implement cart and billing automation
- Add admin panel for product management
- Secure admin login using encrypted password verification
- Improve viva quality and teacher impression
- Make the project internship-ready

---

# MAIN MODULES

---

# CUSTOMER SIDE

---

## 1. Home Page

### Features

- Welcome section
- Restaurant branding
- Hero section
- Professional navbar
- Start Order button
- Online hero image/banner
- Fully responsive layout

File:

- index.html

---

## 2. Menu Page

### Food Items

Default products:

- Pizza
- Burger
- Sandwich
- Fries
- Pasta
- Cold Drink
- Coffee
- Ice Cream

### Features

Each product card must include:

- Food image from online source
- Product name
- Price
- Quantity selector
- Add to Cart button
- Responsive card layout

File:

- menu.html

---

## 3. Cart Page

### Features

- Selected items
- Quantity update
- Remove item
- Subtotal
- GST calculation
- Final Total
- Proceed to Billing button

File:

- cart.html

---

## 4. Billing Page

### Features

- Customer details form
- Name
- Mobile Number
- Address (optional)
- Final order summary
- Ordered items
- Quantity
- Individual prices
- GST
- Final Total
- Generate Bill button
- Print Receipt button (UI only)
- Professional invoice-style layout

File:

- billing.html

---

# ADMIN SIDE

---

## 5. Admin Login Page

### Features

- Admin ID
- Password
- Secure verification

File:

- admin-login.html

---

## 6. Admin Dashboard

### Features

- Add new product
- Remove product
- Update product price
- Manage product list
- View customer orders
- View billing history
- Product management dashboard

File:

- admin-dashboard.html

---

# ADMIN AUTHENTICATION

## Secure Hardcoded Login

Use:

Admin ID:
admin@quickbite

Password:
Use encrypted password verification

Do NOT store plain password directly.

Use:

- hashlib
  OR
- secure hash verification

This improves project quality and viva answer strength.

---

# REQUIRED FLASK APIs

---

# CUSTOMER APIs

## GET /menu

Fetch menu items from menu.json

---

## POST /add-order

Save customer order to orders.json

---

## POST /customer

Save customer details to customer.json

---

## POST /generate-bill

Calculate:

- subtotal
- GST
- final total

Return final bill summary

---

## GET /orders

Fetch saved orders

---

# ADMIN APIs

## POST /admin-login

Verify admin login

---

## POST /add-product

Add new product to menu

---

## DELETE /remove-product

Delete product from menu

---

## PUT /update-price

Update product price

---

## GET /admin/orders

View all customer orders

---

# FOLDER STRUCTURE

```text
quickbite/
│
├── frontend/
│   │
│   ├── index.html
│   ├── menu.html
│   ├── cart.html
│   ├── billing.html
│   │
│   ├── admin-login.html
│   ├── admin-dashboard.html
│   │
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   ├── app.js
│   │   └── admin.js
│   │
│   └── assets/
│       ├── icons/
│       └── images/
│
├── backend/
│   ├── app.py
│   ├── routes.py
│   ├── admin_routes.py
│   ├── auth.py
│   └── utils.py
│
├── data/
│   ├── menu.json
│   ├── orders.json
│   ├── customer.json
│   └── admin.json
│
├── requirements.txt
└── README.md
```
