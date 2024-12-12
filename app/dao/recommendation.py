from app.config.db_config import dbconfig
import psycopg2
import json
import pandas as pd
from fuzzywuzzy import fuzz

class recommendationDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s " \
                         % (dbconfig['dbname'], dbconfig['user'], dbconfig['password'], dbconfig['dbhost'],
                            dbconfig['dbport'])

        self.conn = psycopg2.connect(connection_url)

    def getLikedSongs(self, uid):
        cursor = self.conn.cursor()
        query = 'select genre, artist from songs where song_id = (select song_id from liked_songs where user_id = %s)'
        cursor.execute(query, (uid,))
        songs = cursor.fetchall()
        return songs

    def getDataset(self):
        cursor = self.conn.cursor()
        query = 'select * from songdataset'
        cursor.execute(query)
        songDataset = cursor.fetchall()
        
        column_names = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(songDataset, columns=column_names)
        selected_features = ['track_name', 'track_genre', 'artists', 'popularity']
        df = df[selected_features]
        return df
    
    def getGenre(self, artist, title):
        cursor = self.conn.cursor()
        print(artist, title)
        query = 'select genre from songs where artist = %s and title = %s'
        cursor.execute(query, (artist, title,))
        songGenre = cursor.fetchone()
        print(songGenre)
        return songGenre
    
    def storeHistory(self, uid, title, artist, genre, popularity):
        try:
            with self.conn.cursor() as cursor:
                # Check if the song already exists for the given user
                check_query = '''
                    SELECT 1 
                    FROM recommendation_history 
                    WHERE user_id = %s AND title = %s AND artist = %s;
                '''
                cursor.execute(check_query, (uid, title, artist))
                result = cursor.fetchone()

                if result:  # If a row is found, the song already exists
                    return {"status": "exists", "message": "Song already exists in history"}

                # Insert the song if it doesn't exist
                insert_query = '''
                    INSERT INTO recommendation_history (user_id, title, artist, genre, popularity)
                    VALUES (%s, %s, %s, %s, %s);
                '''
                cursor.execute(insert_query, (uid, title, artist, genre, popularity))
            self.conn.commit()
            return {"status": "success", "message": "Song added to history"}
        except Exception as e:
            self.conn.rollback()
            return {"status": "error", "message": str(e)}
        
    def getHistory(self, uid):
        cursor = self.conn.cursor()
        query = 'select * from recommendation_history where user_id = %s'
        cursor.execute(query, (uid,))
        history = cursor.fetchall()
        
        return history
