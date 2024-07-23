document.getElementById('minimize-btn').addEventListener('click', () => {
	window.electron.minimize();
});
document.getElementById('maximize-btn').addEventListener('click', () => {
	window.electron.maximize();
});
document.getElementById('close-btn').addEventListener('click', () => {
	window.electron.close();
});