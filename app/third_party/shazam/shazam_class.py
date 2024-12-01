import asyncio
from shazamio import Shazam, Serialize

class ShazamAPIClass():
    def __init__(self):
        self.shazam = Shazam()
    async def recognize_track(self, song_mp3_url) -> str:
        search = await self.shazam.recognize(song_mp3_url)  # rust version, use this!
        if(len(search['matches']) == 0): return 'None found'
        song = [search['track']['key'],search['track']['title'],search['track']['genres']['primary'],search['track']['artists']]
        artist_id = song[3][0]['adamid']
        about_artist = await self.shazam.artist_about(artist_id)
        song[3] = about_artist['data'][0]['attributes']['name']
        return song
 


    
    


 
