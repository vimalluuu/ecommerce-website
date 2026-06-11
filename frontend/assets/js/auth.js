import { getSupabase } from './api.js';

export function isLoggedIn() {
  return !!localStorage.getItem('arcform_access_token');
}

export function getUser() {
  const user = localStorage.getItem('arcform_user');
  return user ? JSON.parse(user) : null;
}

export async function authLogin(email, password) {
  try {
    const supabase = await getSupabase();
    const { data, error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) throw error;
    return true;
  } catch (e) {
    console.error("Supabase login error:", e);
    return false;
  }
}

export async function authRegister(name, email, password) {
  try {
    const supabase = await getSupabase();
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: { name }
      }
    });
    if (error) throw error;
    return true;
  } catch (e) {
    console.error("Supabase registration error:", e);
    return false;
  }
}

export async function authLogout() {
  try {
    const supabase = await getSupabase();
    await supabase.auth.signOut();
  } catch (e) {
    console.error("Supabase logout error:", e);
  }
  localStorage.removeItem('arcform_access_token');
  localStorage.removeItem('arcform_refresh_token');
  localStorage.removeItem('arcform_user');
  window.location.href = '/pages/public/home.html';
}

export function requireAuth() {
  if (!isLoggedIn()) {
    window.location.href = '/pages/auth/login.html';
  }
}

export function requireAdmin() {
  const user = getUser();
  if (!user || !user.is_admin) {
    window.location.href = '/pages/auth/login.html';
  }
}

export function updateNavForAuth() {
  const user = getUser();
  const accIcon = document.querySelector('.account-icon');
  if (accIcon) {
    if (user) {
      accIcon.href = user.is_admin ? '/pages/admin/dashboard.html' : '/pages/user/dashboard.html';
    } else {
      accIcon.href = '/pages/auth/login.html';
    }
  }
}

// Setup state change listener for session synchronization
getSupabase().then(supabase => {
  supabase.auth.onAuthStateChange((event, session) => {
    if (session) {
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
    } else {
      localStorage.removeItem('arcform_access_token');
      localStorage.removeItem('arcform_refresh_token');
      localStorage.removeItem('arcform_user');
    }
    updateNavForAuth();
  });
}).catch(e => console.error("Failed to initialize Supabase auth listener", e));

document.addEventListener('DOMContentLoaded', updateNavForAuth);
