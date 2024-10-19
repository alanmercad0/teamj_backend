import os
import yt_dlp
from moviepy.editor import AudioFileClip

def download_youtube_video_as_mp3(youtube_url, output_path):
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

# Example usage:
# youtube_url = 'https://www.youtube.com/watch?v=KwX1f2gYKZ4'
youtube_url='https://www.youtube.com/watch?time_continue=1&v=dIe4T14bkRQ&embeds_referring_euri=https%3A%2F%2Fonline.upr.edu%2F&embeds_referring_origin=https%3A%2F%2Fonline.upr.edu&source_ve_path=NzY3NTg&themeRefresh=1'

output_path = './'  # The directory where you want to save the mp3 file

download_youtube_video_as_mp3(youtube_url, output_path)
