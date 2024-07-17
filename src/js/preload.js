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
	const serverUrl = 'http://localhost:5000';
	const pingEndpoint = `${serverUrl}/ping`;
	const signInUrl = `${serverUrl}/sign-in`;
	const dashboardUrl = `${serverUrl}/dashboard`;
	const validateSessionEndpoint = `${serverUrl}/validate-session`;
	const retryDelay = 2000;

	console.log('Validating session...');
	const pingServer = () => {
		console.log('Pinging server...');
		return fetch(pingEndpoint)
			.then(response => {
				if (!response.ok) {
					throw new Error('Server not ready');
				}
				return response;
			})
			.catch(() => {
				console.log('Server not ready, retrying...');
				return new Promise(resolve => setTimeout(resolve, retryDelay))
					.then(pingServer);
			});
	};

	const validateSession = () => {
		console.log('Attempting to validate session...');
		if (!userSession) {
			console.log('No session found');
			window.location.href = signInUrl;
			return;
		}

		const date = JSON.parse(userSession).date;
		if (Date.now() - date > 3 * 24 * 60 * 60 * 1000) {
			console.log('Session expired');
			ipcRenderer.send('clear-session');
			window.location.href = signInUrl;
			return;
		}

		fetch(validateSessionEndpoint, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ user: JSON.parse(userSession).user })
		})
		.then(response => response.json())
		.then(data => {
			console.log('Fetch successful');
			console.log(data.message);
			if (data.success) {
				console.log('Session valid');
				ipcRenderer.send('save-session', JSON.parse(userSession).user);
				window.location.href = dashboardUrl;
			} else {
				console.log('Session not valid');
				window.location.href = signInUrl;
			}
		})
		.catch(error => {
			console.error('Error:', error);
			window.location.href = signInUrl;
		});
	};

	pingServer().then(validateSession);
});