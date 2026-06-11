import { ProductsAPI } from './api.js';

document.addEventListener('DOMContentLoaded', async () => {
    const grids = document.querySelectorAll('.products-grid');
    if (grids.length === 0) return;

    grids.forEach(grid => {
        grid.innerHTML = Array(4).fill(`
            <div class="product-card skeleton-card">
                <div class="skeleton skeleton-image"></div>
                <div class="product-card-info">
                    <div class="skeleton skeleton-line short"></div>
                    <div class="skeleton skeleton-line wide"></div>
                    <div class="skeleton skeleton-line medium"></div>
                </div>
            </div>
        `).join('');
    });

    try {
        const res = await ProductsAPI.getAll();
        if (res.ok) {
            const data = await res.json();
            const products = data.results || data;
            
            grids.forEach((grid, i) => {
                grid.innerHTML = '';
                // Take 4 products for each grid (maybe different slices if needed, just take first 4 for demo)
                const items = products.slice(0, 4);
                
                items.forEach(p => {
                    const imgHtml = p.image_urls && p.image_urls.length > 0
                        ? `<img src="${p.image_urls[0]}" alt="${p.name}">` 
                        : `<div class="product-img-placeholder">ARC</div>`;
                    
                    const card = `
                        <a href="product-detail.html?id=${p.id}" class="product-card">
                            <div class="product-card-image">
                                ${imgHtml}
                                ${p.is_featured ? '<div class="product-card-badge">Featured</div>' : ''}
                            </div>
                            <div class="product-card-info">
                                <p class="product-card-category">${p.category ? p.category.name : 'Shop'}</p>
                                <h3 class="product-card-name">${p.name}</h3>
                                <div class="product-card-footer">
                                    <div class="product-price">₹${p.price}</div>
                                </div>
                            </div>
                        </a>
                    `;
                    grid.innerHTML += card;
                });
            });
        }
    } catch (e) {
        console.error("Failed to load home products", e);
    }
});
