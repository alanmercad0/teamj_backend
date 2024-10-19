import asyncio
from shazamio import Shazam

class ShazamAPIClass():
    def __init__(self):
        self.shazam = Shazam()
    async def recognize_track(self, song_mp3_url) -> str:
        search = await self.shazam.recognize(song_mp3_url)  # rust version, use this!
        song = [search['track']['key'],search['track']['title'],search['track']['genres']['primary'],search['track']['artists']]
        return song
 


    
    


 
