document.addEventListener('DOMContentLoaded', function () {
	// Tooltip
	var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
	var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
		return new bootstrap.Tooltip(tooltipTriggerEl, {
			container: 'body'
		});
	});

	// User session
	const userSession = localStorage.getItem('user');
	if (userSession) {
		const user = JSON.parse(userSession);
		window.electron.sendSession(user);
	}

	window.electron.onNavigate((destination) => {
		if (destination === 'dashboard') {
			window.location.href = 'dashboard.html';
		} else {
			window.location.href = 'index.html';
		}
	});
});