import yt_dlp,os,json

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

def json_response(status_code,message):
    response = {
        "code":status_code,
        "message":message
    }
    return json.dumps(response)