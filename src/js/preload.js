const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electron', {
	minimize: () => ipcRenderer.send('minimize-window'),
	maximize: () => ipcRenderer.send('maximize-window'),
	close: () => ipcRenderer.send('close-window'),
	sendSession: (userSession) => ipcRenderer.send('send-session', userSession),
	onNavigate: (callback) => ipcRenderer.on('navigate', (event, destination) => callback(destination)),
});