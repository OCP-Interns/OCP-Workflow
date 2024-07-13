document.getElementById('sign-in-form').addEventListener('submit', function(e) {
	e.preventDefault();

	fetch('http://localhost:5000/sign-in', {
		method: 'POST',
		body: new FormData(this),
		headers: {
			'Accept': 'application/json'
		}
	})
	.then(response => response.json())
	.then(data => {
		if (data.success) {
			localStorage.setItem('user', JSON.stringify(data.user));
			window.location.href = 'dashboard.html'
		} else {
			alert(data.message || 'Invalid credentials');
		}
	})
	.catch(error => {
		console.error('Error:', error);
	});
});