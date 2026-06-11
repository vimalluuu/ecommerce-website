const API_BASE = 'http://localhost:8000/api';

let supabaseInstance = null;

async function loadSupabaseScript() {
  if (window.supabase) return window.supabase;
  return new Promise((resolve, reject) => {
    const existingScript = document.querySelector('script[src*="supabase-js"]');
    if (existingScript) {
      existingScript.addEventListener('load', () => resolve(window.supabase));
      existingScript.addEventListener('error', () => reject(new Error('Failed to load Supabase script')));
      return;
    }
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2';
    script.async = true;
    script.onload = () => resolve(window.supabase);
    script.onerror = () => reject(new Error('Failed to load Supabase script'));
    document.head.appendChild(script);
  });
}

export async function getSupabase() {
  if (supabaseInstance) return supabaseInstance;
  const sb = await loadSupabaseScript();
  const SUPABASE_URL = 'https://vptxsqipcshkpjhzbhdt.supabase.co';
  const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZwdHhzcWlwY3Noa3BqaHpoYmR0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODEwODExMzQsImV4cCI6MjA5NjY1NzEzNH0.Qrf0s1FwqwdnADiee89tod0xOOgS4wEaMl3HMgmZdHE';
  
  supabaseInstance = sb.createClient(SUPABASE_URL, SUPABASE_KEY);
  return supabaseInstance;
}

// Auto-trigger load in background
getSupabase().catch(e => console.error("Initial Supabase load failed", e));

async function apiFetch(endpoint, options = {}) {
  let token = localStorage.getItem('arcform_access_token');
  try {
    const supabase = await getSupabase();
    const { data: { session } } = await supabase.auth.getSession();
    if (session) {
      token = session.access_token;
      localStorage.setItem('arcform_access_token', session.access_token);
      if (session.refresh_token) {
        localStorage.setItem('arcform_refresh_token', session.refresh_token);
      }
      localStorage.setItem('arcform_user', JSON.stringify({
        id: session.user.id,
        email: session.user.email,
        name: session.user.user_metadata.name || session.user.email,
        is_admin: session.user.user_metadata.is_admin || false
      }));
    }
  } catch (e) {
    console.error("Supabase session verification failed, using cache token", e);
  }

  const headers = { 'Content-Type': 'application/json', ...options.headers };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  
  const response = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });
  
  if (response.status === 401) {
    localStorage.removeItem('arcform_access_token');
    localStorage.removeItem('arcform_refresh_token');
    localStorage.removeItem('arcform_user');
    window.location.href = '/pages/auth/login.html';
  }
  return response;
}

export const AuthAPI = {
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
