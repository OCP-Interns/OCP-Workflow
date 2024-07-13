const { app, BrowserWindow, ipcMain, session } = require('electron');
const path = require('path');

let fetch;

try {
	require('electron-reloader')(module);
} catch { }

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

	win.loadFile(path.join(__dirname, '../index.html'));

	//import('node-fetch').then(({default: fetch}) => {
	//	const maxRetries = 5;
	//	const retryDelay = 2000;

	//	let attempts = 0;
	//	const attemptFetch = () => {
	//		const userSession = localStorage.getItem('user');
	//		if (userSession) {
	//			fetch('http://localhost:5000/re-establish', {
	//				method: 'POST',
	//				headers: {
	//					'Content-Type': 'application/json'
	//				},
	//				body: JSON.stringify({ user: JSON.parse(userSession) })
	//			})
	//			.then(response => response.json())
	//			.then(data => {
	//				if (data.success) {
	//					console.log(data.message);
	//					win.loadFile(path.join(__dirname, '../dashboard.html'));
	//				} else {
	//					console.log(data.message);
	//					win.loadFile(path.join(__dirname, '../index.html'));
	//				}
	//			})
	//			.catch(error => {
	//				if (attempts < maxRetries) {
	//					setTimeout(() => {
	//						console.log('Retrying...');
	//						attempts++;
	//						setTimeout(attemptFetch, retryDelay);
	//					}, retryDelay);
	//				} else {
	//					console.error('Error:', error);
	//				}
	//			});
	//		}
	//	};

	//	attemptFetch();
	//});

	win.on('closed', () => {
		win.destroy();
	});
}

ipcMain.on('send-session', async (event, userSession) => {
	const response = await fetch('http://localhost:5000/sign-in', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ user: userSession })
	});

	const data = await response.json();
	console.log(data);
	event.reply('navigate', data.success ? 'dashboard' : 'index');
});

app.whenReady().then(createWindow)

app.on('ready', () => {
	const ses = session.fromPartition('persist:ocp-workflow');
	//ses.clearStorageData();
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