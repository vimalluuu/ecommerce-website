export function getCart() {
  const cart = localStorage.getItem('arcform_cart');
  return cart ? JSON.parse(cart) : { items: [], updatedAt: Date.now() };
}

export function saveCart(cart) {
  cart.updatedAt = Date.now();
  localStorage.setItem('arcform_cart', JSON.stringify(cart));
  updateCartBadge();
}

export function addToCart(product, quantity=1, size=null, color=null) {
  const cart = getCart();
  const existing = cart.items.find(i => i.productId === product.id && i.size === size && i.color === color);
  
  if (existing) {
    existing.quantity += quantity;
  } else {
    cart.items.push({
      productId: product.id,
      name: product.name,
      price: product.price,
      image: product.image_urls ? product.image_urls[0] : '',
      quantity,
      size,
      color
    });
  }
  saveCart(cart);
}

export function removeFromCart(productId, size=null, color=null) {
  const cart = getCart();
  cart.items = cart.items.filter(i => !(i.productId === productId && i.size === size && i.color === color));
  saveCart(cart);
}

export function updateQuantity(productId, size, color, quantity) {
  const cart = getCart();
  const existing = cart.items.find(i => i.productId === productId && i.size === size && i.color === color);
  if (existing) {
    existing.quantity = quantity;
    if (existing.quantity <= 0) {
      removeFromCart(productId, size, color);
      return;
    }
    saveCart(cart);
  }
}

export function clearCart() {
  saveCart({ items: [], updatedAt: Date.now() });
}

export function getCartTotal() {
  const cart = getCart();
  return cart.items.reduce((total, item) => total + (item.price * item.quantity), 0);
}

export function getCartCount() {
  const cart = getCart();
  return cart.items.reduce((count, item) => count + item.quantity, 0);
}

export function updateCartBadge() {
  const badge = document.querySelector('.cart-badge, #cart-badge');
  if (badge) {
    badge.textContent = getCartCount();
    badge.style.display = getCartCount() > 0 ? 'inline-block' : 'none';
  }
}

document.addEventListener('DOMContentLoaded', updateCartBadge);
