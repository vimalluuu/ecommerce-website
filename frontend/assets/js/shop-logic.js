import { ProductsAPI } from './api.js';

document.addEventListener('DOMContentLoaded', async () => {
    const grid = document.getElementById('product-grid');
    const categoryFiltersContainer = document.getElementById('category-filters');
    const sortSelect = document.querySelector('.sort-select');
    
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

    let allProducts = [];

    // Parse URL params for initial category filter
    const urlParams = new URLSearchParams(window.location.search);
    const initialCategorySlug = urlParams.get('category');

    // Load categories first
    try {
        const catRes = await ProductsAPI.getCategories();
        if (catRes.ok && categoryFiltersContainer) {
            const categories = await catRes.json();
            const catList = categories.results || categories;
            
            categoryFiltersContainer.innerHTML = '';
            catList.forEach(cat => {
                const isChecked = initialCategorySlug === cat.slug ? 'checked' : '';
                const li = document.createElement('li');
                li.innerHTML = `
                    <label>
                        <input type="checkbox" name="category" value="${cat.slug}" ${isChecked}>
                        ${cat.name}
                    </label>
                `;
                categoryFiltersContainer.appendChild(li);
            });
        }
    } catch (e) {
        console.error("Failed to load categories dynamically, keeping defaults or showing error", e);
    }

    // Load products
    try {
        const res = await ProductsAPI.getAll();
        if (res.ok) {
            const data = await res.json();
            allProducts = data.results || data;
            
            // Set up filter change listeners
            setupFilterListeners();
            
            // Initial render
            applyFiltersAndRender();
        } else {
            grid.innerHTML = '<p class="text-red-500">Failed to load products.</p>';
        }
    } catch (e) {
        console.error("Failed to load products", e);
        grid.innerHTML = '<p class="text-red-500">Failed to load products.</p>';
    }

    function setupFilterListeners() {
        // Listen to dynamically generated category checkboxes
        if (categoryFiltersContainer) {
            categoryFiltersContainer.addEventListener('change', applyFiltersAndRender);
        }
        
        // Listen to static color checkboxes
        document.querySelectorAll('.filter-section input[type="checkbox"]').forEach(checkbox => {
            if (checkbox.name !== 'category') {
                checkbox.addEventListener('change', applyFiltersAndRender);
            }
        });
        
        // Listen to sort select
        if (sortSelect) {
            sortSelect.addEventListener('change', applyFiltersAndRender);
        }
    }

    function applyFiltersAndRender() {
        // 1. Gather checked filters
        const checkedCategories = Array.from(document.querySelectorAll('#category-filters input[type="checkbox"]:checked'))
            .map(cb => cb.value.toLowerCase());
        
        // Find color checkboxes
        const checkedColors = Array.from(document.querySelectorAll('.filter-section:nth-of-type(2) input[type="checkbox"]:checked'))
            .map(cb => cb.value.toLowerCase());
            
        // Find size checkboxes
        const checkedSizes = Array.from(document.querySelectorAll('.filter-section:nth-of-type(3) input[type="checkbox"]:checked'))
            .map(cb => cb.value.toLowerCase());

        // 2. Filter products
        let filtered = allProducts.filter(p => {
            // Category filter
            if (checkedCategories.length > 0) {
                const catSlug = p.category && p.category.slug ? p.category.slug.toLowerCase() : '';
                if (!checkedCategories.includes(catSlug)) return false;
            }
            
            // Color filter
            if (checkedColors.length > 0) {
                const pColors = p.colors ? p.colors.map(c => c.toLowerCase()) : [];
                // Check if any checked color is available in product
                // Match patterns like "black" mapping to "Obsidian Black"
                const hasMatchingColor = checkedColors.some(checkedColor => {
                    return pColors.some(pColor => pColor.includes(checkedColor) || checkedColor.includes(pColor));
                });
                if (!hasMatchingColor) return false;
            }
            
            // Size filter
            if (checkedSizes.length > 0) {
                const pSizes = p.sizes ? p.sizes.map(s => s.toLowerCase()) : [];
                // Check if any checked size is available in product
                const hasMatchingSize = checkedSizes.some(checkedSize => {
                    return pSizes.includes(checkedSize);
                });
                if (!hasMatchingSize) return false;
            }
            
            return true;
        });

        // 3. Sort products
        const sortBy = sortSelect ? sortSelect.value : 'newest';
        if (sortBy === 'price_asc') {
            filtered.sort((a, b) => parseFloat(a.price) - parseFloat(b.price));
        } else if (sortBy === 'price_desc') {
            filtered.sort((a, b) => parseFloat(b.price) - parseFloat(a.price));
        } else {
            // Default: newest
            filtered.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
        }

        // 4. Render
        renderProducts(filtered);
    }

    function renderProducts(products) {
        // Update count
        const countEl = document.querySelector('.product-count');
        if (countEl) countEl.textContent = `Showing ${products.length} pieces`;

        if (products.length === 0) {
            grid.innerHTML = '<p class="text-gray-400 py-8 col-span-3 text-center">No products match the selected filters.</p>';
            return;
        }

        grid.innerHTML = '';
        products.forEach(p => {
            const img = p.image_urls && p.image_urls.length > 0 ? p.image_urls[0] : '';
            const imgHtml = img 
                ? `<img src="${img}" alt="${p.name}" class="product-img">` 
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
                        <div class="product-price">₹${parseFloat(p.price).toLocaleString('en-IN')}</div>
                    </div>
                </a>
            `;
            grid.innerHTML += card;
        });
    }
});
