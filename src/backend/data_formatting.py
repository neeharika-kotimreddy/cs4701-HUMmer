from pydub import AudioSegment
from pydub.utils import make_chunks
from transforms import Converter
from PIL import Image
import pandas as pd
import os


audio_path = "../../data/audio/"
specto_path = "../../data/spectograms/"

m4a_loc = audio_path + "originals/m4a/"
wav_loc = audio_path + "originals/wav/"

song_to_class = {"married": 0, "gasoline": 1, "love_me" : 2, 
                 "best_friends": 3, "dont_break_my_heart": 4,
                 "here_we_go_again": 5, "less_than_zero": 6, 
                 "out_of_time": 7, "sacrifice": 8, 
                 "someone_else": 9, "starry_eyes": 10, 
                 "take_my_breath": 11, "i_feel_it_coming": 12, 
                  "save_your_tears": 13, "starboy": 14, 
                   "die_for_you": 15, "blinding_lights": 16 }

class_to_song = {v: k for k, v in song_to_class.items()}

def convert_to_wav(no_repeats=False):
    for audio in os.listdir(m4a_loc):
        if ".m4a" not in audio:
            continue
        wav_name = audio[:-4] + ".wav"
        if no_repeats and wav_name in os.listdir(wav_loc):
            continue
        print(audio)
        mp3_file = AudioSegment.from_file(m4a_loc + audio)
        mp3_file.export(wav_loc + wav_name, format="wav")


def split_into_chunk(filename, secs=10, no_repeats=False):
    folder = audio_path + filename.split("-")[0].lower() 
    name = filename[:-4]
    print("Folder: " + folder)
    if not os.path.exists(folder):
        os.mkdir( folder)

    if no_repeats:
        for audio_name in os.listdir(folder):
            if name in audio_name:
                return

    song = AudioSegment.from_file(wav_loc + filename)
    length = secs * 1000
    chunks = make_chunks(song,length)  

    for i, chunk in enumerate(chunks): 
        chunk_name = folder+ '/' + name + "_{0}.wav".format(i) 
        print ("exporting", chunk_name) 

        if len(chunk) < length:
            chunk = chunk + AudioSegment.silent(duration=length - len(chunk))
            
        chunk.export(chunk_name, format="wav")


def convert_folder_to_spectograms(no_repeats=False):
    for folder in os.listdir(audio_path):
        if folder == "originals" or not os.path.isdir(audio_path + folder):
            continue
        
        if folder not in os.listdir(specto_path):
            os.makedirs(specto_path + folder)
        
        folder = folder + "/"
        for audio in os.listdir(audio_path + folder):
            img_name = specto_path + folder + audio[:-4] + ".jpg"
            
            if no_repeats and os.path.isfile(img_name):
                continue

            img = convert_to_spectogram(audio_path + folder + audio)
            print("Image: " + img_name)
            Image.fromarray(img, 'RGB').save(img_name)


def convert_to_spectogram(audio_file_path):
    aud = Converter.open(audio_file_path)
    spect = Converter.spectro_gram(aud)
    return Converter.convert_to_color_image(spect)

          
def get_data_df():
    data = {"path": [], "song": []}
    for song in os.listdir(specto_path):
        for spect in os.listdir(specto_path + "/" + song):
            data["path"].append(specto_path  + song + "/" + spect)
            data["song"].append(song_to_class[song])
    
    dataset = pd.DataFrame(data)
    dataset.to_csv("dataset.csv")
    return dataset

if __name__ == "__main__":
    no_repeats=True
    convert_to_wav(no_repeats=no_repeats)
    for filename in os.listdir(wav_loc):
        split_into_chunk(filename, no_repeats=no_repeats)
    convert_folder_to_spectograms(no_repeats=no_repeats)
