from vosk import Model, KaldiRecognizer, SetLogLevel
import os
import wave
import json
from contextlib import contextmanager
import sys

SetLogLevel(-1)

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout
            
def isModelPresent():
    if not os.path.exists("model"):
        print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit (1)
    

def get_timestamp_string(timedelta):
    # timedelta may be eg, '0:00:14'
    if '.' in str(timedelta):
        timestamp = "0" + str(timedelta).split(".")[0] + ','+ str(timedelta).split(".")[-1][:3]
    else:
        timestamp = "0" + str(timedelta) + ',' + "000"
    return timestamp


def transcribe(audioPath):
    wf = wave.open(audioPath, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        exit (1)

    with suppress_stdout():
        model = Model("model")
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)

        nFrames = wf.getnframes()
        data = wf.readframes(nFrames)
        a = rec.AcceptWaveform(data)
        ans = rec.FinalResult()
        
    ansDict = json.loads(ans)
    return ansDict["text"]


