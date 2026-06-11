import { getCart, removeFromCart, updateQuantity, getCartTotal } from './cart.js';

document.addEventListener('DOMContentLoaded', () => {
    renderCart();
});

function renderCart() {
    const cartItemsContainer = document.querySelector('.cart-items');
    const orderTotalEl = document.querySelector('.order-total');
    if (!cartItemsContainer || !orderTotalEl) return;

    const cart = getCart();
    
    if (cart.items.length === 0) {
        cartItemsContainer.innerHTML = '<p>Your cart is empty. <a href="../public/shop.html" class="text-accent hover:underline">Continue shopping</a>.</p>';
        orderTotalEl.textContent = '₹0.00';
        return;
    }

    cartItemsContainer.innerHTML = '';
    cart.items.forEach(item => {
        const itemHtml = `
            <div class="cart-item border-b border-gray-800 pb-6 mb-6 flex gap-6">
                <div class="cart-item-image w-24 h-32 bg-gray-900 flex-shrink-0">
                    ${item.image ? `<img src="${item.image}" class="w-full h-full object-cover">` : ''}
                </div>
                <div class="cart-item-details flex-grow">
                    <div class="flex justify-between mb-2">
                        <h3 class="font-heading text-lg">${item.name}</h3>
                        <div class="text-accent font-mono">₹${item.price}</div>
                    </div>
                    <div class="text-sm text-gray-500 mb-4">
                        Size: ${item.size || 'OS'} <br>
                        Color: ${item.color || 'Standard'}
                    </div>
                    <div class="flex justify-between items-center">
                        <div class="quantity-selector flex items-center border border-gray-700">
                            <button class="px-3 py-1 hover:text-accent" onclick="window.updateItemQuantity('${item.productId}', '${item.size}', '${item.color}', ${item.quantity - 1})">-</button>
                            <span class="px-3 font-mono text-sm">${item.quantity}</span>
                            <button class="px-3 py-1 hover:text-accent" onclick="window.updateItemQuantity('${item.productId}', '${item.size}', '${item.color}', ${item.quantity + 1})">+</button>
                        </div>
                        <button class="text-xs text-gray-500 uppercase tracking-widest hover:text-red-500 transition-colors" onclick="window.removeCartItem('${item.productId}', '${item.size}', '${item.color}')">Remove</button>
                    </div>
                </div>
            </div>
        `;
        cartItemsContainer.innerHTML += itemHtml;
    });

    const total = getCartTotal();
    orderTotalEl.textContent = `₹${total.toFixed(2)}`;
}

window.updateItemQuantity = (id, size, color, qty) => {
    updateQuantity(id, size, color, qty);
    renderCart();
};

window.removeCartItem = (id, size, color) => {
    removeFromCart(id, size, color);
    renderCart();
};
