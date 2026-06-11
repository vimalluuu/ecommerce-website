import { OrdersAPI } from './api.js';
import { getCart, getCartTotal, clearCart } from './cart.js';
import { requireAuth } from './auth.js';

document.addEventListener('DOMContentLoaded', () => {
    // Ensure user is logged in to checkout
    requireAuth();

    const checkoutForm = document.getElementById('checkoutForm');
    const orderItemsContainer = document.querySelector('.order-items');
    const subtotalEl = document.querySelector('.subtotal-amount');
    const totalEl = document.querySelector('.total-amount');
    
    if (!checkoutForm || !orderItemsContainer) return;

    const cart = getCart();
    if (cart.items.length === 0) {
        alert("Your cart is empty.");
        window.location.href = "cart.html";
        return;
    }

    // Render items in order summary
    orderItemsContainer.innerHTML = '';
    cart.items.forEach(item => {
        orderItemsContainer.innerHTML += `
            <div class="flex justify-between text-sm mb-4">
                <div class="text-gray-400">
                    <span class="text-white">${item.quantity}x</span> ${item.name} (${item.size})
                </div>
                <div class="font-mono text-accent">₹${item.price * item.quantity}</div>
            </div>
        `;
    });

    const subtotal = getCartTotal();
    const shipping = 15.00; // Flat shipping
    subtotalEl.textContent = `₹${subtotal.toFixed(2)}`;
    totalEl.textContent = `₹${(subtotal + shipping).toFixed(2)}`;

    checkoutForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const btn = checkoutForm.querySelector('.btn-primary');
        const originalText = btn.textContent;
        btn.textContent = 'Processing...';
        btn.disabled = true;

        const formData = new FormData(checkoutForm);
        const orderData = {
            total_amount: subtotal + shipping,
            shipping_cost: shipping,
            shipping_address: {
                name: formData.get('firstName') + ' ' + formData.get('lastName'),
                address: formData.get('address'),
                city: formData.get('city'),
                postal: formData.get('postal'),
            },
            items: cart.items.map(i => ({
                product: i.productId,
                quantity: i.quantity,
                price: i.price,
                size: i.size,
                color: i.color
            }))
        };

        try {
            const res = await OrdersAPI.create(orderData);
            if (res.ok) {
                clearCart();
                alert('Order placed successfully!');
                window.location.href = 'dashboard.html';
            } else {
                const err = await res.json();
                console.error(err);
                alert('Failed to place order. Please try again.');
                btn.textContent = originalText;
                btn.disabled = false;
            }
        } catch (error) {
            console.error(error);
            alert('An error occurred. Please try again.');
            btn.textContent = originalText;
            btn.disabled = false;
        }
    });
});
