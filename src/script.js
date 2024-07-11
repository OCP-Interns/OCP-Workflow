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