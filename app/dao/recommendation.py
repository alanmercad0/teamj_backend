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