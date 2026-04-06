// Login Page Script
document.addEventListener('DOMContentLoaded', () => {
    // Redirect if already logged in
    if (isAuthenticated()) {
        window.location.href = 'home.html';
        return;
    }

    const loginForm = document.getElementById('loginForm');
    const errorMessage = document.getElementById('errorMessage');
    const successMessage = document.getElementById('successMessage');

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        // Clear previous messages
        errorMessage.classList.remove('show');
        successMessage.classList.remove('show');

        try {
            // Show loading state
            const submitBtn = loginForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.disabled = true;
            submitBtn.textContent = '⏳ Entrando...';

            // Login
            const response = await API.login(email, password);
            
            // Save token
            localStorage.setItem(STORAGE_KEYS.TOKEN, response.access_token);
            localStorage.setItem(STORAGE_KEYS.USER_ID, email);

            // Show success message
            successMessage.textContent = '✅ Login realizado com sucesso! Redirecionando...';
            successMessage.classList.add('show');

            // Redirect after 1 second
            setTimeout(() => {
                window.location.href = 'home.html';
            }, 1500);

        } catch (error) {
            // Show error message
            errorMessage.textContent = '❌ Erro ao fazer login. Verifique suas credenciais.';
            errorMessage.classList.add('show');
            
            // Reset button
            const submitBtn = loginForm.querySelector('button[type="submit"]');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Entrar';

            console.error('Login error:', error);
        }
    });
});
