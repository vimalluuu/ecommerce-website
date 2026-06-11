import { OrdersAPI, AuthAPI } from './api.js';
import { requireAuth, getUser } from './auth.js';

document.addEventListener('DOMContentLoaded', async () => {
    requireAuth();

    const user = getUser();
    const userNameEl = document.querySelector('.user-name');
    const userEmailEl = document.querySelector('.user-email');
    if (userNameEl && user) userNameEl.textContent = user.name || user.email;
    if (userEmailEl && user) userEmailEl.textContent = user.email;

    const recentActivityContainer = document.querySelector('.recent-activity');
    if (!recentActivityContainer) return;

    recentActivityContainer.innerHTML = '<p class="text-gray-500">Loading recent activity...</p>';

    try {
        const res = await OrdersAPI.getAll();
        if (res.ok) {
            const data = await res.json();
            const orders = data.results || data;
            
            const totalOrdersEl = document.querySelector('.total-orders-count');
            if (totalOrdersEl) totalOrdersEl.textContent = orders.length;

            if (orders.length === 0) {
                recentActivityContainer.innerHTML = '<p class="text-gray-500">No recent activity found.</p>';
                return;
            }

            recentActivityContainer.innerHTML = '';
            orders.slice(0, 5).forEach(order => {
                const date = new Date(order.created_at).toLocaleDateString();
                const statusColor = order.order_status === 'delivered' ? 'text-white' : 'text-accent';

                recentActivityContainer.innerHTML += `
                    <div class="flex justify-between border-b border-gray-800 pb-4">
                        <div class="text-gray-300">Order <span class="${statusColor}">#${order.order_number}</span> ${order.order_status}</div>
                        <div class="text-gray-500 font-mono text-xs">${date}</div>
                    </div>
                `;
            });
        }
    } catch (e) {
        console.error(e);
        recentActivityContainer.innerHTML = '<p class="text-red-500">Failed to load activity.</p>';
    }
});
