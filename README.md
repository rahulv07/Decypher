# Decypher :clapper:

## Description:
Decypher is a subtitle file generator for videos. It is made using **Python** and **VOSK**, an open source speech recognition engine.

## How to use:
1. Clone this repository or download the zip folder and extract the files into your system.
2. **cd** into the code repository
3. Install the required libraries using the **requirements.txt** file

       pip install requirements.txt
       
4. Install **FFMPEG**, for audio processing. Run the below command in the terminal

       sudo apt-get install ffmpeg
        
5. Download the **VOSK** speech recognition model. To download the model, run the below commands in the terminal

       wget https://alphacephei.com/kaldi/models/vosk-model-small-en-us-0.15.zip
       unzip vosk-model-small-en-us-0.15.zip
       mv vosk-model-small-en-us-0.15 model
   or download it as [zip file](http://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip), extract it and rename the extracted folder as *model*.

6. Now you are ready to transcribe the video file. Run the main.py file, by passing the path of the video as argument.

       python main.py {video path}
       
   Example:
   
       python main.py ~/Videos/stevejobs.mp4
       
7. After transcribing, the subtitle file will be located in the code folder.

>Note: The transcribing process will take some time and depends upon the length of the video. 

## Supported formats:
**Video** - mp4 format

**Subtitle file** - srt format

### Credits:
Referred some code from [**Autosub**](https://github.com/abhirooptalasila/AutoSub), an open source project.
