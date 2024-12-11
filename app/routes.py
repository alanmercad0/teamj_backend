from app.controller.users import userController
from app.controller.songs import songsController
from app.controller.recommendation import recommendationController
from app.dao.songs import songsDAO
from flask import Blueprint, render_template,jsonify, Flask,request, redirect, url_for, session
from app.third_party.shazam.shazam_class import ShazamAPIClass
from app.third_party.musicai.musicai_class import MusicAIClass
from app.tools import *
from pprint import pprint
from mutagen.mp3 import MP3
from flask_cors import CORS, cross_origin
import requests
import json
import os
import asyncio
bp = Blueprint('main', __name__)
CORS(bp)
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('NEXT_PUBLIC_FRONT_URL')


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

credenciales = None


@bp.route('/users', methods=['GET'])
def getUsers():
    if request.method == 'GET':
        return userController().getAllUsers();
    else:
        return jsonify("Not Supported"), 405

@bp.route('/')
def index():
    if 'credentials' in session:
        return "You are authenticated!"
    else:
        return '<a href="/start_auth">Authenticate</a>'
@bp.route('/test')
def test():
    return "This is a test route"

def getChordJson(download_link):
    if not download_link:
        raise ValueError("No download link provided")

    # Step 2: Download the JSON file
    json_file_response = requests.get(download_link)
    if json_file_response.status_code == 200:
        # Step 3: Process the JSON content
        try:
            json_content = json_file_response.json()  # Load directly as JSON
            return json_content  # Return the processed content for further use
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON content")
    else:
        raise ValueError("Failed to download the JSON file")
    
@bp.route('/start_auth')
def start_auth():
    flow = get_flow()
    authorization_url, state = flow.authorization_url()

    # Save state in the session
    session['state'] = state

    # Redirect the user to the authorization URL
    return redirect(authorization_url)

@bp.route('/auth_status')
def auth_status():
    global credenciales
    if credenciales is not None:
        return jsonify({"status": "success", "message": "Authentication successful"})
    else: 
        return jsonify({"status": "failure", "message": "Authentication unsuccessfull"})
        


@bp.route('/oauth2callback')
def oauth2callback():
    flow = get_flow()

    if 'state' not in session or session['state'] != request.args.get('state'):
        session['auth_status'] = {"status": "error", "message": "State mismatch"}

    # try:
        # Complete the OAuth flow
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials

    # Save credentials and status
    global credenciales
    credenciales = credentials
    session['auth_status'] = {"status": "success", "message": "Authentication successful"}

    return redirect(f"{url}/")





@bp.route('/process_song')
async def process_song():
    if credenciales is None:
        print("User not authenticated. Please authenticate first")
        return jsonify(Error='User not authenticated. Please authenticate first.'), 401
    ytb_url = request.args.get('ytb_url')
    shazam_instance = ShazamAPIClass()
    musicai_instance = MusicAIClass()

    
    credentials = credenciales
    print("Credenciales",type(credentials))
    save_cookies(credentials=credentials)
    mp3 = download_youtube_video_as_mp3(ytb_url,'./app/third_party/shazam')
    
    print(f"MP3 file: {mp3}")

    checking_mp3 = MP3(mp3)
    # print(f"Checking MP3 object: {mp3}")

    length_in_seconds = checking_mp3.info.length
    minutes, seconds = divmod(length_in_seconds, 60)
    # print(f"Length of the MP3 file: {int(minutes)} minutes and {int(seconds)} seconds")
    if minutes <= 4:
        recognize_song = await shazam_instance.recognize_track(mp3)
        print(recognize_song)
        checkSong = songsController().getSongChords(title=recognize_song[1])
        # print(checkSong)
        # print(recognize_song)
        if recognize_song == 'None found':
            return jsonify(Error='No sound found from URL')
        else:
            checkSong = songsController().getSongChords(title=recognize_song[1])
            if checkSong is not None:
                os.remove(mp3)
                return jsonify({'id':checkSong['song_id']})
            else:
                new_job = await musicai_instance.create_job('new job',mp3)
                # print(new_job[1], recognize_song)
                chords = getChordJson(new_job[1]['chords'])
                bpm = new_job[1]['BPM']
                song_id = songsDAO().newSong(recognize_song[1], recognize_song[2], recognize_song[3], chords, bpm)
                os.remove(mp3)
                # result = {'song': recognize_song, 'chords': chords, 'bpm': bpm}
                return jsonify({'id': song_id})
    else:
        result = f"Invalid Song: Song must be less than 4:00 minutes. Song Length {minutes}:{seconds}"
    return result

@bp.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        print(request.json)
        return userController().signup(request.json)
    else:
        return jsonify("Not Supported"), 405
    
@bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        print(request.json)
        return userController().login(request.json)
    else:
        return jsonify("Not Supported"), 405
    
@bp.route('/getSongByTitle', methods=['GET'])
def getSongByTitle():
    if request.method == 'GET':
        title = request.args.get('title')
        return songsController().getSongByTitle(title) 
    else:
        return jsonify("Not Supported"), 405
    
@bp.route('/getSongChords')
def getSongChords():
    title = request.args.get('title')
    id = request.args.get('id')
    if title is not None:
        return songsController().getSongChords(title=title) 
    if id is not None:
        return songsController().getSongChords(id=id) 
    return jsonify(error='missing info'), 400
    
@bp.route('/addToHistory', methods=['POST'])
def addToHistory():
    if request.method == 'POST':
        return userController().addToHistory(request.json)
    else:
        return jsonify("Not Supported"), 405 
    
@bp.route('/getHistory')
def getHistory():
    id = request.args.get('id')
    if id is not None:
        return userController().getHistory(id) 
    return jsonify(error='missing info'), 400

@bp.route('/getLikedSongs')
def getLikedSongs():
    id = request.args.get('id')
    if id is not None:
        return userController().getLikedSongs(id) 
    return jsonify(error='missing info'), 400

@bp.route('/likeSong', methods=['POST'])
def likeSong():
    if request.method == 'POST':
        return userController().likeSong(request.json)
    else:
        return jsonify("Not Supported"), 405 
    
@bp.route('/dislikeSong', methods=['POST'])
def dislikeSong():
    if request.method == 'POST':
        return userController().dislikeSong(request.json)
    else:
        return jsonify("Not Supported"), 405 
    
@bp.route('/checkIfLiked')
def checkIfLiked():
    id = request.args.get('id')
    song_id = request.args.get('song_id')
    if id is not None:
        return userController().checkIfLiked(id, song_id) 
    return jsonify(error='missing info'), 400
@bp.route('/getRecommendations')
def getRecommendations():
    title = request.args.get('title')
    artist = request.args.get('artist')

    return recommendationController().getRecommendation(title, artist)

