document.getElementById('sign-in-form').addEventListener('submit', async function(e) {
	e.preventDefault();

	const formData = new FormData(this);
	console.log(formData.get('reg_num'));
	const response = await fetch('http://localhost:5000/sign-in', {
		method: 'POST',
		body: JSON.stringify(Object.fromEntries(formData)),
		headers: {
			'Content-Type': 'application/json'
		}
	});

	const data = await response.json();
	if (data.success) {
		const remember = formData.get('remember_me') === 'on';
		if (remember) {
			console.log('Saving session');
			window.electron.saveSession(data.user);
		} else {
			console.log('Clearing session');
			window.electron.clearSession();
		}
		window.location.href = 'dashboard.html'
	} else {
		alert(data.message || 'Invalid credentials');
	}
});
