import { ProductsAPI } from './api.js';

document.addEventListener('DOMContentLoaded', async () => {
    const featuredGrid = document.getElementById('featured-grid');
    const bestsellersGrid = document.getElementById('bestsellers-grid');

    // Show skeletons
    if (featuredGrid) {
        featuredGrid.innerHTML = Array(4).fill(`
            <div class="product-card skeleton-card">
                <div class="skeleton skeleton-image"></div>
                <div class="product-card-info">
                    <div class="skeleton skeleton-line short"></div>
                    <div class="skeleton skeleton-line wide"></div>
                    <div class="skeleton skeleton-line medium"></div>
                </div>
            </div>
        `).join('');
    }
    if (bestsellersGrid) {
        bestsellersGrid.innerHTML = Array(4).fill(`
            <div class="product-card skeleton-card">
                <div class="skeleton skeleton-image"></div>
                <div class="product-card-info">
                    <div class="skeleton skeleton-line short"></div>
                    <div class="skeleton skeleton-line wide"></div>
                    <div class="skeleton skeleton-line medium"></div>
                </div>
            </div>
        `).join('');
    }

    // Load Featured
    try {
        if (featuredGrid) {
            const res = await ProductsAPI.getFeatured();
            if (res.ok) {
                const data = await res.json();
                const products = data.results || data;
                featuredGrid.innerHTML = '';
                products.slice(0, 4).forEach(p => {
                    featuredGrid.appendChild(createProductCardElement(p));
                });
            } else {
                featuredGrid.innerHTML = '<p class="text-gray-500">Failed to load featured products.</p>';
            }
        }
    } catch (e) {
        console.error("Failed to load featured products", e);
    }

    // Load Bestsellers / All products
    try {
        if (bestsellersGrid) {
            const res = await ProductsAPI.getAll();
            if (res.ok) {
                const data = await res.json();
                const products = data.results || data;
                bestsellersGrid.innerHTML = '';
                // Render up to 6 products
                products.slice(0, 6).forEach(p => {
                    bestsellersGrid.appendChild(createProductCardElement(p));
                });
            } else {
                bestsellersGrid.innerHTML = '<p class="text-gray-500">Failed to load bestseller products.</p>';
            }
        }
    } catch (e) {
        console.error("Failed to load bestseller products", e);
    }

    function createProductCardElement(p) {
        const div = document.createElement('div');
        div.className = 'product-card';
        div.onclick = () => { window.location.href = `product-detail.html?id=${p.id}`; };
        
        const img = p.image_urls && p.image_urls.length > 0 ? p.image_urls[0] : '';
        const imgHtml = img 
            ? `<img src="${img}" alt="${p.name}" style="width: 100%; height: 100%; object-fit: cover;">` 
            : `<div class="product-img-placeholder">ARC</div>`;
            
        div.innerHTML = `
            <div class="product-card-image">
                ${imgHtml}
                ${p.is_featured ? '<div class="product-card-badge">Featured</div>' : ''}
            </div>
            <div class="product-card-info">
                <p class="product-card-category">${p.category ? p.category.name : 'Shop'}</p>
                <h3 class="product-card-name">${p.name}</h3>
                <div class="product-card-footer">
                    <div class="product-price">₹${parseFloat(p.price).toLocaleString('en-IN')}</div>
                </div>
            </div>
        `;
        return div;
    }
});
