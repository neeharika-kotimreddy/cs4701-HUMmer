from flask import Flask, request, jsonify, send_from_directory
from main import get_name_of_song, get_songs, trim_audio
import time

app = Flask(__name__)

# Serve the frontend files
@app.route('/')
def serve_frontend():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)

@app.route('/guess', methods=['POST'])
def guess():
    if 'audio' not in request.files:
        return jsonify({'error': 'No file part'})

    audio_file = request.files['audio']
    print(audio_file)
    if audio_file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Save the file to a desired location
    audio_file.save('uploaded_audio.wav')
    trim_audio('uploaded_audio.wav')
    song_name = get_name_of_song("uploaded_audio.wav")
    return jsonify({'success': 'File uploaded successfully', 'song_name': song_name})

@app.route('/retry', methods=['GET'])
def retry():
    trim_audio('uploaded_audio.wav')
    song_name = get_name_of_song("uploaded_audio.wav")
    return jsonify({ 'song_name': song_name})


@app.route('/upload', methods=['POST'])
def upload():
    if 'audio' not in request.files:
        return jsonify({'error': 'No file part'})
    print("here")
    audio_file = request.files['audio']
    song_name = request.form['song_name'].capitalize()

    if audio_file.filename == '':
        return jsonify({'error': 'No selected file'})
    print(audio_file)
    song_name = song_name + "-" + str(int(time.time()))
    audio_file.save('../../data/audio/originals/wav/' + song_name + ".wav")
    return jsonify({'success': 'File uploaded successfully', 'song_name': song_name})


@app.route('/get_songs', methods=['GET'])
def songs():
    return jsonify({'songs': get_songs()}) 

if __name__ == '__main__':
    app.run(port = 5001, debug=True)
