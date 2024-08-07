const video = document.getElementById('cam1');
const canvas = document.createElement('canvas');
const context = canvas.getContext('2d');
let lastFrameTime = 0;
const frameInterval = 100;

function sendFrame(timestamp) {
    if (timestamp - lastFrameTime > frameInterval) {
        lastFrameTime = timestamp;

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const dataURL = canvas.toDataURL('image/jpeg');

        fetch('/frame', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `image=${encodeURIComponent(dataURL)}`
        })
        .then(response => response.text())
        .then(data => console.log(data))
        .catch(err => console.error('Fetch error: ', err));
    }
    requestAnimationFrame(sendFrame);
}

if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({video: true})
    .then(stream => {
        video.srcObject = stream;
        sendFrame();
    })
    .catch(err => console.error('Accessing webcam error: ', err));
} else {
    console.error("Browser doesn't support user media");
}