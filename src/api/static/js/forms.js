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

if (typeof employeeCIN !== 'undefined') {
	handleFormSubmit('edit-employee-form', 'form-validated', `/edit-employee-details/${employeeCIN}`,
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
			location.reload();
		}, 'Failed to update employee');
}

// ========= Manage Events =========
handleFormSubmit('add-event-form', 'form-validated', '/events', (data, formData) => {
		console.log(data);
		return true;
	}, (data, formData) => {
		alert('Event added successfully');
		location.reload();
	}, 'Failed to add event');

// ========= Manage Time Table =========
if (typeof employeeNum !== 'undefined') {
	handleFormSubmit('add-timetable-form', 'form-validated', `/edit-employee-timetable/${employeeNum}`,
		(formData) => {
			// Check if the start time is before (or equal to) the end time
			const from = parseInt(formData.get('from').split(':')[0]);
			const to = parseInt(formData.get('to').split(':')[0]);
			if (from >= to) {
				alert('Start time should be before the end time');
				return false;
			}
			return true;
		}, (data, formData) => {
			alert('Time table added successfully');
			window.location.href = `/edit-employee-timetable/${employeeNum}`;
		}, 'Failed to add time table');
}

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
		console.log(response);

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
(function () {
	'use strict';
	const forms = document.querySelectorAll('.needs-validation');
	Array.from(forms).forEach((form) => {
		console.log(form);
		form.addEventListener('submit', async (event) => {
			event.preventDefault();
			event.stopPropagation();

			if (form.checkValidity()) {
				form.dispatchEvent(formValidatedEvent);
			}

			form.classList.add('was-validated');
		});
	});
})();