document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorElement = document.getElementById('error');

    fetch('https://register-server-logg.onrender.com/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            errorElement.textContent = 'Registration successful!';
            errorElement.style.color = 'green';
        } else {
            errorElement.textContent = data.error || 'Registration failed!';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        errorElement.textContent = 'An error occurred!';
    });
});
