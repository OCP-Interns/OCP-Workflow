const faceIDButton = document.getElementById('face-id-btn');
if (faceIDButton) {
	faceIDButton.addEventListener('click', async () => {
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
				url: '/face-recognition',
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
				window.location.href = '/dashboard';
			} else {
				alert(data.error || 'Face not recognized');
			}
		} catch (error) {
			console.error('Error: ', error);
		}
	});
}

//document.getElementById('sign-in-form').addEventListener('submit', async (e) => {
//	e.preventDefault();

//	const formData = new FormData(this);
//	console.log(formData.get('reg_num'));
//	const response = await fetch('http://localhost:5000/sign-in', {
//		method: 'POST',
//		body: JSON.stringify(Object.fromEntries(formData)),
//		headers: {
//			'Content-Type': 'application/json'
//		}
//	});

//	const data = await response.json();
//	if (data.success) {
//		const remember = formData.get('remember_me') === 'on';
//		if (remember) {
//			console.log('Saving session');
//			window.electron.saveSession(data.user);
//		} else {
//			console.log('Clearing session');
//			window.electron.clearSession();
//		}
//		window.location.href = 'http://localhost:5000/dashboard';
//	} else {
//		alert(data.message || 'Invalid credentials');
//	}
//});

// ========= Manage Employees ==========
//document.getElementById('add-employee-form').addEventListener('submit', async (e) => {
//	e.preventDefault();

//	const formData = new FormData(this);
//	const response = await fetch('http://localhost:5000/add-employee', {
//		method: 'POST',
//		body: JSON.stringify(Object.fromEntries(formData)),
//		headers: {
//			'Content-Type': 'application/json'
//		}
//	});

//	const data = await response.json();
//	if (data.success) {
//		alert('Employee added successfully');
//		this.reset();
//	} else {
//		alert(data.message || 'Failed to add employee');
//	}
//});

// ========= Handle Sign In =========
handleFormSubmitJSON('sign-in-form', '/sign-in', (data, formData) => {},
	(data, formData) => {
		const remember = formData.get('remember_me') === 'on';
		console.log(data);
		if (remember) {
			console.log('Saving session');
			window.electron.saveSession(data.user);
		} else {
			console.log('Clearing session');
			window.electron.clearSession();
		}
		window.location.href = '/dashboard';
	}, 'Invalid credentials');

// ========= Manage Employees =========
handleFormSubmitJSON('add-employee-form', '/add-employee', (data, formData) => {
		console.log(data);
	}, (data, formData) => {
		alert('Employee added successfully');
		document.getElementById('add-employee-form').reset();
	}, 'Failed to add employee');

// A generic function to handle all the form submissions
function handleFormSubmitJSON(formId, url, callback, successCallback, message = '') {
	const form = document.getElementById(formId);
	if (!form)
		return;
	form.addEventListener('submit', async (e) => {
		e.preventDefault();

		const formData = new FormData(e.currentTarget);
		const response = await fetch(url, {
			method: 'POST',
			body: JSON.stringify(Object.fromEntries(formData)),
			headers: {
				'Content-Type': 'application/json'
			}
		});

		const data = await response.json();
		callback(data, formData);

		if (data.success) {
			successCallback(data, formData);
		} else {
			alert(data.message || message);
		}
	});
}

// Handle all bootstrap form validations
(function() {
	'use strict';
	const forms = document.querySelectorAll('.needs-validation');
	Array.from(forms).forEach((form) => {
		form.addEventListener('submit', async (event) => {
			if (!form.checkValidity()) {
				event.preventDefault();
				event.stopPropagation();
			} else {
				if (form.id === 'add-employee-form') {
					event.preventDefault();
					event.stopPropagation();

					const formData = new FormData(form);
					const response = await fetch('/add-employee', {
						method: 'POST',
						body: JSON.stringify(Object.fromEntries(formData)),
						headers: {
							'Content-Type': 'application/json'
						}
					});

					const data = await response.json();
					console.log(data);

					if (data.success) {
						window.location.href = '/manage-employees';
					} else {
						alert(data.message || 'Failed to add employee');
					}

					console.log('Form validated');
				}
			}

			form.classList.add('was-validated');
		});
	});
})();