import yt_dlp,os,json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import json

def authenticate_and_download(youtube_url,install_path):
    credentials = authenticate_user()
    save_cookies(credentials=credentials)
    mp3 = download_youtube_video_as_mp3(youtube_url,install_path)
    return mp3


def save_cookies(credentials, cookies_file='cookies.txt'):
    # Extract the access token from the credentials
    access_token = credentials.token

    # Create a cookies file compatible with yt-dlp
    cookies = [
        {
            'domain': '.youtube.com',
            'path': '/',
            'secure': True,
            'expires': None,
            'name': 'Authorization',
            'value': f'Bearer {access_token}',
        }
    ]

    # Write cookies to a file in the correct format
    with open(cookies_file, 'w') as f:
        for cookie in cookies:
            f.write(f"{cookie['domain']}\tTRUE\t{cookie['path']}\t{str(cookie['secure']).upper()}\t{cookie['expires'] or 0}\t{cookie['name']}\t{cookie['value']}\n")
    print(f"Cookies saved to {cookies_file}")


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

    # Initialize the OAuth 2.0 flow
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secrets.json',  # Your client ID and secret file
        scopes=scopes
    )
    print("OAuth 2.0 flow initialized")

    # Get the user's credentials
    credentials = flow.run_local_server(port=8080,prompt='consent',success_message="Authentication successful! You may close this tab.")
    
    print("Local Server Running")

    # credentials = flow.credentials

    # print(credentials)
    return credentials



def download_youtube_video_as_mp3(youtube_url, output_path='./app/third_party/musicai',cookies_file='cookies.txt'):
    # Step 1: Download the YouTube video as audio
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'cookies_file':cookies_file
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