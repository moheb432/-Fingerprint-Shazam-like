
import imagehash
from imagehash import hex_to_hash
from PIL import Image
import librosa as lib
from scipy import signal
import numpy as np

def get_features(data,color,rate):
   return[lib.feature.mfcc(y=data.astype('float64'),sr=rate),
  lib.feature.melspectrogram(y=data,sr=rate,S=color),
  lib.feature.chroma_stft(y=data,sr=rate,S=color)]
   



def PerHash(array):
   dataInstance = Image.fromarray(array)
   P_HASH= imagehash.phash(dataInstance, hash_size=16).__str__()
   return P_HASH



def per_spec_hashs(data,rate):
   hashes=[]
   fs,ts, image_data= signal.spectrogram(data,fs=rate)
   test_spect_hash=PerHash(image_data)
   hashes.append(test_spect_hash)
   for feat in get_features(data,image_data,rate):
       hashes.append(PerHash(feat))
  
   return hashes

# def mix(song1, song2 , per):
#     return (per*song1 + (1.0-per)*song2)

def mix(song1: np.ndarray, song2: np.ndarray,w) -> np.ndarray:
   
    return (w*song1 + (1.0-w)*song2)

    