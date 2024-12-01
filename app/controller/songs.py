
from flask import jsonify
from app.dao.songs import songsDAO
import json

class songsController:

    def getSongByTitle(self, title):
        # title = json['title']
        if title:
            dao = songsDAO()
            song = dao.getSongByTitle(title)
            if song:
                result = {}
                result['song_id'] = song[0]
                result['title'] = song[1]
                result['genre'] = song[2]
                result['artist'] = song[3]
                result['bpm'] = song[4]
                return jsonify(result)
            else:
                return jsonify(Error="Not Found"), 404
        else:
            return jsonify(Error="Malformed post request"), 400
        
    def getSongById(self, id):
        # title = json['title']
        if id:
            dao = songsDAO()
            song = dao.getSongById(id)
            if song:
                result = {}
                result['song_id'] = song[0]
                result['title'] = song[1]
                result['genre'] = song[2]
                result['artist'] = song[3]
                result['bpm'] = song[4]
                return jsonify(result)
            else:
                return jsonify(Error="Not Found"), 404
        else:
            return jsonify(Error="Malformed post request"), 400
        

    def getSongChords(self, title = False, id = False):
        # title = json['title']
        dao = songsDAO()
        
        if title:
            song = dao.getSongByTitle(title)
            if song is not None:
                songChords = dao.getSongChords(song[0])
                # print(songChords)
                chords = json.loads(songChords[3])
                result = {}
                result['song_id'] = song[0]
                result['chords'] = chords
                result['bpm'] = song[4]
                return result
            else:
                return None
        elif id:
            song = dao.getSongById(id)
            if song is not None:
                songChords = dao.getSongChords(song[0])
                print(song)
                chords = json.loads(songChords[3])
                result = {}
                result['song_id'] = song[0]
                result['chords'] = chords
                result['bpm'] = song[4]
                result['title'] = song[1]
                result['artist'] = song[3]
                return result
            else:
                return None
        else:
            return jsonify(Error="Malformed post request"), 400