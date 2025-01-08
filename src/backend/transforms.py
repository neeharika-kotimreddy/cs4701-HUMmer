import torch
import torchaudio
from torchaudio import transforms
import matplotlib.pyplot as plt
import numpy as np


class Converter():
  def open(audio_file):
    sig, sr = torchaudio.load(audio_file)
    return (sig, sr)
  
  def spectro_gram(aud, n_mels=64, n_fft=1024, hop_len=None):
    sig,sr = aud
    top_db = 80

    # spec has shape [channel, n_mels, time], where channel is mono, stereo etc
    spec = transforms.MelSpectrogram(sr, n_fft=n_fft, hop_length=hop_len, n_mels=n_mels)(sig)

    # Convert to decibels
    spec = transforms.AmplitudeToDB(top_db=top_db)(spec)
    return (spec)
  
  def convert_to_color_image(spect):
    spect = spect.permute(1, 2, 0)
    spect = spect.squeeze()
    minimum = torch.min(spect)
    maximum = torch.max(spect)

    spect = (spect - minimum) / (maximum - minimum)
    cmap = plt.get_cmap()
    return (cmap.__call__(spect)[:, :, :3] * 255).astype(np.uint8)