import yt_dlp,os,json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from config.client_config import web
import json




def get_video_details(video_id, credentials):
    # Build the YouTube API client
    youtube = build("youtube", "v3", credentials=credentials)

    # Fetch video details
    response = youtube.videos().list(
        part="snippet,contentDetails",
        id=video_id
    ).execute()

    # Extract video metadata
    video_details = response["items"][0]["snippet"]
    print(f"Title: {video_details['title']}")
    return video_details


def authenticate_user():
    # Scopes for YouTube access
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

    print("Line after scopes")

    # Convert to JSON
    with open('client_config.json', 'w') as json_file:
        json.dump(web, json_file, indent=4)

    # Initialize the OAuth 2.0 flow
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_config.json',  # Your client ID and secret file
        scopes=scopes
    )
    print("OAuth 2.0 flow initialized")

    # Get the user's credentials
    credentials = flow.run_local_server(port=8080,prompt='consent',success_message="Authentication successful! You may close this tab.")
    
    print("Local Server Running")

    # credentials = flow.credentials

    # print(credentials)
    return credentials



def download_youtube_video_as_mp3(youtube_url, output_path='./app/third_party/musicai'):
    # Step 1: Download the YouTube video as audio
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=True)
        audio_file = ydl.prepare_filename(info_dict)
        mp3_file = os.path.splitext(audio_file)[0] + ".mp3"
    
    print(f"Downloaded and converted: {mp3_file}")
    return mp3_file

def refresh_token(credentials):
    # Refresh the OAuth 2.0 token if expired
    if credentials.expired:
        credentials.refresh()
    return credentials

def json_response(status_code,message):
    response = {
        "code":status_code,
        "message":message
    }
    return json.dumps(response)