from app.controller.users import userController
from app.controller.songs import songsController
from app.dao.songs import songsDAO
from flask import Blueprint, render_template,jsonify, Flask,request
from app.third_party.shazam.shazam_class import ShazamAPIClass
from app.third_party.musicai.musicai_class import MusicAIClass,download_youtube_video_as_mp3
from pprint import pprint
from flask_cors import CORS, cross_origin
import requests
import json


import asyncio
bp = Blueprint('main', __name__)
CORS(bp)

@bp.route('/users', methods=['GET'])
def getUsers():
    if request.method == 'GET':
        return userController().getAllUsers();
    else:
        return jsonify("Not Supported"), 405

@bp.route('/')
def index():
    return "Hello, Flask on Heroku!"
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

@bp.route('/process_song')
async def process_song():
    ytb_url = request.args.get('ytb_url')
    shazam_instance = ShazamAPIClass()
    musicai_instance = MusicAIClass()
    mp3 = download_youtube_video_as_mp3(ytb_url,'./app/third_party/shazam')
    recognize_song = await shazam_instance.recognize_track(mp3)
    checkSong = songsController().getSongChords(title=recognize_song[1])
    if checkSong is not None:
        return jsonify({'id':checkSong['song_id']})
    else:
        new_job = await musicai_instance.create_job('new job',mp3)
        print(new_job[1], recognize_song)
        chords = getChordJson(new_job[1]['chords'])
        bpm = new_job[1]['BPM']
        song_id = songsDAO().newSong(recognize_song[1], recognize_song[2], '', chords, bpm)
        # result = {'song': recognize_song, 'chords': chords, 'bpm': bpm}
        return jsonify({'id': song_id})

@bp.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        return userController().signup(request.json)
    else:
        return jsonify("Not Supported"), 405
    
@bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
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
    


