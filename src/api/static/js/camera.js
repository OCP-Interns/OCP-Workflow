document.addEventListener("DOMContentLoaded", function() {
    const cameraIds = ['cam1'];

    cameraIds.forEach(function(id) {
        const video = document.getElementById(id);
        if (video) {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(function(stream) {
                    video.srcObject = stream;
                    video.play();
                    sendFrames(video)
                })
                .catch(function(err) {
                    console.error("Error accessing the camera for " + id + ": " + err);
                });
        }
    });
});

