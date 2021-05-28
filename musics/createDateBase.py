import pandas as pd
import numpy as np
import csv
import os
from PIL import Image
import imagehash
import matplotlib.pyplot as plot
import librosa 
from pydub import AudioSegment
from tempfile import mktemp
import librosa.display
import numpy as np
import os
import pylab
import pandas as pd
import numpy as np
from scipy import signal



Song = []
spect_hash_list=[]
mfccHashList = []
melSpectroHashList=[]
chromaHashList=[]
print(os.listdir())
   
for filename in os.listdir():
    if filename.endswith(".mp3"):
        
        mp3_audio = AudioSegment.from_file((filename), format="mp3")[:60000]  # read mp3
        wavsong = np.array(mp3_audio.get_array_of_samples()).astype(np.float16)
        samplingFrequency = mp3_audio.frame_rate

        print(wavsong)

        sampleFreqs,sampleTime, colorMesh =signal.spectrogram(wavsong,fs=samplingFrequency)

        feature1= librosa.feature.mfcc(y=wavsong, sr=samplingFrequency)
        feature2= librosa.feature.melspectrogram(y=wavsong, sr=samplingFrequency,S=colorMesh)
        feature3= librosa.feature.chroma_stft(y=wavsong, sr=samplingFrequency,S=colorMesh)
        # lib.feature.melspectrogram(y=data,sr=rate,S=color)

        spect_image=Image.fromarray(colorMesh)
        new_image = Image.fromarray(feature1)
        new_image2=Image.fromarray(feature2)
        new_image3=Image.fromarray(feature3)

        spectHash=imagehash.phash(spect_image, hash_size=16).__str__()
        firstHash=imagehash.phash(new_image, hash_size=16).__str__()
        secondHash=imagehash.phash(new_image2, hash_size=16).__str__()
        thirdHash=imagehash.phash(new_image3, hash_size=16).__str__()

        Song.append(filename)

        spect_hash_list.append(spectHash)
        mfccHashList.append(firstHash)
        melSpectroHashList.append(secondHash)
        chromaHashList.append(thirdHash)
    



dict = {'song': Song, 'spectrogram hash':spect_hash_list,\
    'mfcc hash': mfccHashList,'mel spectrogram hash':melSpectroHashList,\
        'Chroma_stft hash':chromaHashList}
# dict = {'song': Song,'mfcc hash': mfccHashList,'mel spectrogram hash':melSpectroHashList,'Chroma_stft hash':chromaHashList}

df = pd.DataFrame(dict)
print(df.head)
df.to_csv('songsDataBase5.csv',index=False)