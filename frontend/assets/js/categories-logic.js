import { ProductsAPI } from './api.js';

document.addEventListener('DOMContentLoaded', async () => {
    const grid = document.querySelector('.grid-3');
    if (!grid) return;

    grid.innerHTML = Array(3).fill(`
        <div class="collection-card skeleton">
            <h3 class="skeleton skeleton-line medium"></h3>
            <p class="skeleton skeleton-line short"></p>
        </div>
    `).join('');

    try {
        const res = await ProductsAPI.getCategories();
        if (res.ok) {
            const data = await res.json();
            const categories = data.results || data;
            
            grid.innerHTML = '';
            
            categories.forEach(cat => {
                const card = `
                    <div class="collection-card" onclick="window.location.href='shop.html?category=${cat.slug}'">
                        <h3>${cat.name}</h3>
                        <p>${cat.description || 'Explore collection'}</p>
                        <button class="btn">Browse Collection</button>
                    </div>
                `;
                grid.innerHTML += card;
            });
        }
    } catch (e) {
        console.error("Failed to load categories", e);
        grid.innerHTML = '<p class="text-red-500">Failed to load categories.</p>';
    }
});
