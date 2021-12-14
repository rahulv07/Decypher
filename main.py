import filter
import argparse
import os
import split
import decipher
import datetime


parser = argparse.ArgumentParser()
parser.add_argument("path",help = "Enter the video file path")
args = parser.parse_args()

video_file_name = args.path

base_directory = os.getcwd()
output_directory = os.path.join(base_directory, "output")
audio_directory = os.path.join(base_directory, "audio")
video_prefix = os.path.splitext(os.path.basename(video_file_name))[0]
audio_file_name = os.path.join(audio_directory, video_prefix + ".wav")

print("Extracting the audio...")
filter.extractAudio(video_file_name,audio_file_name)

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

print(f"Number of audio segments: {len(audiofiles)}")

decipher.isModelPresent()

#Transcribing
print("Transcribing the audio...")

subtitle = open("subtitle.txt","a")

for i,file in enumerate(audiofiles):
    file = os.path.join(audio_directory,file)
    interval = file.split(os.sep)[-1][:-4].split("_")[-1].split("-")
    fromTime = decipher.get_timestamp_string(datetime.timedelta(seconds=float(interval[0])))
    toTime = decipher.get_timestamp_string(datetime.timedelta(seconds=float(interval[1])))
    subtitle.write(str(i+1)+"\n")
    subtitle.write(fromTime+" --> "+toTime+"\n")
    subtitle.write(decipher.transcribe(file)+"\n\n")

subtitle.close()