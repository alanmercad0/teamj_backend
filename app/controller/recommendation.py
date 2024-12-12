from flask import jsonify
from app.dao.recommendation import recommendationDAO
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class recommendationController:

    def getHistory(self, uid):
        dao = recommendationDAO()
        return jsonify(dao.getHistory(uid))
    
    def storeRecommendationHistory(self, uid, title, artist, genre, popularity):
        dao = recommendationDAO()
        return jsonify(dao.storeHistory(uid, title, artist, genre, popularity))


    def getRecommendation(self, title, artist, user):
        if user == 'No User':
            dao = recommendationDAO()
            df = dao.getDataset()
            genre = dao.getGenre(artist, title)

            input_song = [title, genre[0], artist]
            recommended_songs = self.get_similar_songs(input_song, df)
            recommended_songs = self.recommend_songs(recommended_songs, title, genre[0], artist)

            return recommended_songs.to_json()
        
        else:
            dao = recommendationDAO()
            df = dao.getDataset()
            likedSongs = dao.getLikedSongs(user)
            genre = dao.getGenre(artist, title)

            input_song = [title, genre[0], artist]
            recommended_songs = self.get_similar_songs_adv(input_song, df, likedSongs)
            recommended_songs = self.recommend_songs(recommended_songs, title, genre[0], artist)

            return recommended_songs.to_json()
        

    def get_similar_songs(self, song_features, df, top_n=100):
        track_name, track_genre, artists = song_features

        df = df.fillna({
            'track_name': '',
            'track_genre': '',
            'artists': ''
        })

        def similarity_score(row):
            score = 0

            # Check track name similarity
            if isinstance(row['track_name'], str):
                if track_name.lower() == row['track_name'].lower():
                    score += 3
                elif track_name.lower() in row['track_name'].lower() or row['track_name'].lower() in track_name.lower():
                    score += 1

            # Check track genre similarity
            if isinstance(row['track_genre'], str):
                if track_genre.lower() == row['track_genre'].lower():
                    score += 1
                elif track_genre.lower() in row['track_genre'].lower() or row['track_genre'].lower() in track_genre.lower():
                    score += 1

            # Check artists similarity
            if isinstance(row['artists'], str):
                if artists.lower() == row['artists'].lower():
                    score += 3
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
        return recommended_songs[['track_name', 'track_genre', 'artists', 'similarity']]
    
    def get_similar_songs_adv(self, song_features, df, liked_songs, top_n=100):
        track_name, track_genre, artists = song_features

        # Fill missing values
        df = df.fillna({
            'track_name': '',
            'track_genre': '',
            'artists': ''
        })

        def similarity_score(row):
            score = 0

            # Check track name similarity
            if isinstance(row['track_name'], str):
                if track_name.lower() == row['track_name'].lower():
                    score += 3
                elif track_name.lower() in row['track_name'].lower() or row['track_name'].lower() in track_name.lower():
                    score += 1

            # Check track genre similarity
            if isinstance(row['track_genre'], str):
                if track_genre.lower() == row['track_genre'].lower():
                    score += 1
                elif track_genre.lower() in row['track_genre'].lower() or row['track_genre'].lower() in track_genre.lower():
                    score += 1

            # Check artists similarity
            if isinstance(row['artists'], str):
                if artists.lower() == row['artists'].lower():
                    score += 3
                elif artists.lower() in row['artists'].lower() or row['artists'].lower() in artists.lower():
                    score += 1
            
            # Add extra points if the song's genre and artist match any in the liked_songs list
            for liked_genre, liked_artist in liked_songs:
                if row['track_genre'].lower() == liked_genre.lower() or row['artists'].lower() == liked_artist.lower():
                    score += 1

            return score

        df['similarity'] = df.apply(similarity_score, axis=1)
        df_filtered = df[
            ~((df['track_name'].str.lower() == track_name.lower()) &
            (df['artists'].str.lower() == artists.lower()))
        ]

        df_filtered = df_filtered.drop_duplicates(subset=['track_name'])
        recommended_songs = df_filtered.sort_values(by='similarity', ascending=False).head(top_n)
        return recommended_songs[['track_name', 'track_genre', 'artists', 'similarity']]

    def recommend_songs(self, df, track_name, track_genre, artist, num_recommendations=5):
        selected_features = ['track_name', 'track_genre', 'artists']
        df = df[selected_features]
        
        # Fill missing values with empty strings
        df = df.fillna('')
        
        # Filter out rows with missing or empty track_name or artists
        df = df[(df['track_name'].str.strip() != '') & (df['artists'].str.strip() != '')]
        
        new_song = {'track_name': track_name, 'track_genre': track_genre, 'artists': artist}
        new_song_df = pd.DataFrame([new_song])
        df = pd.concat([df, new_song_df], ignore_index=True)

        df['combined_features'] = df['track_name'] + ' ' + df['track_genre'] + ' ' + df['artists']
        df['combined_features'] = df['combined_features'].astype(str)
        
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(df['combined_features']) 
        cosine_similarities = cosine_similarity(tfidf_matrix)
        
        new_song_index = len(df) - 1
        similar_songs = list(enumerate(cosine_similarities[new_song_index]))
        sorted_similar_songs = sorted(similar_songs, key=lambda x: x[1], reverse=True)
        unique_similar_songs = []
        seen_songs = set()
        
        for i in sorted_similar_songs[1:]:
            track_name = df['track_name'][i[0]]
            if track_name not in seen_songs:
                unique_similar_songs.append(i)
                seen_songs.add(track_name)
            if len(unique_similar_songs) >= num_recommendations:
                break

        similar_songs_df = pd.DataFrame({
            'track_name': [df['track_name'][i[0]] for i in unique_similar_songs],
            'track_genre': [df['track_genre'][i[0]] for i in unique_similar_songs],
            'artists': [df['artists'][i[0]] for i in unique_similar_songs]
        })
        
        return similar_songs_df
