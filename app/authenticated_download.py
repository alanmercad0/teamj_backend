from tools import *

def main():
    # Step 1: Authenticate the user
    credentials = authenticate_user()
    # print("Credentials",credentials)

    # Step 2: Fetch video details
    video_id = "f5hBQtDrxYs"  # Replace with the YouTube video ID
    video_details = get_video_details(video_id, credentials)

    # Step 3: Get the video's URL and pass it to yt-dlp
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    download_youtube_video_as_mp3(video_url,'.')

if __name__ == "__main__":
    main()
