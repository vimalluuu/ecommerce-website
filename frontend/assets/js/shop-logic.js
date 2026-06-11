import { ProductsAPI } from './api.js';

document.addEventListener('DOMContentLoaded', async () => {
    const grid = document.getElementById('product-grid');
    if (!grid) return;

    // Show skeletons
    grid.innerHTML = Array(6).fill(`
        <div class="product-card skeleton-card">
            <div class="skeleton skeleton-image"></div>
            <div class="product-card-info">
                <div class="skeleton skeleton-line short"></div>
                <div class="skeleton skeleton-line wide"></div>
                <div class="skeleton skeleton-line medium"></div>
            </div>
        </div>
    `).join('');

    try {
        const res = await ProductsAPI.getAll();
        if (res.ok) {
            const data = await res.json();
            const products = data.results || data;
            
            // Update count
            const countEl = document.querySelector('.product-count');
            if (countEl) countEl.textContent = `Showing ${products.length} pieces`;

            grid.innerHTML = '';
            
            products.forEach(p => {
                const img = p.image_urls && p.image_urls.length > 0 ? p.image_urls[0] : '';
                const imgHtml = img 
                    ? `<img src="${img}" alt="${p.name}">` 
                    : `<div class="product-img-placeholder">ARC</div>`;
                
                const card = `
                    <a href="product-detail.html?id=${p.id}" class="product-card">
                        <div class="product-card-image">
                            ${imgHtml}
                            ${p.is_featured ? '<div class="product-card-badge">Featured</div>' : ''}
                        </div>
                        <div class="product-card-info">
                            <p class="font-mono text-xs text-gray-500 mb-1 tracking-widest uppercase">${p.category ? p.category.name : 'Shop'}</p>
                            <h3 class="product-card-name">${p.name}</h3>
                            <div class="product-price">₹${p.price}</div>
                        </div>
                    </a>
                `;
                grid.innerHTML += card;
            });
        }
    } catch (e) {
        console.error("Failed to load products", e);
        grid.innerHTML = '<p class="text-red-500">Failed to load products.</p>';
    }
});
