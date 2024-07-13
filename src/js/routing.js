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

		const data = response.data;
		if (data.success) {
			console.log('Saving session');
			window.electron.saveSession(data.user);
			window.location.href = 'dashboard.html';
		} else {
			alert(data.error || 'Face not recognized');
		}
	} catch (error) {
		console.error('Error: ', error);
	}
});
