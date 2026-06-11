import { AuthAPI } from './api.js';

export function isLoggedIn() {
  return !!localStorage.getItem('arcform_access_token');
}

export function getUser() {
  const user = localStorage.getItem('arcform_user');
  return user ? JSON.parse(user) : null;
}

export async function authLogin(email, password) {
  const res = await AuthAPI.login({ email, password });
  if (res.ok) {
    const data = await res.json();
    localStorage.setItem('arcform_access_token', data.access);
    localStorage.setItem('arcform_refresh_token', data.refresh);
    const profileRes = await AuthAPI.getProfile();
    if (profileRes.ok) {
      const profile = await profileRes.json();
      localStorage.setItem('arcform_user', JSON.stringify(profile));
    }
    return true;
  }
  return false;
}

export async function authLogout() {
  const refresh = localStorage.getItem('arcform_refresh_token');
  if (refresh) {
    await AuthAPI.logout({ refresh });
  }
  localStorage.removeItem('arcform_access_token');
  localStorage.removeItem('arcform_refresh_token');
  localStorage.removeItem('arcform_user');
  window.location.href = '/frontend/pages/public/home.html';
}

export function requireAuth() {
  if (!isLoggedIn()) {
    window.location.href = '/frontend/pages/auth/login.html';
  }
}

export function requireAdmin() {
  const user = getUser();
  if (!user || !user.is_admin) {
    window.location.href = '/frontend/pages/auth/login.html';
  }
}

export function updateNavForAuth() {
  const user = getUser();
  const accIcon = document.querySelector('.account-icon');
  if (accIcon) {
    if (user) {
      accIcon.href = user.is_admin ? '/frontend/pages/admin/dashboard.html' : '/frontend/pages/user/dashboard.html';
    } else {
      accIcon.href = '/frontend/pages/auth/login.html';
    }
  }
}

document.addEventListener('DOMContentLoaded', updateNavForAuth);
