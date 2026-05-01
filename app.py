from flask import Flask, render_template, request, jsonify, session
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = "super_secret_key"  # In production, use os.urandom(24)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

MENU_FILE = os.path.join(DATA_DIR, 'menu.json')
ORDERS_FILE = os.path.join(DATA_DIR, 'orders.json')
CUSTOMER_FILE = os.path.join(DATA_DIR, 'customer.json')
ADMIN_FILE = os.path.join(DATA_DIR, 'admin.json')

def load_json(filepath, default=None):
    if default is None:
        default = []
    if not os.path.exists(filepath):
        save_json(filepath, default)
        return default
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

# Initialize files
load_json(MENU_FILE)
load_json(ORDERS_FILE)
load_json(CUSTOMER_FILE)

# Initialize admin
admin_data = load_json(ADMIN_FILE)
if not admin_data or not isinstance(admin_data, list) or len(admin_data) == 0:
    admin_data = [{"username": "admin", "password_hash": generate_password_hash("admin123")}]
    save_json(ADMIN_FILE, admin_data)

# --- Frontend Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin_dashboard():
    if 'admin_logged_in' not in session:
        return render_template('admin_login.html')
    return render_template('admin_dashboard.html')

@app.route('/admin/login', methods=['GET'])
def admin_login_page():
    if 'admin_logged_in' in session:
        return render_template('admin_dashboard.html')
    return render_template('admin_login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/track')
def track_page():
    return render_template('track_order.html')

@app.route('/admin/logout', methods=['GET', 'POST'])
def admin_logout():
    session.pop('admin_logged_in', None)
    return jsonify({"success": True, "message": "Logged out successfully"})


# --- API Routes - Customer ---
@app.route('/api/menu', methods=['GET'])
def get_menu():
    menu = load_json(MENU_FILE)
    return jsonify(menu)

@app.route('/api/customer', methods=['POST'])
def add_customer():
    data = request.json
    customers = load_json(CUSTOMER_FILE)
    customer_id = "cust_" + str(uuid.uuid4())[:8]
    new_customer = {
        "id": customer_id,
        "name": data.get('name'),
        "phone": data.get('phone'),
        "email": data.get('email', ''),
        "address": data.get('address', '')
    }
    customers.append(new_customer)
    save_json(CUSTOMER_FILE, customers)
    return jsonify({"success": True, "customer_id": customer_id})

@app.route('/api/add-order', methods=['POST'])
def add_order():
    data = request.json
    orders = load_json(ORDERS_FILE)
    order_id = "ord_" + str(uuid.uuid4())[:8]
    
    new_order = {
        "order_id": order_id,
        "customer_id": data.get('customer_id'),
        "items": data.get('items'),
        "total_amount": data.get('total_amount'),
        "status": "Completed",
        "timestamp": datetime.now().isoformat()
    }
    orders.append(new_order)
    save_json(ORDERS_FILE, orders)
    return jsonify({"success": True, "order_id": order_id})

@app.route('/api/generate-bill', methods=['POST'])
def generate_bill():
    data = request.json
    order_id = data.get('order_id')
    orders = load_json(ORDERS_FILE)
    customers = load_json(CUSTOMER_FILE)
    
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return jsonify({"success": False, "message": "Order not found"}), 404
        
    customer = next((c for c in customers if c['id'] == order['customer_id']), None)
    
    return jsonify({
        "success": True,
        "order": order,
        "customer": customer
    })

@app.route('/api/track/<order_id>', methods=['GET'])
def api_track_order(order_id):
    orders = load_json(ORDERS_FILE)
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return jsonify({"success": False, "message": "Order not found"}), 404
    return jsonify({"success": True, "status": order.get('status', 'Preparing')})

# --- API Routes - Admin ---
@app.route('/api/admin-login', methods=['POST'])
def api_admin_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    admin_data = load_json(ADMIN_FILE)
    admin = next((a for a in admin_data if a['username'] == username), None)
    
    if admin and check_password_hash(admin['password_hash'], password):
        session['admin_logged_in'] = True
        return jsonify({"success": True, "message": "Login successful"})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route('/api/admin/orders', methods=['GET'])
def get_orders():
    if 'admin_logged_in' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    orders = load_json(ORDERS_FILE)
    customers = load_json(CUSTOMER_FILE)
    customer_map = {c['id']: c for c in customers}
    
    for order in orders:
        if order.get('customer_id') in customer_map:
            order['customer'] = customer_map[order['customer_id']]
            
    orders.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    return jsonify(orders)

@app.route('/api/add-product', methods=['POST'])
def add_product():
    if 'admin_logged_in' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401
        
    data = request.json
    menu = load_json(MENU_FILE)
    
    new_product = {
        "id": "item_" + str(uuid.uuid4())[:8],
        "name": data.get('name'),
        "price": float(data.get('price', 0)),
        "category": data.get('category', 'General'),
        "image_url": data.get('image_url', ''),
        "description": data.get('description', '')
    }
    menu.append(new_product)
    save_json(MENU_FILE, menu)
    return jsonify({"success": True, "product": new_product})

@app.route('/api/remove-product/<product_id>', methods=['DELETE'])
def remove_product(product_id):
    if 'admin_logged_in' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401
        
    menu = load_json(MENU_FILE)
    new_menu = [item for item in menu if item['id'] != product_id]
    
    if len(new_menu) == len(menu):
        return jsonify({"success": False, "message": "Product not found"}), 404
        
    save_json(MENU_FILE, new_menu)
    return jsonify({"success": True, "message": "Product removed"})

@app.route('/api/update-price/<product_id>', methods=['PUT'])
def update_price(product_id):
    if 'admin_logged_in' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401
        
    data = request.json
    new_price = float(data.get('price', 0))
    
    menu = load_json(MENU_FILE)
    for item in menu:
        if item['id'] == product_id:
            item['price'] = new_price
            save_json(MENU_FILE, menu)
            return jsonify({"success": True, "message": "Price updated", "product": item})
            
    return jsonify({"success": False, "message": "Product not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
