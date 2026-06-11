const API_BASE = 'http://localhost:8000/api';

async function apiFetch(endpoint, options = {}) {
  const token = localStorage.getItem('arcform_access_token');
  const headers = { 'Content-Type': 'application/json', ...options.headers };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  
  const response = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });
  
  if (response.status === 401) {
    const refreshed = await refreshToken();
    if (refreshed) {
      const newToken = localStorage.getItem('arcform_access_token');
      headers['Authorization'] = `Bearer ${newToken}`;
      return fetch(`${API_BASE}${endpoint}`, { ...options, headers });
    } else {
      localStorage.removeItem('arcform_access_token');
      localStorage.removeItem('arcform_refresh_token');
      localStorage.removeItem('arcform_user');
      window.location.href = '/frontend/pages/auth/login.html';
    }
  }
  return response;
}

async function refreshToken() {
  const refresh = localStorage.getItem('arcform_refresh_token');
  if (!refresh) return false;
  try {
    const res = await fetch(`${API_BASE}/auth/token/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh })
    });
    if (res.ok) {
      const data = await res.json();
      localStorage.setItem('arcform_access_token', data.access);
      return true;
    }
  } catch (e) { console.error(e); }
  return false;
}

export const AuthAPI = {
  login: (data) => apiFetch('/auth/login/', { method: 'POST', body: JSON.stringify(data) }),
  register: (data) => apiFetch('/auth/register/', { method: 'POST', body: JSON.stringify(data) }),
  logout: (data) => apiFetch('/auth/logout/', { method: 'POST', body: JSON.stringify(data) }),
  getProfile: () => apiFetch('/auth/profile/'),
};

export const ProductsAPI = {
  getAll: (query='') => apiFetch(`/products/${query}`),
  getById: (id) => apiFetch(`/products/${id}/`),
  getFeatured: () => apiFetch('/products/featured/'),
  getCategories: () => apiFetch('/products/categories/'),
  getRelated: (id) => apiFetch(`/products/${id}/related/`),
};

export const OrdersAPI = {
  getAll: () => apiFetch('/orders/'),
  getById: (id) => apiFetch(`/orders/${id}/`),
  create: (data) => apiFetch('/orders/', { method: 'POST', body: JSON.stringify(data) }),
};

export const WishlistAPI = {
  getAll: () => apiFetch('/wishlist/'),
  add: (data) => apiFetch('/wishlist/add/', { method: 'POST', body: JSON.stringify(data) }),
  remove: (id) => apiFetch(`/wishlist/${id}/`, { method: 'DELETE' }),
};

export const AdminAPI = {
  getStats: () => apiFetch('/admin/dashboard/'),
};
