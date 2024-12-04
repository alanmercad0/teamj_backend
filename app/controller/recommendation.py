from flask import jsonify
from app.dao.recommendation import recommendationDAO
import json
import pandas as pd
from fuzzywuzzy import fuzz
from googleapiclient.discovery import build

class recommendationController:

    def getRecommendation(self, title, artist):
        dao = recommendationDAO()
        df = dao.getDataset()
        genre = dao.getGenre(artist, title)

        input_song = [title, genre[0], artist]
        recommended_songs = self.get_similar_songs(input_song, df)
        recommended_songs = recommended_songs.sort_values(by='popularity', ascending=False)

        # recommended_songs = self.add_youtube_links(recommended_songs)

        return recommended_songs.to_json()
        


    def get_similar_songs(self, song_features, df, top_n=11):
        track_name, track_genre, artists = song_features

        df = df.fillna({
            'track_name': '',
            'track_genre': '',
            'artists': ''
        })

        def similarity_score(row):
            score = 0

            if isinstance(row['track_name'], str):
                similarity = fuzz.ratio(track_name.lower(), row['track_name'].lower()) / 100
                score += int(similarity * 5)

            if isinstance(row['track_genre'], str):
                if track_genre.lower() == row['track_genre'].lower():
                    score += 5
                elif track_genre.lower() in row['track_genre'].lower() or row['track_genre'].lower() in track_genre.lower():
                    score += 1

            if isinstance(row['artists'], str):
                if artists.lower() == row['artists'].lower():
                    score += 5
                elif artists.lower() in row['artists'].lower() or row['artists'].lower() in artists.lower():
                    score += 1

            return score

        df['similarity'] = df.apply(similarity_score, axis=1)

        df_filtered = df[
            ~((df['track_name'].str.lower() == track_name.lower()) &
            (df['artists'].str.lower() == artists.lower()))
        ]

        df_filtered = df_filtered.drop_duplicates(subset=['track_name'])

        recommended_songs = df_filtered.sort_values(by='similarity', ascending=False).head(top_n)
        return recommended_songs
    
    def add_youtube_links(self, df):
        df['Youtube Links'] = df.apply(
            lambda row: self.youtubeLink(row['track_name'], row['artists']), axis=1
        )
        return df

        
    def youtubeLink(self, title, artist, max_results=5):
        API_KEY = 'AIzaSyBLFzYgN7H1PAnJEyiwbSjcYCtP0dGYbUA'
        youtube = build('youtube', 'v3', developerKey=API_KEY)

        query = f'{title} {artist}'
        
        request = youtube.search().list(
            q=query,
            part='snippet',
            type='video',
            maxResults=1
        )
        
        response = request.execute()

        video_urls = []
        for item in response['items']:
            video_id = item['id']['videoId']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            video_urls.append(video_url)

        return video_urls[0]