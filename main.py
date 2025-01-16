import os
from moviepy import VideoFileClip, ImageClip, TextClip, AudioFileClip, concatenate_audioclips, CompositeVideoClip, concatenate_videoclips, CompositeAudioClip
import random
import json
import math
import pysrt
import pandas as pd
import sys

class TikTokGenerator:
    def __init__(self, RedditData):
        
        try:
            with open(RedditData, "r") as f:
                self.data = json.load(f)
                self.datafile = RedditData
        except (FileNotFoundError, json.JSONDecodeError):
            print("Please pass in RedditMakerData file")

        # Generate assets before updating the data
        self.base_directory = self.data['directory_data']['main.py']
        self.generate_assets()  # generate the assets first

        # Update the data after generating assets
        self.datafile = RedditData
        with open(RedditData, "r") as f:
            self.data = json.load(f)

        self.duration_title = self.data['duration_data']["title"]
        self.duration_transcript = self.data['duration_data']["transcript"]
        self.duration_total =  self.duration_title + self.duration_transcript 
        print(f'Title: {self.duration_title}, Transcript: {self.duration_transcript}, Total: {self.duration_total}')
        self.duration_total = self.duration_title + self.duration_transcript + 1        #give a addition second for breathing room at end of video

 
    
    def generate_assets(self):
        
        pythonscripts_directories = [
            self.data['directory_data']['RequestInitalizer'],
            self.data['directory_data']['AudioProcessing'],
            self.data['directory_data']['CommentFrame']
        ]
        for directory_path in pythonscripts_directories:
            sys.path.append(directory_path)
            
        import Reddit_Initializer 
        Reddit_Initializer.initialize_data()
        import Reddit_Request
        Reddit_Request.RedditAPIClient(self.datafile).run_RedditRequest()
        import AudioProcessing
        AudioProcessing.AudioProcessing(self.datafile).run_AudioProcessing()
        import CommentFrameMaker
        CommentFrameMaker. CommentFrameMaker(self.datafile).createCommentFrame()

    def get_video_clip(self):
        file_path_video = self.data['directory_data']['VideoAsset']
        background_video_file = random.choice(os.listdir(file_path_video))           #select a video file out of the choices 
        background_video_path = os.path.join(file_path_video, background_video_file) #create full path to the video
        background_video = VideoFileClip(background_video_path)                      #store the video clip in a varible 
        max_duration = background_video.duration - self.duration_total
        starting_duration = random.choice(range(0, math.ceil(max_duration)))         #ensures start time are different among each video
        ending_duration = starting_duration + self.duration_total
        background_video = background_video.subclipped(starting_duration, ending_duration)   #cut background_video to fit in with duration of story 
        print(f'Background Video: {background_video_file}, Start: {starting_duration}, End: {ending_duration}')
        return background_video
    
    

    def get_music(self):
        file_path_music = self.data['directory_data']['MusicAssets']
        background_music_file = random.choice(os.listdir(file_path_music))
        background_music_path = os.path.join(file_path_music, background_music_file)
        video =  VideoFileClip(background_music_path)
        background_music = video.audio.with_volume_scaled(0.25)                       #extract and lower the audio 
        background_music_duration = background_music.duration 

        #Find how many copies of the music we need 
        count = 1
        current_duration = background_music_duration   
        while current_duration < self.duration_total:
            current_duration += background_music_duration  
            print(f"Current Duration: {current_duration}")
            count += 1

        music_clips = []
        for i in range(1, count+1):
            music_clips.append(background_music)

        final_music_clip = concatenate_audioclips(music_clips)
        final_music_clip = final_music_clip.subclipped(0, self.duration_total)  #Remove excess music             
        print(f'Music: {background_music_file }, Count: {count}, Start: {0}, End: {self.duration_total}')
        return final_music_clip
    
    def get_speaking_audio(self):
        file_path_title = os.path.join(self.data["directory_data"]["SpeakingAudio"],'title_Audio.wav')
        file_path_transcript = os.path.join(self.data["directory_data"]['SpeakingAudio'],'transcript_Audio.wav')
        title_audio = AudioFileClip(file_path_title)
        transcript_audio = AudioFileClip(file_path_transcript)
        speaking_audio = concatenate_audioclips([title_audio, transcript_audio])
        print("Obtained Speaking Audio")
        return speaking_audio

    @staticmethod
    def convert_to_seconds(time_str):
        # Convert SubRipTime to a string
        time_str = str(time_str)
        td = pd.to_timedelta(time_str.replace(",", "."))
        return td.total_seconds()

        
    def obtain_subtitles(self):
        file_path_subtitles = os.path.join(self.data["directory_data"]['AudioProcessing'], 'output.srt')
        subs = pysrt.open(file_path_subtitles, encoding='utf-8')
        
        combined_clip = []
        font = 'Anton-Regular.ttf'
        
        for sub in subs:  #iterate throught subs, create a subtitle clip based on SRT
            duration=TikTokGenerator.convert_to_seconds(sub.end - sub.start)        #Convert to seconds (float), this ensure it fits TextClip agrument parameters             
            subtitleclip = TextClip(
                font = font ,
                text = sub.text,
                font_size= 110,
                color= "#FFFFFF",
                stroke_width = 5 ,
                stroke_color="#000000",
                duration = duration
            )
            combined_clip.append(subtitleclip)          #Add each iteration to the list of final_clip
        subtitles = concatenate_videoclips(combined_clip)   #compose all text clips into one
        print("Obtained Subtitles")                 
        return subtitles 

    def get_commentframe(self):
        commentFrame_path = os.path.join(self.data["directory_data"]['CommentFrame'], 'CommentFrame.png') 
        commentFrame= ImageClip(commentFrame_path, duration=self.duration_title).resized(2)    #make a litte bit larger
        print("Obtained comment Frame") 
        return commentFrame
    
    def make_TikTok(self, videoAsset, musicAsset, speaking_audio, subtitles, commentFrame):
        # Position comment frame and subtitles in the center
        commentFrame = commentFrame.with_position(("center", "center"))
        subtitles = subtitles.with_position(("center", "center")).with_start(self.duration_title)
        TikTokVid = CompositeVideoClip([videoAsset, commentFrame, subtitles])
        combined_audio = CompositeAudioClip([musicAsset, speaking_audio])     # Combine videoAsset, commentFrame, and subtitles into one final clip
        TikTokVid = TikTokVid.with_audio(combined_audio).with_fps(30)       # Set audio for the final video
        print("Creating Video...")
        TikTokVid.write_videofile("TikTokVid.mp4")    # Write the final video to a file
    
    def move_tiktok(self):

        while True:
            user_answer = input("Ready to move file? (Yes/Wait): ").strip().lower()
            if user_answer == "yes":
                current_file_path = os.path.join(self.base_directory, "TikTokVid.mp4")      
                new_directory = self.data["directory_data"]['FinsihedVideoStorage']

                index = self.data['index']
                new_file_path = os.path.join(new_directory, f'TikTokVid{index}.mp4')
                os.rename(current_file_path, new_file_path)
                print(f"File renamed and moved to {new_file_path}")

                index +=1

                self.data['index'] = index
                with open (self.datafile, 'w') as f:
                    json.dump(self.data, f, indent=4)
                
                break
            elif user_answer == 'wait':
                print("Waiting..")
            else:
                print("Invalid input. Please enter 'Yes', 'No', or 'Wait'.")

    def create_tiktok(self):
        video_asset = self.get_video_clip()
        music_asset = self.get_music()
        subtitles = self.obtain_subtitles()
        comment_frame = self.get_commentframe()
        speaking_audio = self.get_speaking_audio()
        self.make_TikTok(video_asset, music_asset, speaking_audio, subtitles, comment_frame)
        self.move_tiktok()

if __name__ == "__main__":
    TikTokGenerator(r'C:/Users/Joseph/Documents/vscode/Reddit Project/Reddit Request/RedditMakerData.json').create_tiktok()




