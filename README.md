# Quick-Bite

QuickBite – Online Food Ordering System

# QuickBite – Online Food Ordering System

## Project Overview

QuickBite is a GUI-based Online Food Ordering System built for a college mini project. The application allows customers to browse menu items, add food to a cart, generate bills, and view order summaries.

This project uses a simple architecture with:

- Frontend: Python GUI (Tkinter or generated UI structure)
- Backend: Flask Mock API
- Data Storage: JSON files (No SQL database)

The goal is to create a professional, easy-to-understand, and internship-ready mini project without database complexity.

---

# Technology Stack

## Frontend

- Python
- Tkinter (GUI)
- Optional UI enhancement using Antigravity-generated layout

## Backend

- Flask
- REST-style API structure

## Data Storage

- JSON files
  - menu.json
  - orders.json
  - customer.json

## Tools

- VS Code
- Python 3.10+
- Postman (optional for API testing)
- GitHub (optional)

---

# Project Objectives

- Create a user-friendly restaurant ordering system
- Display menu items with prices
- Allow customers to add/remove items from cart
- Generate automatic billing with GST calculation
- Save order history using JSON
- Build a professional mini project without SQL

---

# Core Features

## 1. Home Page

- Welcome screen
- Restaurant branding
- Start Order button

## 2. Customer Details Page

- Customer name
- Mobile number
- Address (optional)

## 3. Food Menu Page

- Display food items
- Quantity selector
- Add to Cart functionality

## 4. Cart System

- View selected items
- Update quantity
- Remove items
- Subtotal + GST + Final Total

## 5. Billing Page

- Final bill generation
- Customer details
- Ordered items summary
- Printable receipt UI

---

# Folder Structure

```text
quickbite/
│
├── frontend/
│   ├── main.py
│   ├── home.py
│   ├── customer.py
│   ├── menu.py
│   ├── cart.py
│   └── billing.py
│
├── backend/
│   ├── app.py
│   ├── menu_api.py
│   ├── order_api.py
│   └── billing_api.py
│
├── data/
│   ├── menu.json
│   ├── orders.json
│   └── customer.json
│
├── assets/
│   ├── images/
│   └── icons/
│
├── README.md
└── requirements.txt
```

---

# Development Plan

# Phase 1 – Project Setup

## Step 1

Create project folders and files

## Step 2

Install dependencies

```bash
pip install flask
```

## Step 3

Create JSON data files

- menu.json
- orders.json
- customer.json

---

# Phase 2 – Backend Development

## Step 1 – Create Flask App

File: backend/app.py

Responsibilities:

- Start Flask server
- Register API routes
- Handle requests

## Step 2 – Menu API

Endpoints:

- GET /menu

Responsibilities:

- Fetch food items
- Return JSON response

## Step 3 – Order API

Endpoints:

- POST /add-order
- GET /orders

Responsibilities:

- Save orders
- View order history

## Step 4 – Billing API

Endpoints:

- POST /generate-bill

Responsibilities:

- Calculate total
- Add GST
- Return final summary

---

# Phase 3 – Frontend Development

## Step 1 – Home Page UI

Create clean landing page

## Step 2 – Customer Form

Collect customer details

## Step 3 – Food Menu UI

Display menu dynamically

## Step 4 – Cart Page

Cart management logic

## Step 5 – Billing Page

Generate final receipt

---

# Phase 4 – Integration

## Connect Frontend + Backend

Frontend should:

- Fetch menu from API
- Send order details to API
- Receive billing summary

---

# Phase 5 – Testing

## Functional Testing

Check:

- Menu loading
- Cart updates
- Total calculation
- Order saving
- Bill generation

## UI Testing

Check:

- Buttons
- Forms
- Navigation

---

# Future Enhancements

- Payment Gateway
- Delivery Tracking
- Admin Dashboard
- PDF Receipt Generation
- Email Receipt
- Mobile App Version

---

# Viva Preparation

## Why no SQL?

Because this mini project focuses on ordering workflow and GUI interaction. JSON-based mock API makes the project lightweight, faster to build, and easier to explain during viva.

## Why Flask?

Flask is lightweight, simple, and suitable for building backend APIs without unnecessary complexity.

---

# Final Submission Checklist

- Source Code
- Project Report
- PPT
- Flowchart
- ER Diagram
- Viva Questions
- Screenshots
- GitHub Upload (optional)

---

# Project Title

## QuickBite – Online Food Ordering System

A modern GUI-based mini project for restaurant food ordering and billing management.
