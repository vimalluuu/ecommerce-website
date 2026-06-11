import { authLogin, isLoggedIn } from './auth.js';

document.addEventListener('DOMContentLoaded', () => {
    if (isLoggedIn()) {
        window.location.href = '../user/dashboard.html';
        return;
    }

    const loginForm = document.getElementById('loginForm');
    if (!loginForm) return;

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const inputs = loginForm.querySelectorAll('input');
        const email = inputs[0].value;
        const password = inputs[1].value;
        const btn = loginForm.querySelector('.btn-auth');
        
        const originalText = btn.textContent;
        btn.textContent = 'Signing In...';
        btn.disabled = true;

        try {
            const success = await authLogin(email, password);
            if (success) {
                // Redirect will happen in authLogin or we do it here
                window.location.href = '../user/dashboard.html';
            } else {
                alert('Invalid email or password.');
                btn.textContent = originalText;
                btn.disabled = false;
            }
        } catch (err) {
            console.error(err);
            alert('An error occurred during sign in.');
            btn.textContent = originalText;
            btn.disabled = false;
        }
    });
});
