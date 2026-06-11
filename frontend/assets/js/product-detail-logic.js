import { ProductsAPI } from './api.js';
import { addToCart } from './cart.js';

document.addEventListener('DOMContentLoaded', async () => {
    const params = new URLSearchParams(window.location.search);
    const productId = params.get('id');

    if (!productId) {
        document.querySelector('.product-info').innerHTML = '<p>Product not found.</p>';
        return;
    }

    try {
        const res = await ProductsAPI.getById(productId);
        if (!res.ok) throw new Error('Product not found');
        const product = await res.json();

        // Update basic info
        document.title = `ARCFORM | ${product.name}`;
        document.querySelector('.product-title').textContent = product.name;
        document.querySelector('.product-price').textContent = `₹${product.price}`;
        document.querySelector('.product-description').textContent = product.description;
        
        // Update Breadcrumb
        const categoryName = product.category ? product.category.name : 'Category';
        document.querySelector('.breadcrumb').innerHTML = `<a href="home.html">Home</a> / <a href="shop.html">Shop</a> / ${categoryName}`;

        // Update Images
        const mainImage = document.querySelector('.main-image');
        const thumbnails = document.querySelector('.thumbnails');
        
        if (product.image_urls && product.image_urls.length > 0) {
            mainImage.innerHTML = `<img src="${product.image_urls[0]}" alt="${product.name}" style="width:100%; height:100%; object-fit:cover;">`;
            thumbnails.innerHTML = '';
            product.image_urls.forEach((img, idx) => {
                const thumb = document.createElement('div');
                thumb.className = `thumbnail ${idx === 0 ? 'active' : ''}`;
                thumb.innerHTML = `<img src="${img}" style="width:100%; height:100%; object-fit:cover;">`;
                thumb.onclick = () => {
                    document.querySelectorAll('.thumbnail').forEach(t => t.classList.remove('active'));
                    thumb.classList.add('active');
                    mainImage.innerHTML = `<img src="${img}" style="width:100%; height:100%; object-fit:cover;">`;
                };
                thumbnails.appendChild(thumb);
            });
        }

        // Update Sizes
        const sizeContainer = document.querySelector('.size-selector');
        sizeContainer.innerHTML = '';
        let selectedSize = product.sizes && product.sizes.length > 0 ? product.sizes[0] : 'OS';
        
        if (product.sizes) {
            product.sizes.forEach(size => {
                const btn = document.createElement('button');
                btn.className = `size-btn ${size === selectedSize ? 'selected' : ''}`;
                btn.textContent = size;
                btn.onclick = () => {
                    document.querySelectorAll('.size-btn').forEach(b => b.classList.remove('selected'));
                    btn.classList.add('selected');
                    selectedSize = size;
                };
                sizeContainer.appendChild(btn);
            });
        }

        // Add to Cart Logic
        const addBtn = document.querySelector('.btn-add-cart');
        // Replace onclick to avoid the inline alert
        addBtn.removeAttribute('onclick');
        addBtn.addEventListener('click', () => {
            const color = product.colors && product.colors.length > 0 ? product.colors[0] : null;
            addToCart(product, 1, selectedSize, color);
            alert(`Added ${product.name} (Size: ${selectedSize}) to cart!`);
        });

    } catch (e) {
        console.error(e);
        document.querySelector('.product-info').innerHTML = '<p>Error loading product details.</p>';
    }
});
