# HUMmer: Song Identification Through Humming

HUMmer is a web-based application designed to identify songs from short humming snippets. By leveraging machine learning and sound recognition, the project helps users who struggle to recall song titles. It provides a user-friendly interface where users can record humming snippets, which are then processed and matched to a song in the database. This is my final project for CS 4701: Practicum in AI, which I took at Cornell in the fall 2023 semester. 

## Description

HUMmer's goal is to match short human humming segments to songs using a convolutional neural network (CNN). The application focuses on identifying songs from The Weeknd's discography, with an initial dataset of 17 songs. Users interact with the application by recording 10-second humming segments, which are converted into spectrograms and processed by the trained model. The predicted song is then displayed on the user interface. Additionally, users can upload new humming recordings to expand the training dataset, improving the model's accuracy and robustness. This project demonstrates the integration of sound recognition, data augmentation, and CNNs to provide a seamless and interactive experience for song identification.

## Getting Started

### Dependencies

To run HUMmer, ensure the following prerequisites are installed:
- **Python 3.x** with libraries:
  - `os`
  - `torch` (PyTorch)
  - `torchaudio`
  - `matplotlib`
  - `numpy`
  - `flask`
- Audio file processing tools such as `ffmpeg`

### Installing

1. Clone the repository.
2. Navigate to the project directory.
3. Install the required Python libraries.
4. Ensure `ffmpeg` is installed for audio file processing.
   
### Executing Program
1. Start the server:
   ```bash
   python3 app.py
2. Access the user interface by opening a web browser and going to http://localhost:5000/.
3. Record a 10-second humming snippet using the provided interface.
4. Submit the snippet to predict the song.
5. View the predicted song displayed on the interface.

## Authors
* Arnav Parashar
* Manvir Chahal
* Neeharika Kotimreddy
* Shashaank Aiyer

