import os
import json
import pyttsx3
import srt
from datetime import timedelta
from moviepy import AudioFileClip, TextClip, VideoFileClip
import whisper

class AudioProcessing:
    def __init__(self, RedditData):
        self.datafile = RedditData

        with open (RedditData, "r") as f:
            self.data = json.load(f)

        self.basedirectory = self.data["directory_data"]["AudioProcessing"] 
        self.story = self.data["story_data"]  #file path to story
        self.export_directory = self.data["directory_data"]["SpeakingAudio"]
        self.model = whisper.load_model(self.data["AudioProcessingInformation"]["model"])
        self.font = self.data["AudioProcessingInformation"]["font"]
        self.maxlength = 859.2
 
    def get_audio(self, name, datatype):
        textdata=self.story[datatype]
        print(f'Loaded {name} for Audio Processing')
      
        engine = pyttsx3.init()  # Creates engine object for speech
        voices = engine.getProperty('voices')  # List of all available voices
        engine.setProperty('rate', 200)

        for voice in voices:
            if self.data['SystemInformation']['query']['speaker'] in voice.name:  # Find the desired voice
                engine.setProperty('voice', voice.id)
                print("Begin Generating Audio...")
                break
        
        export_file_path = os.path.join(self.export_directory, f'{name}_Audio.wav')
        print(f'Saving {name} audio to: {export_file_path}')
        engine.save_to_file(textdata, export_file_path)
        engine.runAndWait()  # Must excute this method 

        print(f"Generated Audio!")
        return export_file_path 
        
    def get_audio_duration(self, name, export_file_path):
        audio = AudioFileClip(export_file_path)  #get export file path
        total_seconds = audio.duration
        with open(self.datafile, 'r') as f:
            file = json.load(f)
            
        file["duration_data"][name] = total_seconds  #add the dic entry 

        with open(self.datafile, 'w') as f:  #update the informatio
            json.dump(file, f, indent=4)

        print("Obtain audio duration for editing use")
    
    def get_text_width(self, text):
        subtitleclip = TextClip(
            font=self.font,
            text=text,
            font_size=110,
            color="#FFFFFF",
            stroke_width=5,
            stroke_color="#000000",
            duration=0.01
        )
        width, height = subtitleclip.size
        return width

    def srt_convert(self, export_file_path):
        print('Loading Whisper data...')
        result = self.model.transcribe(export_file_path)  # transcribe the audio
        list_segments = []
        for segment in result['segments']:  # open segments data
            list_segments.append({
                "start": segment["start"],  # parse the data and append the list of dictionaries to list_segments variable
                "end": segment["end"],
                "text":segment["text"],
            })
        print('Starting Conversion to SRT...')
        
        #needed variables 
        subs = [] 
        time_change = 0
        current_time = 0
        index = 1  
        max_width = 859.2  
        current_size = 0
        content = [] 
        
        for segment in list_segments:
            segment_duration = segment['end'] - segment['start']
            segment_length = len("".join(segment["text"].split()))
            for word in segment["text"].split():
                word_width = self.get_text_width(word)
                if current_size + word_width <= max_width:      # Word fits in the current subtitle
                    content.append(word)
                    word_duration = (len(word) / segment_length) * segment_duration
                    time_change += word_duration
                    current_size += word_width

                else:
                    subs.append(srt.Subtitle(
                            index=index,
                            start=timedelta(seconds=current_time),
                            end=timedelta(seconds=current_time + time_change),
                            content=" ".join(content)
                        ))
                    index += 1  
                    current_time += time_change 
                    time_change = 0   

                    content = [word]
                    word_duration = (len(word) / segment_length) * segment_duration
                    time_change += word_duration
                    current_size = word_width

        # Add the last subtitle for the remaining words
        if content:
            subs.append(srt.Subtitle(
                    index=index,
                    start=timedelta(seconds=current_time),
                    end=timedelta(seconds=current_time + time_change),
                    content=" ".join(content)
                ))
                   
               
        with open(os.path.join(self.basedirectory, "output.srt"),  "w", encoding="utf-8") as f:
            f.write(srt.compose(subs))
        print("Converted to SRT")

    def run_AudioProcessing(self):
        export_file_pathTitle = self.get_audio("title", "title")
        self.get_audio_duration("title",  export_file_pathTitle)
        export_file_pathTranscript = self.get_audio("transcript", "selftext")
        self.get_audio_duration("transcript",  export_file_pathTranscript)
        self.srt_convert(export_file_pathTranscript)

if __name__ == "__main__":
    AudioProcessing(r'C:/Users/Joseph/Documents/vscode/Reddit Project/Reddit Request/RedditMakerData.json').run_AudioProcessing()