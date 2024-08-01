fetch('https://register-server-logg.onrender.com/register', { // Adicionado '/register' ao final da URL
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
