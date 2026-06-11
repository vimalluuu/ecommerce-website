import { getCart, removeFromCart, updateQuantity, getCartTotal } from './cart.js';

document.addEventListener('DOMContentLoaded', () => {
    renderCart();
});

function renderCart() {
    const cartItemsContainer = document.querySelector('.cart-items');
    const subtotalEl = document.querySelector('.cart-subtotal');
    const totalEl = document.querySelector('.cart-total');
    if (!cartItemsContainer) return;

    const cart = getCart();
    
    if (cart.items.length === 0) {
        cartItemsContainer.innerHTML = '<p class="py-8 text-center text-gray-400 col-span-2">Your cart is empty. <a href="../public/shop.html" class="text-accent hover:underline">Continue shopping</a>.</p>';
        if (subtotalEl) subtotalEl.textContent = '₹0';
        if (totalEl) totalEl.textContent = '₹0';
        return;
    }

    cartItemsContainer.innerHTML = '';
    cart.items.forEach(item => {
        const img = item.image ? `<img src="${item.image}" style="width: 100%; height: 100%; object-fit: cover;">` : '';
        const itemHtml = `
            <div class="cart-item">
                <div class="cart-item-img">
                    ${img}
                </div>
                <div class="cart-item-details">
                    <div>
                        <div class="cart-item-brand">${item.category || 'Shop'}</div>
                        <h3 class="cart-item-name">${item.name}</h3>
                        <div class="cart-item-variant">Size: ${item.size || 'OS'} | Color: ${item.color || 'Standard'}</div>
                    </div>
                    <div class="cart-item-actions">
                        <div class="qty-controls">
                            <button class="qty-btn" onclick="window.updateItemQuantity('${item.productId}', '${item.size}', '${item.color}', ${item.quantity - 1})">-</button>
                            <input type="text" class="qty-input" value="${item.quantity}" readonly>
                            <button class="qty-btn" onclick="window.updateItemQuantity('${item.productId}', '${item.size}', '${item.color}', ${item.quantity + 1})">+</button>
                        </div>
                        <button class="remove-btn" onclick="window.removeCartItem('${item.productId}', '${item.size}', '${item.color}')">Remove</button>
                    </div>
                </div>
                <div class="cart-item-price">₹${parseFloat(item.price * item.quantity).toLocaleString('en-IN')}</div>
            </div>
        `;
        cartItemsContainer.innerHTML += itemHtml;
    });

    const total = getCartTotal();
    if (subtotalEl) subtotalEl.textContent = `₹${total.toLocaleString('en-IN')}`;
    if (totalEl) totalEl.textContent = `₹${total.toLocaleString('en-IN')}`;
}

window.updateItemQuantity = (id, size, color, qty) => {
    updateQuantity(id, size, color, qty);
    renderCart();
};

window.removeCartItem = (id, size, color) => {
    removeFromCart(id, size, color);
    renderCart();
};
