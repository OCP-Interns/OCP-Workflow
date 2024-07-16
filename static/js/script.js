document.addEventListener('DOMContentLoaded', () => {
	console.log('\x1b[32m%s\x1b[0m', 'DOM fully loaded and parsed');

	const btn = document.getElementById('show-password-btn');

	btn.addEventListener('mousedown', (e) => {
		const button = e.currentTarget;
		button.querySelector('.bi-eye-slash').style.display = 'none';
		button.querySelector('.bi-eye-slash-fill').style.display = 'none';
		button.querySelector('.bi-eye-fill').style.display = 'inline';

		document.getElementById('password').type = 'text';
	});

	btn.addEventListener('mouseup', (e) => {
		const button = e.currentTarget;
		button.querySelector('.bi-eye-slash').style.display = 'none';
		button.querySelector('.bi-eye-slash-fill').style.display = 'inline';
		button.querySelector('.bi-eye-fill').style.display = 'none';

		document.getElementById('password').type = 'password';
	});

	btn.addEventListener('mouseleave', (e) => {
		const button = e.currentTarget;
		button.querySelector('.bi-eye-slash').style = '';
		button.querySelector('.bi-eye-slash-fill').style = '';
		button.querySelector('.bi-eye-fill').style = '';

		document.getElementById('password').type = 'password';
	});
});

document.getElementById('minimize-btn').addEventListener('click', () => {
	window.electron.minimize();
});
document.getElementById('maximize-btn').addEventListener('click', () => {
	window.electron.maximize();
});
document.getElementById('close-btn').addEventListener('click', () => {
	window.electron.close();
});