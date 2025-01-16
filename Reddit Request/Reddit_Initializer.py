import json
import os


def initialize_data():
    base_directory = r'C:/Users/FakeUser/Documents'

    try:
        # Attempt to open the file and read it as JSON
        with open(os.path.join(base_directory, "RedditMakerData.json"), "r") as f:
            json.load(f)  # Try to load the JSON content
            print("Data Retrieved successfully.")

    except (FileNotFoundError, json.JSONDecodeError):
        # Catch the error if file doesn't exist or JSON is invalid
        print()
        print("Welcome to this script. This script will be able to generate you a reddit story TikTok video. We will need to initialize some things before starting")
        print("These are the necessary libraries/modules you will need to install: ")
        print()
        print("""
            pyttsx3
            ffmpeg
            Selenium and some type of webdriver
            Whisper
            MoviePy
              """)
        print()
        print("Please input data for your reddit bot")
        
        Client_ID = input("Client_ID: ")
        Secret_Key = input("Secret_Key: ")
        key = {"Client_ID " : Client_ID,
               "Secret_Key" : Secret_Key }

        username = input("Username: ")
        password = input("Password: ")
        login_info = {
            "username" : username,
            "password" : password
        }

        user_agent = input("user_agent: ")
        headers = {
            "User-Agent":user_agent
        }

        time = input("Enter time of submission: ")
        limit = int(input("Enter limit of returned submissions: "))
        over_18 = input("NSFW (True/False): ").lower()

        params = {
            "t" : time,
            "limit" : limit,
            "over_18": over_18 ,
        
        }

        min_length = int(input('Min length of submission: '))
        max_length = int(input('Max length (chars) of submission: '))

        length_submission = {

            "min_length" : min_length, 
            "max_length" : max_length
        }
        
        sort = input('Enter sort type: ')
        subreddit = input('Enter subreddit name: ')
        speaker = input('Enter pyttsx3 voice: ')

        
        query = {
            'sort' : sort,
            'subreddit' :  subreddit,
            'speaker' : speaker
        }

            
    
        SystemInformation = {
            "key": key,
            "login_info": login_info, 
            "headers" : headers,
            "parms" : params,
            "length_submission" :  length_submission,
            'query' : query 

        }

        font = input("Enter file path to your caption font: ")
        model = input("Enter Whisper model: ")

        AudioProcessingInformation = {
            "font": font,
            "model" : model
        }

        print("Now, please state directories where key scripts and assets will be located on your device:")
        data1 = input("Reddit_Initializer.py, Reddit_Request.py, RedditMakerData.json: " )
        data2 = input("Audio_Processing.py: ")
        data3 = input("Speaking Audio: ")
        data4 = input("Comment Frame script and related assets: ")
        data5 = input("Main.py: ")
        data6 = input("Music assets: ")
        data7 = input("Video assets: ")
        data8 = input("Finished TikTok Video Storage: ")

        directory_data = {
            'RequestInitalizer' : data1,
            'AudioProcessing' : data2,
            'SpeakingAudio' : data3,
            'CommentFrame' : data4,
            'main.py' : data5,
            'MusicAssets' : data6,
            'VideoAsset': data7,
            'FinsihedVideoStorage': data8 
        }

        story_data = {
        }

        submission_id = []
        duration_data = {}

        index = 0

        RedditMakerData = {
            'SystemInformation' :   SystemInformation,
            'AudioProcessingInformation' : AudioProcessingInformation,
            'directory_data' :  directory_data,
            'story_data' : story_data,
            'submission_id' : submission_id,
            'duration_data' :  duration_data,
            'index' : index
        }

        with open("RedditMakerData.json", "w") as f:
            json.dump(RedditMakerData, f, indent = 4) # Try to load the JSON content
            print("Data loaded successfully.")

def reset(file):
    if file.strip().lower() == "story":
        print("Cannot perform action at this currentt moment")
    if file.strip().lower() == "ids":
        with open("RedditMakerData.json", "r") as f:
            data = json.load(f)

        data["submission_id"] = []  # Reset the list
        
        with open("RedditMakerData.json", "w") as f:
            json.dump(data, f, indent=4)

        print("Done!")
        
if __name__ == "__main__":
   initialize_data()


