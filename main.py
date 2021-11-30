import filter
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("path",help = "Enter the video file path")
args = parser.parse_args()

videoName = args.path

audioName = filter.extractAudio(videoName)
filter.preProcess(audioName)

