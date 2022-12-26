// Select elements here
//const video = document.getElementById('video');

//here we check if the browser is able to play videos from our custom player
/** 
document.querySelector("#input-video-file").addEventListener("change", (event) =>{
    const video = document.createElement('video');
    const box = document.getElementById('video-box');

    if (video.canPlayType) {
        const file = event.target.files[0];
        var url = URL.createObjectURL(file);
        video.src = url;
        video.controls = true;
        video.muted = false;
        video.autoplay = true;
        box.append(video);
    }
})
*/

window.onload = function(){

    let dropArea = document.getElementById("drop-area");

    //Prevent default drag behaviors
    ;['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);   
        document.body.addEventListener(eventName, preventDefaults, false);
    })

    // Highlight drop area when item is dragged over it
    ;['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false)
    })

    ;['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    })

    // Handle dropped files
    dropArea.addEventListener('drop', handleDrop, false);

    function preventDefaults (e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function highlight(e) {
        dropArea.classList.add('highlight')
    }

    function unhighlight(e) {
        dropArea.classList.remove('active')
    }

    function handleDrop(e) {
        var data = e.dataTransfer;
        var file = data.files[0];

        const video = document.createElement('video');
        const box = document.getElementById('video-box');
    
        if (video.canPlayType) {
            var url = URL.createObjectURL(file);
            video.src = url;
            video.controls = true;
            video.muted = false;
            video.autoplay = true;
            box.append(video);
        }
    }

    document.querySelector("#fileElem").addEventListener("change", (event) =>{
        const video = document.createElement('video');
        const box = document.getElementById('video-box');
    
        if (video.canPlayType) {
            const file = event.target.files[0];
            var url = URL.createObjectURL(file);
            video.src = url;
            video.controls = true;
            video.muted = false;
            video.autoplay = true;
            box.append(video);
        }
    })

}