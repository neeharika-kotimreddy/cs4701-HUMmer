const startRecordingButton = document.getElementById('startRecording');
const startRecordingButton2 = document.getElementById('startRecording2');

// const stopRecordingButton = document.getElementById('stopRecording');
const retryButton = document.getElementById('retry')
const saveButton = document.getElementById('save')

const audioPlayer = document.getElementById('audioPlayer');
const audioPlayer2 = document.getElementById('audioPlayer2');

const countdownTimer = document.getElementById('countdownTimer');
const countdownTimer2 = document.getElementById('countdownTimer2');

const songName = document.getElementById("songName")

const song_list = document.getElementById('songs')

let recorder;
let audioChunks = [];
let countdownInterval;
const RECORDING_TIME = 10; // in seconds

startRecordingButton.addEventListener('click', startRecording);
startRecordingButton2.addEventListener('click', startRecordingData);

retryButton.addEventListener('click', retry);
saveButton.addEventListener('click', save)

// stopRecordingButton.addEventListener('click', stopRecording);

document.addEventListener("DOMContentLoaded", (event) => {
    fetch('/get_songs', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {

        for(var song of data['songs']) {
            song_list.innerHTML += `<option value="${song}"> ${song} </option>`
        }
    })
});

async function save() {
    const audioBlob = await fetch(audioPlayer2.src).then(r => r.blob());
    const formData = new FormData();
    const song_name = song_list.value
    console.log(audioBlob)
    formData.append('audio', audioBlob, 'recorded_audio.wav');
    formData.append('song_name', song_name)
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('Error uploading file:', error);
        });
}

function retry() {
    fetch('/retry', {
        method: 'GET',
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            song_name = data["song_name"]
            songName.innerText = song_name
        })

}

function startRecordingData() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            recorder = new MediaRecorder(stream);
            recorder.start();
            startRecordingButton.disabled = true;
            // stopRecordingButton.disabled = false;
            audioChunks = [];
            countdownTimer2.innerText = RECORDING_TIME;

            countdownInterval = setInterval(() => {
                const remainingTime = parseInt(countdownTimer2.innerText) - 1;
                countdownTimer2.innerText = remainingTime;
                if (remainingTime <= 0) {
                    stopRecording();
                }
            }, 1000);

            recorder.addEventListener('dataavailable', event => {
                audioChunks.push(event.data);
            });

            recorder.addEventListener('stop', () => {
                clearInterval(countdownInterval);
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const audioUrl = URL.createObjectURL(audioBlob);
                audioPlayer2.src = audioUrl;
            });
        })
        .catch(error => {
            console.error('Error accessing microphone:', error);
        });
}

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            recorder = new MediaRecorder(stream);
            recorder.start();
            startRecordingButton.disabled = true;
            // stopRecordingButton.disabled = false;
            audioChunks = [];
            countdownTimer.innerText = RECORDING_TIME;

            countdownInterval = setInterval(() => {
                const remainingTime = parseInt(countdownTimer.innerText) - 1;
                countdownTimer.innerText = remainingTime;
                if (remainingTime <= 0) {
                    stopRecording();
                }
            }, 1000);

            recorder.addEventListener('dataavailable', event => {
                audioChunks.push(event.data);
            });

            recorder.addEventListener('stop', () => {
                clearInterval(countdownInterval);
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const formData = new FormData();
                formData.append('audio', audioBlob, 'recorded_audio.wav');

                fetch('/guess', {
                    method: 'POST',
                    body: formData
                })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data);
                        song_name = data["song_name"]
                        songName.innerText = song_name
                    })
                    .catch(error => {
                        console.error('Error uploading file:', error);
                    });

                const audioUrl = URL.createObjectURL(audioBlob);
                audioPlayer.src = audioUrl;
            });
        })
        .catch(error => {
            console.error('Error accessing microphone:', error);
        });
}

function stopRecording() {
    if (recorder && recorder.state === 'recording') {
        recorder.stop();
        startRecordingButton.disabled = false;
        startRecordingButton2.disabled = false;
        // stopRecordingButton.disabled = true;
    }
}
