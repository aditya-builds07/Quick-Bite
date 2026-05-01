document.addEventListener('DOMContentLoaded', () => {
    // State
    let menu = [];
    let cart = [];

    // DOM Elements
    const menuGrid = document.getElementById('menu-grid');
    const cartBtn = document.getElementById('cart-btn');
    const closeCartBtn = document.getElementById('close-cart');
    const cartSidebar = document.getElementById('cart-sidebar');
    const cartOverlay = document.getElementById('cart-overlay');
    const cartItemsContainer = document.getElementById('cart-items');
    const cartCount = document.getElementById('cart-count');
    const cartTotalPrice = document.getElementById('cart-total-price');
    const checkoutBtn = document.getElementById('checkout-btn');
    
    const checkoutModal = document.getElementById('checkout-modal');
    const closeCheckoutBtn = document.getElementById('close-checkout');
    const checkoutForm = document.getElementById('checkout-form');
    
    const invoiceModal = document.getElementById('invoice-modal');
    const closeInvoiceBtn = document.getElementById('close-invoice');
    const invoiceDetails = document.getElementById('invoice-details');

    if (!menuGrid) return; // Only run menu-related JS on pages with menu grid

    // Fetch Menu
    fetch('/api/menu')
        .then(res => res.json())
        .then(data => {
            menu = data;
            renderMenu();
        });

    // Render Menu
    function renderMenu() {
        menuGrid.innerHTML = '';
        menu.forEach(item => {
            const card = document.createElement('div');
            card.className = 'menu-card';
            card.innerHTML = `
                <img src="${item.image_url}" alt="${item.name}" class="menu-img">
                <div class="menu-content">
                    <div class="menu-header">
                        <div class="menu-title">${item.name}</div>
                        <div class="menu-price">₹${item.price}</div>
                    </div>
                    <p class="menu-desc">${item.description}</p>
                    <button class="btn btn-primary btn-full add-to-cart-btn" data-id="${item.id}">Add to Cart</button>
                </div>
            `;
            menuGrid.appendChild(card);
        });

        // Add event listeners to buttons
        document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = e.target.getAttribute('data-id');
                addToCart(id);
            });
        });
    }

    // Cart Functions
    function addToCart(id) {
        const item = menu.find(m => m.id === id);
        const existing = cart.find(c => c.item_id === id);
        if (existing) {
            existing.quantity += 1;
        } else {
            cart.push({
                item_id: item.id,
                name: item.name,
                price: item.price,
                quantity: 1
            });
        }
        updateCart();
        openCart();
    }

    function updateCart() {
        cartItemsContainer.innerHTML = '';
        let total = 0;
        let count = 0;

        if (cart.length === 0) {
            cartItemsContainer.innerHTML = '<div class="empty-cart-msg">Your cart is empty.</div>';
            checkoutBtn.disabled = true;
        } else {
            checkoutBtn.disabled = false;
            cart.forEach(item => {
                total += item.price * item.quantity;
                count += item.quantity;

                const cartItem = document.createElement('div');
                cartItem.className = 'cart-item';
                cartItem.innerHTML = `
                    <div class="cart-item-info">
                        <h4>${item.name}</h4>
                        <p>₹${item.price}</p>
                    </div>
                    <div class="cart-item-actions">
                        <button class="qty-btn minus" data-id="${item.item_id}">-</button>
                        <span>${item.quantity}</span>
                        <button class="qty-btn plus" data-id="${item.item_id}">+</button>
                    </div>
                `;
                cartItemsContainer.appendChild(cartItem);
            });
        }

        cartCount.textContent = count;
        cartTotalPrice.textContent = `₹${total}`;

        // Event listeners for quantity changes
        document.querySelectorAll('.qty-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = e.target.getAttribute('data-id');
                const isPlus = e.target.classList.contains('plus');
                changeQuantity(id, isPlus ? 1 : -1);
            });
        });
    }

    function changeQuantity(id, change) {
        const itemIndex = cart.findIndex(c => c.item_id === id);
        if (itemIndex > -1) {
            cart[itemIndex].quantity += change;
            if (cart[itemIndex].quantity <= 0) {
                cart.splice(itemIndex, 1);
            }
            updateCart();
        }
    }

    // Cart Sidebar Toggles
    function openCart() {
        cartSidebar.classList.add('open');
        cartOverlay.classList.add('show');
    }

    function closeCart() {
        cartSidebar.classList.remove('open');
        cartOverlay.classList.remove('show');
    }

    cartBtn.addEventListener('click', openCart);
    closeCartBtn.addEventListener('click', closeCart);
    cartOverlay.addEventListener('click', closeCart);

    // Checkout Modal
    checkoutBtn.addEventListener('click', () => {
        closeCart();
        checkoutModal.classList.add('show');
    });

    closeCheckoutBtn.addEventListener('click', () => {
        checkoutModal.classList.remove('show');
    });

    // Handle Form Submit
    checkoutForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const customerData = {
            name: document.getElementById('cust-name').value,
            phone: document.getElementById('cust-phone').value,
            email: document.getElementById('cust-email').value,
            address: document.getElementById('cust-address').value
        };

        try {
            // 1. Create Customer
            const custRes = await fetch('/api/customer', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(customerData)
            });
            const custResult = await custRes.json();
            
            if (custResult.success) {
                // 2. Create Order
                const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
                const orderData = {
                    customer_id: custResult.customer_id,
                    items: cart,
                    total_amount: total
                };

                const orderRes = await fetch('/api/add-order', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(orderData)
                });
                const orderResult = await orderRes.json();

                if (orderResult.success) {
                    // 3. Generate Bill
                    const billRes = await fetch('/api/generate-bill', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ order_id: orderResult.order_id })
                    });
                    const billResult = await billRes.json();
                    
                    if (billResult.success) {
                        showInvoice(billResult);
                        cart = []; // Clear cart
                        updateCart();
                        checkoutForm.reset();
                        checkoutModal.classList.remove('show');
                    }
                }
            }
        } catch (error) {
            console.error("Error processing order:", error);
            alert("Something went wrong. Please try again.");
        }
    });

    // Invoice Modal
    function showInvoice(data) {
        const { order, customer } = data;
        const date = new Date(order.timestamp).toLocaleString();
        
        let itemsHtml = order.items.map(item => `
            <tr>
                <td>${item.name} x${item.quantity}</td>
                <td class="amount">₹${item.price * item.quantity}</td>
            </tr>
        `).join('');

        invoiceDetails.innerHTML = `
            <div class="invoice-meta">
                <div>
                    <strong>Order ID:</strong> ${order.order_id}<br>
                    <strong>Date:</strong> ${date}
                </div>
                <div style="text-align: right;">
                    <strong>Customer:</strong><br>
                    ${customer.name}<br>
                    ${customer.phone}
                </div>
            </div>
            
            <table class="invoice-table">
                <thead>
                    <tr>
                        <th>Item</th>
                        <th class="amount">Total</th>
                    </tr>
                </thead>
                <tbody>
                    ${itemsHtml}
                </tbody>
            </table>
            
            <div class="invoice-summary">
                <div class="invoice-row">
                    <span>Subtotal</span>
                    <span>₹${order.total_amount}</span>
                </div>
                <div class="invoice-row">
                    <span>Taxes (0%)</span>
                    <span>₹0</span>
                </div>
                <div class="invoice-row total">
                    <span>Total Paid</span>
                    <span>₹${order.total_amount}</span>
                </div>
            </div>
            
            <div style="text-align: center; margin-bottom: 20px;">
                <p><strong>Delivery Address:</strong><br>${customer.address}</p>
            </div>
        `;
        
        invoiceModal.classList.add('show');
    }

    closeInvoiceBtn.addEventListener('click', () => {
        invoiceModal.classList.remove('show');
    });
});
