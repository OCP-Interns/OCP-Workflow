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

document.getElementById('face-id-btn').addEventListener('click', async () => {
	try {
		const stream = await navigator.mediaDevices.getUserMedia({ video: true });
		const track = stream.getVideoTracks()[0];
		const imageCapture = new ImageCapture(track);

		const blob = await imageCapture.takePhoto();

		track.stop();

		const formData = new FormData();
		formData.append('file', blob, 'capture.png');

		const response = await axios({
			method: 'post',
			url: 'http://localhost:5000/face-recognition',
			data: formData,
			headers: {
				'Content-Type': 'multipart/form-data',
				'Access-Control-Allow-Origin': '*'
			}
		});

		console.log(response.data);
	} catch (error) {
		console.error('Error: ', error);
	}
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