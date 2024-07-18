const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electron', {
	minimize: () => ipcRenderer.send('minimize-window'),
	maximize: () => ipcRenderer.send('maximize-window'),
	close: () => ipcRenderer.send('close-window'),
	navigate: (page) => ipcRenderer.send('navigate', page)
});