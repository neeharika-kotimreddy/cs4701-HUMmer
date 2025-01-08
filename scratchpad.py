
from data.transforms import AudioUtil
import matplotlib.pyplot as plt
from pydub import AudioSegment 
from pydub.utils import make_chunks
import numpy as np
import os
from PIL import Image


# cmap = plt.get_cmap()
# vals = np.zeros((11, 3))
# vals[:, 0] = np.linspace(0, 1, num=11)
# vals[:, 1] = np.linspace(0, 1, num=11)*0.4+0.2
# vals[:, 2] = np.linspace(0, 1, num=11)*0.8

# print(vals)
# test = (cmap.__call__(vals) *255).astype(np.uint8)[:, :, :3]
# print(test)

# Image.fromarray(test, "RGB").save("small.jpg")
# plt.imshow(test)
# plt.show()

aud = AudioUtil.open("testing/output2.wav")
aud = AudioUtil.rechannel(aud, 2)
original = AudioUtil.spectro_gram(aud)

# img = AudioUtil.convert_to_image(spect)
# print(img.shape)
# print(img)
# print(spect.shape)

plt.figure()
f, axarr = plt.subplots(2,1) 
axarr[0].imshow(original)
# axarr[0].title("original")

spect = AudioUtil.spectro_augment(original)
# spect = spect.permute(1, 2, 0)
# spect = spect.squeeze()

# # b = (spect - np.min(spect))/np.ptp(spect)
# b = AudioUtil.convert_to_image(spect)
# print(b)
# plt.imshow( b )
# plt.title("Custom lin norm") 
# plt.show()

# Image.fromarray(img, "RGB").save("testing.jpg")

axarr[1].imshow(spect)
# axarr[1].title("augmented")
plt.show()


def split_into_chunk(filename, src, secs=15):
    folder = "audio/" + filename.split("-")[0].lower() 
    name = filename[:-4]
    print("Folder: " + folder)

    song = AudioSegment.from_wav(src + filename)
    length = secs * 1000
    chunks = make_chunks(song,length)  
    for i, chunk in enumerate(chunks): 
        chunk_name = './' +folder+ '/' + name + "_{0}.wav".format(i) 
        print ("exporting", chunk_name) 
        if len(chunk) < length:
            chunk = chunk + AudioSegment.silent(duration=length - len(chunk))
            
        chunk.export(chunk_name, format="wav")

# wav_path = "audio/originals/wav/"
# for filename in os.listdir(wav_path):
#     split_into_chunk(filename, wav_path)