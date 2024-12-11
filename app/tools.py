import yt_dlp,os,json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from google_auth_oauthlib.flow import Flow

from flask import redirect,url_for,session,request
import json
import webbrowser
import requests
from http.cookiejar import MozillaCookieJar


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# OAuth flow configuration
def get_flow():
    return Flow.from_client_secrets_file(
        'client_secrets.json',
        scopes=['https://www.googleapis.com/auth/youtube.readonly'],
        redirect_uri=url_for('main.oauth2callback', _external=True)
    )

async def authenticate_and_download(youtube_url,install_path,authorization_url,state):
    
    print("/n")
    print("/n")
    print("/n")
    print("Redirecting",redirect(authorization_url))
    print("/n")
    print("/n")
    print("/n")
   
    return ""


def save_cookies(credentials, cookies_file='cookies.txt'):
    # Extract the access token from the credentials
    access_token = credentials.token

    session = requests.Session()

   # Create a requests session to simulate a browser
    session = requests.Session()

    # Add the authorization header with the Bearer token
    session.headers.update({
        'Authorization': f'Bearer {access_token}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    })

    cookie_jar = MozillaCookieJar(cookies_file)
    for cookie in session.cookies:
        cookie_jar.set_cookie(cookie)

    # Write the cookies to the file
    cookie_jar.save(ignore_discard=True, ignore_expires=True)


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


# def authenticate_user():
#     # Scopes for YouTube access
#     scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

#     print("Line after scopes")

#     # Initialize the OAuth 2.0 flow
#     flow = InstalledAppFlow.from_client_secrets_file(
#         'client_secrets.json',  # Your client ID and secret file
#         scopes=scopes
#     )
#     print("OAuth 2.0 flow initialized")

#     # Get the user's credentials
#     credentials = flow.run_local_server(
#         port=8080,
#         prompt='consent',
#         success_message="Authentication successful! You may close this tab."
#     )
    
#     print("Local Server Running")

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
        'cookies_file':cookies_file,
        'verbose': True
    }

    print(type(cookies_file))

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