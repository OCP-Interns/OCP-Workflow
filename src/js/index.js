const { app, BrowserWindow, ipcMain, session } = require('electron');
const path = require('path');
const Storage = require('electron-store');
try {
	require('electron-reloader')(module);
} catch { };

const storage = new Storage();
let win;

function createWindow() {
	win = new BrowserWindow({
		width: 1280,
		height: 720,
		frame: false,
		webPreferences: {
			partition: 'persist:ocp-workflow',
			preload: path.join(__dirname, 'preload.js'),
			nodeIntegration: true
		}
	});

	win.loadFile(path.join(__dirname, '../pages/loader.html'));
	console.log('Window created');

	win.on('closed', () => {
		win.destroy();
		fetch('http://localhost:5000/exit', {
			method: 'POST'
		}).then(() => {
			console.log('Server stopped');
		}).catch((error) => {
			console.error('Error: ', error);
		});
		
	});
}

app.whenReady().then(() => {
	console.log('App ready');
	createWindow();

	//! This is for development purposes only
	storage.clear();

	const userSession = storage.get('session');
	win.webContents.send('validate-session', userSession);
});

ipcMain.on('save-session', (event, user) => {
	console.log('Session saved');
	// Current date in milliseconds
	const date = Date.now();

	storage.set('session', JSON.stringify({ user, date }));
});
ipcMain.on('clear-session', (event) => {
	console.log('Session cleared');
	storage.delete('session');
});

app.on('window-all-closed', () => {
	if (process.platform !== 'darwin') {
		app.quit()
	}
});

app.on('activate', () => {
	if (BrowserWindow.getAllWindows().length === 0) {
		createWindow()
	}
});

ipcMain.on('minimize-window', () => {
	win.minimize();
});
ipcMain.on('maximize-window', () => {
	win.isMaximized() ? win.unmaximize() : win.maximize();
});
ipcMain.on('close-window', () => {
	win.close();
});