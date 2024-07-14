const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');

try {
	require('electron-reloader')(module);
} catch { }

let win;

function createWindow() {
	win = new BrowserWindow({
        width: 900,
        height: 600,
		frame: false,
		webPreferences: {
			preload: path.join(__dirname, 'preload.js'),
			nodeIntegration: true
		}
	});
	win.loadURL('http://localhost:5500/src/dashboard.html');
	win.on('closed', () => {
		win.destroy();
	});

}

app.whenReady().then(createWindow)

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