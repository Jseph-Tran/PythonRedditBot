# PythonRedditBot
A Python bot that automates short-form content creation with customizable parameters. Users can specify the background video, script length, subreddit source, and other settings. The bot pulls submissions from Reddit, generates voice-over narrations, overlays captions, and adds a video background, streamlining content creation with full automation.

## Features
- User-friendly terminal interface for initializing file paths, specifying parameters such as subreddit, script length, sort order, and tracking key information.
- Pulls scripts from Reddit based on a specified subreddit.
- Generates a voice-over narration for the Reddit post.
- Generates auto-captions for the Reddit video.
- Combines voice-over, auto-captions, and a randomly selected background video to generate the video

## How to use
1. **Import Scripts**: Add the Reddit scripts to the file.
2. **Import Background Video and Music**: Provide the background video and music files for the final video.
3. **Reddit Initializer**: The program will connect the file paths between the different scripts based on the user input.
4. **Run the Bot**: Execute `main.py` to start the bot and generate the TikTok video.

## Example

The following JSON illustrates the tracking data created and managed by the Reddit Initializer, including configuration details, submission data, and related paths:

```
{
    "SystemInformation": {
        "key": {
            "Client_ID": "fake_client_id_12345",
            "Secret_Key": "fake_secret_key_67890"
        },
        "login_info": {
            "username": "fake_username",
            "password": "fake_password"
        },
        "headers": {
            "User-Agent": "fake_user_agent_string",
            "Authorization": "bearer fake_token_string_abcdef123456"
        },
        "parms": {
            "t": "month",
            "limit": 100,
            "over_18": "true"
        },
        "length_submission": {
            "min_length": 200,
            "max_length": 400
        },
        "query": {
            "sort": "new",
            "subreddit": "FakeSubreddit",
            "speaker": "Microsoft George Desktop"
        }
    },
    "AudioProcessingInformation": {
        "font": "C:/fake_path/Anton-Regular.ttf",
        "model": "advanced"
    },
    "directory_data": {
        "RequestInitalizer": "C:/fake_path/Reddit Request",
        "AudioProcessing": "C:/fake_path/Audio&Script Python",
        "SpeakingAudio": "C:/fake_path/Speaking Audio",
        "CommentFrame": "C:/fake_path/Comment Frame",
        "main.py": "C:/fake_path/Reddit TikTok video",
        "MusicAssets": "C:/fake_path/Music Assets",
        "VideoAsset": "C:/fake_path/Video Assets",
        "FinishedVideoStorage": "C:/fake_path/Finished Tik Toks"
    },
    "story_data": {
        "title": "This is a fake example of a Reddit post.",
        "selftext": "This is a fake example of a Reddit post.",
        "id": "fake_id_12345"
    },
    "submission_id": [
        "fake_submission_1",
        "fake_submission_2",
        "fake_submission_3",
        "fake_submission_4",
        "fake_submission_5"
    ],
    "duration_data": {
        "title": 4.50,
        "transcript": 90.00
    },
    "index": 1
}
```
## Example
[Video](TikTokVid3.mp4)
## Improvements
- Create a real user interface using Tkinter or html/css
- Generate video in multiple different languages
- Automating uploading process (web apps opened on Selenium are typically banned)
