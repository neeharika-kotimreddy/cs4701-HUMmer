from pydub import AudioSegment
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import os


file_path = "audio/originals/m4a/"
save_path = "audio/originals/wav/"

for audio in os.listdir(file_path):
     mp3_file = AudioSegment.from_file(file_path + audio)
     wav_name = audio[:-4] + ".wav"
     wav_file = mp3_file.export(save_path + wav_name, format="wav")

# mp3_file = AudioSegment.from_file("bday2.m4a")
# wav_file = mp3_file.export("bday2.wav", format="wav")
# files = ["output.wav", "output2.wav", "output3.wav"]
# # files = ["test.wav"]
# files = ["audacity.wav", "bday2.wav"]
# fig, axs = plt.subplots(2)
# i = 0
# for file in files:
#     sample_rate, audio_data = wavfile.read(file)
#     print(sample_rate)
#     print(audio_data.shape)
#     x = np.array(range(len(audio_data)))
#     axs[i].plot(x, audio_data)
#     i += 1
# plt.show()