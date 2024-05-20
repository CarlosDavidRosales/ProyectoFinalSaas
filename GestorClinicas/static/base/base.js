document.getElementById('login').addEventListener('click', function(event) {
    event.preventDefault();
    var loginForm = document.getElementById('loginForm');
    var registerForm = document.getElementById('registerForm');
    if (loginForm.style.display === 'block') {
        loginForm.style.display = 'none';
    } else {
        loginForm.style.display = 'block';
        registerForm.style.display = 'none'; // Asegura que el formulario de registro esté cerrado
    }
});

document.getElementById('register').addEventListener('click', function(event) {
    event.preventDefault();
    var registerForm = document.getElementById('registerForm');
    var loginForm = document.getElementById('loginForm');
    if (registerForm.style.display === 'block') {
        registerForm.style.display = 'none';
    } else {
        registerForm.style.display = 'block';
        loginForm.style.display = 'none'; // Asegura que el formulario de inicio de sesión esté cerrado
    }
});

function toggleVisibility(form) {
    if (form.style.display === 'block') {
        form.style.display = 'none';
    } else {
        form.style.display = 'block';
    }
}

// Mostrar el mensaje de error si existe
window.onload = function() {
    var errorMessage = document.getElementById('errorMessage');
    if (errorMessage) {
        errorMessage.style.display = 'block';
        setTimeout(function() {
            errorMessage.style.display = 'none';
        }, 5000); // Ocultar después de 5 segundos
    }
};