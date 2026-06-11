import { WishlistAPI } from './api.js';
import { requireAuth } from './auth.js';

document.addEventListener('DOMContentLoaded', async () => {
    requireAuth();

    const wishlistContainer = document.querySelector('.wishlist-items');
    if (!wishlistContainer) return;

    wishlistContainer.innerHTML = '<p class="text-gray-500 col-span-4 text-center py-8">Loading wishlist...</p>';

    try {
        const res = await WishlistAPI.getAll();
        if (res.ok) {
            const data = await res.json();
            const items = data.results || data;

            if (items.length === 0) {
                wishlistContainer.innerHTML = '<p class="text-gray-500 col-span-4 text-center py-8">Your wishlist is empty.</p>';
                return;
            }

            wishlistContainer.innerHTML = '';
            items.forEach(item => {
                const p = item.product;
                const imgHtml = p.image_urls && p.image_urls.length > 0
                    ? `<img src="${p.image_urls[0]}" alt="${p.name}">` 
                    : `<div class="product-img-placeholder">ARC</div>`;
                
                wishlistContainer.innerHTML += `
                    <div class="product-card bg-gray-900 border border-gray-800 transition-colors hover:border-gray-600">
                        <div class="product-card-image">
                            ${imgHtml}
                            <button onclick="window.removeWishlist(${item.id})" class="absolute top-2 right-2 w-8 h-8 bg-black/50 text-white flex items-center justify-center hover:bg-red-500 transition-colors">×</button>
                        </div>
                        <div class="p-4">
                            <h3 class="font-heading text-lg mb-1">${p.name}</h3>
                            <div class="font-mono text-accent">₹${p.price}</div>
                            <button onclick="window.location.href='../public/product-detail.html?id=${p.id}'" class="mt-4 w-full border border-gray-700 py-2 text-xs font-mono uppercase tracking-widest hover:border-accent hover:text-accent transition-colors">View Product</button>
                        </div>
                    </div>
                `;
            });
        }
    } catch (e) {
        console.error(e);
        wishlistContainer.innerHTML = '<p class="text-red-500 col-span-4 text-center py-8">Failed to load wishlist.</p>';
    }
});

window.removeWishlist = async (id) => {
    try {
        await WishlistAPI.remove(id);
        window.location.reload();
    } catch (e) {
        console.error(e);
        alert('Failed to remove from wishlist');
    }
};
