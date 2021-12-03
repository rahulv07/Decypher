import subprocess
import numpy as np
import wave
import math
import contextlib
import os

def extractAudio(videoName):
    fileName,fileExt = os.path.splitext(os.path.basename(videoName))
    command = f"ffmpeg -i {videoName} -ab 128k -ac 1 -ar 16000 -vn -y {fileName}.wav"
    try:
        subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return f"{fileName}.wav"
    except Exception as e:
        print("Error: "+str(e))
        exit(1)
   
def channelize(raw_bytes, n_frames, n_channels, sample_width, interleaved = True):
    if sample_width == 1:
        dtype = np.uint8
    elif sample_width == 2:
        dtype = np.int16
    else:
        raise ValueError("Only supports 8 and 16 bit audio formats.")

    channels = np.fromstring(raw_bytes, dtype=dtype)

    if interleaved:
        channels.shape = (n_frames, n_channels)
        channels = channels.T
    else:
        channels.shape = (n_channels, n_frames)

    return channels
    
   
def movAvgFilter(fs,audioData):
    fc = 3000
    fr = fc/fs
    windowSize = int(math.sqrt(0.196196 + fr**2)/fr)
    cumsum = np.cumsum(np.insert(audioData,0,0))
    filteredAudio = (cumsum[windowSize:] - cumsum[:-windowSize]) / windowSize
    return filteredAudio.astype(audioData.dtype)

def bandPassFiltering():
    command = 'ffmpeg -i avgFiltered.wav -af "highpass=f=300, lowpass=f=3000" -y bandFiltered.wav'
    subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove("avgFiltered.wav")
    
def removeStaticNoise():
    command = 'sox bandFiltered.wav -n noiseprof noise.prof'
    subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    command = 'sox bandFiltered.wav noiseLess.wav noisered noise.prof 0.19'
    subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove("bandFiltered.wav")
    os.remove("noise.prof")
    
def amplifyAudio(audioName):
    command = f'ffmpeg -i noiseLess.wav -filter:a "volume=2" -y {audioName}'
    subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove("noiseLess.wav")
    
def preProcess(audioName):
    with contextlib.closing(wave.open(audioName,'rb')) as spf:
        fs = spf.getframerate()
        ampWidth = spf.getsampwidth()
        nChannels = spf.getnchannels()
        nFrames = spf.getnframes()
        
        # Extract Raw Audio from multi-channel Wav File
        signal = spf.readframes(nFrames*nChannels)
        spf.close()
        
        #Seperating the audio into multiple channels
        channels = channelize(signal, nFrames, nChannels, ampWidth, True)

        #Low pass filtering using moving average filter
        filtered = movAvgFilter(fs,channels[0])
        wav_file = wave.open("avgFiltered.wav", "w")
        wav_file.setparams((1, ampWidth, fs, nFrames, spf.getcomptype(), spf.getcompname()))
        wav_file.writeframes(filtered.tobytes('C'))
        wav_file.close()
        
    bandPassFiltering()
    removeStaticNoise()
    amplifyAudio(audioName)
    