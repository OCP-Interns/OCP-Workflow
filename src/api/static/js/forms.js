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

// ========= Handle Sign In =========
handleFormSubmit('sign-in-form', '/sign-in', (formData) => {},
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
	}, 'Invalid credentials', true);

// ========= Manage Employees =========
//handleFormSubmit('add-employee-form', '/add-employee', (formData) => {
//		console.log('Adding employee');
//		console.log(Object.fromEntries(formData));
//	}, (data, formData) => {
//		alert('Employee added successfully');
//		document.getElementById('add-employee-form').reset();
//	}, 'Failed to add employee');

// A generic function to handle all the form submissions
function handleFormSubmit(formId, url, callback, successCallback, message = '', use_json = false) {
	const form = document.getElementById(formId);
	if (!form)
		return;
	form.addEventListener('submit', async (e) => {
		e.preventDefault();

		const formData = new FormData(e.currentTarget);
		callback(formData);

		const response = use_json ? await fetch(url, {
			method: 'POST',
			body: JSON.stringify(Object.fromEntries(formData)),
			headers: {
				'Content-Type': 'application/json'
			}
		}) : await fetch(url, {
			method: 'POST',
			body: formData
		});

		const data = await response.json();
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
		console.log(form);
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
						body: formData
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