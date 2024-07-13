const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electron', {
	minimize: () => ipcRenderer.send('minimize-window'),
	maximize: () => ipcRenderer.send('maximize-window'),
	close: () => ipcRenderer.send('close-window'),

	saveSession: (userSession) => ipcRenderer.send('save-session', userSession),
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
			fetch('http://localhost:5000/validate-session', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ user: JSON.parse(userSession) })
			})
			.then(response => response.json())
			.then(data => {
				fetchSuccessful = true;
				console.log('Fetch successful');
				if (data.success) {
					console.log(data.message);
					window.location.href = 'dashboard.html';
				} else {
					console.log(data.message);
					window.location.href = 'index.html';
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
