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
handleFormSubmit('sign-in-form', 'submit', '/sign-in',
	(formData) => true,
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
handleFormSubmit('add-employee-form', 'form-validated', '/add-employee',
	(formData) => {
		// Check the size of the image
		const file = formData.get('photo');
		if (file.size > 1000000) {
			alert('Image size should not exceed 1MB');
			return false;
		}
		return true;
	},
	(data, formData) => {
		alert('Employee added successfully');
		window.location.href = '/manage-employees';
	}, 'Failed to add employee');

handleFormSubmit('edit-employee-form', 'submit', `/edit-employee/${employeeCIN}`,
	(formData) => {
		// Check the size of the image if an image was uploaded
		const file = formData.get('photo');
		if (file && file.size > 1000000) {
			alert('Image size should not exceed 1MB');
			return false;
		}
		return true;
	},
	(data, formData) => {
		alert('Employee updated successfully');
		window.location.href = '/manage-employees';
	}, 'Failed to update employee');

// ========= General =========
// A generic function to handle all the form submissions
function handleFormSubmit(formId, event, url, callback, successCallback, message = '', use_json = false) {
	const form = document.getElementById(formId);
	if (!form)
		return;
	form.addEventListener(event, async (e) => {
		e.preventDefault();

		const formData = new FormData(e.currentTarget);
		var valid = callback(formData);
		if (!valid) {
			return;
		}

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

// A custom event to handle form validation
const formValidatedEvent = new Event('form-validated', {
	detail: { message: 'Form has been validated successfully' }
});

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
					form.dispatchEvent(formValidatedEvent);
				}
			}

			form.classList.add('was-validated');
		});
	});
})();