import filter
import argparse
import os
import split
import decipher
import datetime
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("path",help = "Enter the video file path")
args = parser.parse_args()

videoPath= args.path
    
base_directory = os.getcwd()
output_directory = os.path.join(base_directory, "output")
audio_directory = os.path.join(base_directory, "audio")
video_prefix = os.path.splitext(os.path.basename(videoPath))[0]
audio_file_name = os.path.join(audio_directory, video_prefix + ".wav")

if not os.path.isfile(videoPath):
    raise Exception("Video file does not exist")

if not os.path.isdir(audio_directory):
    os.makedirs(audio_directory)

print("Extracting the audio...")
filter.extractAudio(videoPath,audio_file_name)

print("Processing the audio...")
filter.preProcess(audio_file_name)


#Splitting the audio
print("Splitting the audio...")
audiofiles=split.splitAudio(audio_file_name,audio_directory)
audiofiles.remove(os.path.basename(audio_file_name))

#Remove non related audiofiles
audiofiles_ = []
for filename in audiofiles:
    if filename.startswith(video_prefix):
        audiofiles_.append(filename)
audiofiles = audiofiles_
del(audiofiles_)

decipher.isModelPresent()

#Transcribing
print("Transcribing the audio...")

subtitle = open(f"{video_prefix}.srt","a")

for i in enumerate(tqdm(audiofiles)):
    count = i[0]
    file = i[1]
    file = os.path.join(audio_directory,file)
    interval = file.split(os.sep)[-1][:-4].split("_")[-1].split("-")
    fromTime = decipher.get_timestamp_string(datetime.timedelta(seconds=float(interval[0])))
    toTime = decipher.get_timestamp_string(datetime.timedelta(seconds=float(interval[1])))
    subtitle.write(str(count+1)+"\n")
    subtitle.write(fromTime+" --> "+toTime+"\n")
    subtitle.write(decipher.transcribe(file)+"\n\n")

subtitle.close()