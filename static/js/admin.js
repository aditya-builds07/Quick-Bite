document.addEventListener('DOMContentLoaded', () => {
    // Tabs
    const tabLinks = document.querySelectorAll('.sidebar-nav a[data-tab]');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const tabId = link.getAttribute('data-tab');
            
            tabLinks.forEach(l => l.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));
            
            link.classList.add('active');
            document.getElementById(`tab-${tabId}`).classList.add('active');
            
            if (tabId === 'orders') loadOrders();
            if (tabId === 'menu') loadMenu();
        });
    });

    // Logout
    document.getElementById('logout-btn').addEventListener('click', async (e) => {
        e.preventDefault();
        await fetch('/admin/logout');
        window.location.href = '/admin/login';
    });

    // Load Orders
    const ordersTbody = document.getElementById('orders-tbody');
    let allOrders = [];

    async function loadOrders() {
        try {
            const res = await fetch('/api/admin/orders');
            if (res.status === 401) { window.location.href = '/admin/login'; return; }
            allOrders = await res.json();
            renderOrders();
        } catch (error) {
            console.error(error);
        }
    }

    function renderOrders() {
        ordersTbody.innerHTML = '';
        allOrders.forEach(order => {
            const date = new Date(order.timestamp).toLocaleString();
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>#${order.order_id.split('_')[1]}</td>
                <td>${date}</td>
                <td>${order.customer ? order.customer.name : 'Unknown'}</td>
                <td>₹${order.total_amount}</td>
                <td><span class="status-badge ${order.status}">${order.status}</span></td>
                <td><button class="action-btn view-order" data-id="${order.order_id}">View</button></td>
            `;
            ordersTbody.appendChild(tr);
        });

        document.querySelectorAll('.view-order').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = e.target.getAttribute('data-id');
                viewOrder(id);
            });
        });
    }

    // View Order Details
    const viewOrderModal = document.getElementById('view-order-modal');
    const closeViewOrder = document.getElementById('close-view-order');
    const viewOrderDetails = document.getElementById('view-order-details');

    function viewOrder(orderId) {
        const order = allOrders.find(o => o.order_id === orderId);
        if (!order) return;

        let itemsHtml = order.items.map(item => `
            <tr>
                <td>${item.name} x${item.quantity}</td>
                <td style="text-align:right">₹${item.price * item.quantity}</td>
            </tr>
        `).join('');

        viewOrderDetails.innerHTML = `
            <div style="margin-bottom: 20px;">
                <strong>Customer:</strong> ${order.customer ? order.customer.name : 'N/A'}<br>
                <strong>Phone:</strong> ${order.customer ? order.customer.phone : 'N/A'}<br>
                <strong>Address:</strong> ${order.customer ? order.customer.address : 'N/A'}
            </div>
            <table class="data-table" style="margin-bottom: 20px;">
                <thead><tr><th>Item</th><th style="text-align:right">Total</th></tr></thead>
                <tbody>${itemsHtml}</tbody>
            </table>
            <div style="text-align: right; font-size: 1.2rem; font-weight: bold; color: var(--primary);">
                Total: ₹${order.total_amount}
            </div>
        `;
        viewOrderModal.classList.add('show');
    }

    closeViewOrder.addEventListener('click', () => viewOrderModal.classList.remove('show'));

    // Load Menu
    const adminMenuGrid = document.getElementById('admin-menu-grid');
    let menuItems = [];

    async function loadMenu() {
        try {
            const res = await fetch('/api/menu');
            menuItems = await res.json();
            renderAdminMenu();
        } catch (error) {
            console.error(error);
        }
    }

    function renderAdminMenu() {
        adminMenuGrid.innerHTML = '';
        menuItems.forEach(item => {
            const card = document.createElement('div');
            card.className = 'admin-menu-card';
            card.innerHTML = `
                <img src="${item.image_url}" alt="${item.name}">
                <h3>${item.name}</h3>
                <div class="price-input-container">
                    <span style="display:flex; align-items:center;">₹</span>
                    <input type="number" value="${item.price}" id="price-${item.id}">
                    <button class="btn btn-primary update-price" style="padding: 5px 10px;" data-id="${item.id}">Update</button>
                </div>
                <div class="card-actions">
                    <button class="btn remove-product" style="background:#FA5252; color:white; width:100%;" data-id="${item.id}">Remove</button>
                </div>
            `;
            adminMenuGrid.appendChild(card);
        });

        document.querySelectorAll('.update-price').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const id = e.target.getAttribute('data-id');
                const newPrice = document.getElementById(`price-${id}`).value;
                await updatePrice(id, newPrice);
            });
        });

        document.querySelectorAll('.remove-product').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                if (confirm("Are you sure you want to remove this item?")) {
                    const id = e.target.getAttribute('data-id');
                    await removeProduct(id);
                }
            });
        });
    }

    async function updatePrice(id, price) {
        try {
            await fetch(`/api/update-price/${id}`, {
                method: 'PUT',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({price})
            });
            alert("Price updated!");
            loadMenu();
        } catch (error) {
            console.error(error);
        }
    }

    async function removeProduct(id) {
        try {
            await fetch(`/api/remove-product/${id}`, {
                method: 'DELETE'
            });
            loadMenu();
        } catch (error) {
            console.error(error);
        }
    }

    // Add Product
    const addProductModal = document.getElementById('add-product-modal');
    const closeAddProduct = document.getElementById('close-add-product');
    const addProductForm = document.getElementById('add-product-form');

    document.getElementById('add-product-btn').addEventListener('click', () => {
        addProductModal.classList.add('show');
    });

    closeAddProduct.addEventListener('click', () => {
        addProductModal.classList.remove('show');
    });

    addProductForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            name: document.getElementById('p-name').value,
            price: document.getElementById('p-price').value,
            category: document.getElementById('p-category').value,
            image_url: document.getElementById('p-image').value,
            description: document.getElementById('p-desc').value
        };

        try {
            const res = await fetch('/api/add-product', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            if (res.ok) {
                addProductForm.reset();
                addProductModal.classList.remove('show');
                loadMenu();
            }
        } catch (error) {
            console.error(error);
        }
    });

    // Initial Load
    window.loadOrders = loadOrders; // Expose for refresh button
    if (document.getElementById('orders-tbody')) {
        loadOrders();
    }
});
