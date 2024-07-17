const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electron', {
	minimize: () => ipcRenderer.send('minimize-window'),
	maximize: () => ipcRenderer.send('maximize-window'),
	close: () => ipcRenderer.send('close-window'),

	saveSession: (user) => ipcRenderer.send('save-session', user),
	clearSession: () => ipcRenderer.send('clear-session'),

	send: (channel, data) => {
		let validChannels = ['validate-session'];
		if (validChannels.includes(channel)) {
			ipcRenderer.send(channel, data);
		}
	}
});

console.log('Preload script loaded');

ipcRenderer.on('validate-session', (event, userSession) => {
	const maxRetries = 5;
	const retryDelay = 2000;

	let attempts = 0;
	let fetchSuccessful = false;

	const attemptFetch = () => {
		console.log('Attempting to validate session...');

		if (userSession && !fetchSuccessful) {
			// Check if the session has expired
			const date = JSON.parse(userSession).date;
			console.log('Difference:', Date.now() - date);
			//                      3 days in milliseconds
			if (Date.now() - date > 3 * 24 * 60 * 60 * 1000) {
			// for testing purposes, we will set the session to expire in 30 seconds
			//if (Date.now() - date > 30 * 1000) {
				console.log('Session expired');
				// Delete the session
				ipcRenderer.send('clear-session');
				//window.location.href = 'index.html';
				window.location.href = 'http://localhost:5000/sign-in';
				return;
			}

			fetch('http://localhost:5000/validate-session', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ user: JSON.parse(userSession).user })
			})
			.then(response => response.json())
			.then(data => {
				fetchSuccessful = true;
				console.log('Fetch successful');
				console.log(data.message);
				if (data.success) {
					// Renew the session
					ipcRenderer.send('save-session', userSession.user);
					window.location.href = 'http://localhost:5000/dashboard';
				} else {
					//window.location.href = 'index.html';
					window.location.href = 'http://localhost:5000/sign-in';
				}
			})
			.catch(error => {
				if (attempts < maxRetries) {
					console.log('Retrying...');
					attempts++;
					setTimeout(attemptFetch, retryDelay);
				} else {
					console.error('Error:', error);
				}
			});
		}
	};

	attemptFetch();
});
