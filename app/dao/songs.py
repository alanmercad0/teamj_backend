from app.config.db_config import dbconfig
import psycopg2
import json

class songsDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s " \
                         % (dbconfig['dbname'], dbconfig['user'], dbconfig['password'], dbconfig['dbhost'],
                            dbconfig['dbport'])

        self.conn = psycopg2.connect(connection_url)

    def getSongByTitle(self, title):
        cursor = self.conn.cursor()
        query = "select * from songs where title = %s"
        cursor.execute(query, (title, ))
        song = cursor.fetchone()
        return song

    def getSongById(self, id):
        cursor = self.conn.cursor()
        query = "select * from songs where song_id = %s"
        cursor.execute(query, (id, ))
        song = cursor.fetchone()
        return song
    
    def getSongChords(self, song_id):
        cursor = self.conn.cursor()
        query = 'select * from song_chords sc, songs s where sc.song_id = %s and sc.song_id = s.song_id'
        cursor.execute(query, (song_id, ))
        songChords = cursor.fetchone()
        return songChords
    
    def newSong(self, title, genre, artist, chords, bpm):
        cursor = self.conn.cursor()
        query = 'insert into songs (title, genre, artist, bpm) values (%s, %s, %s, %s) returning song_id'
        cursor.execute(query, (title, genre, artist, bpm)) 
        song_id = cursor.fetchone()
        self.conn.commit()

        song_id = song_id[0]
        query = 'insert into song_chords (song_id, song_time, chord_json) values (%s, %s, %s) returning chord_id'
        cursor.execute(query, (song_id, 'blah', json.dumps(chords))) 
        chord_id = cursor.fetchone()
        self.conn.commit()

        return song_id