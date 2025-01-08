import librosa 
import random
import numpy as np
from scipy.io.wavfile import write
from pydub import AudioSegment

def change_pitch(file):
  audio  =AudioSegment.from_file(file) 
  for i in range(5):
    steps = random.uniform(-5,5)
    audio_shifted = librosa.effects.pitch_shift(audio, sr = 44100, n_steps = steps)
    scaled = np.int16(audio_shifted / np.max(np.abs(audio_shifted)) * 32767)
    write('test' + str(i) + '.wav', 44100, scaled)


change_pitch("./data/audio/best_friends/Best_friends-Manvir_2.wav")