import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
from data_formatting import convert_to_spectogram
import torch
from model import Net
from PIL import Image
from torchvision import transforms
from pydub import AudioSegment


# from PIL import Image
# from torchvision.io import read_image



device_info = sd.query_devices(kind='input')
input_channels = device_info['max_input_channels']
freq = 44100
duration = 10

# recording = sd.rec(int(duration * freq), 
#                    samplerate=freq, channels=min(input_channels, 2))

# print("Begin Humming Now")
# sd.wait()
# wv.write("recording.wav", recording, freq, sampwidth=2)
# print("Converting image")

mp3_file = AudioSegment.from_file("shank-test.m4a")
mp3_file.export("shank-test.wav", format="wav")

img = convert_to_spectogram("shank-test.wav")
Image.fromarray(img, 'RGB').save("test.jpg")

img = torch.from_numpy(img).float().permute(2, 1, 0).unsqueeze(0)

# img_path = "../data/spectograms/married/Married-Manvir_5.jpg"
# img = Image.open(img_path)
# transform = transforms.Compose( [
#             transforms.ToTensor(),
#             ])
# img = transform(img)
# img = img.unsqueeze(0)

print(img.shape)
# img = read_image("test.jpg")
print("loading model")
path = "../models/test3.pth"
net = Net()
net.load_state_dict(torch.load(path))
net.eval()
outputs = net(img)
print(outputs)
_, predicted = torch.max(outputs.data, 1)
print(predicted)