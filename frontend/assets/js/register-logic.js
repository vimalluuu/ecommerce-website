import { authRegister, isLoggedIn } from './auth.js';

document.addEventListener('DOMContentLoaded', () => {
    if (isLoggedIn()) {
        window.location.href = '../user/dashboard.html';
        return;
    }

    const registerForm = document.getElementById('registerForm');
    if (!registerForm) return;

    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const inputs = registerForm.querySelectorAll('input');
        const name = inputs[0].value;
        const email = inputs[1].value;
        const password = inputs[2].value;
        const btn = registerForm.querySelector('.btn-auth');
        
        const originalText = btn.textContent;
        btn.textContent = 'Creating Account...';
        btn.disabled = true;

        try {
            const success = await authRegister(name, email, password);
            if (success) {
                // Redirect will happen in authRegister or we do it here
                window.location.href = '../user/dashboard.html';
            } else {
                alert('Registration failed. Email might be already in use.');
                btn.textContent = originalText;
                btn.disabled = false;
            }
        } catch (err) {
            console.error(err);
            alert('An error occurred during registration.');
            btn.textContent = originalText;
            btn.disabled = false;
        }
    });
});
