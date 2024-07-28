document.addEventListener("DOMContentLoaded", function() {
    const video = document.getElementById('cam1');

        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function(stream) {
                // Attach the video stream to the video element
                video.srcObject = stream;
                video.play();
            })
            .catch(function(err) {
                console.error("Error accessing the camera: " + err);
            });

});
