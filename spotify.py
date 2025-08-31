import spotipy
import os
from tqdm import tqdm
from spotipy.oauth2 import SpotifyPKCE
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

SCOPES = [
        "playlist-read-private",
        "playlist-read-collaborative",
        "playlist-modify-private",
        "playlist-modify-public",
        "user-library-read",
        "user-library-modify"
    ]

REDIRECT_URI = 'http://127.0.0.1:8888/callback'

CREDITS = "Support development: paypal.me/AdrianCarlosSkaczylo"


load_dotenv()

class SpotifyUser:
    
    def __init__(self):

        self.auth_manager = None
        self.access_token = None
        self.sp = None #Spotify API client

     
    def sign_in(self):

        try:
            """
            Gets the access token for the app
            If the code is not given and no cached token is used, an authentication window will be shown to the user to get a new code.
            """

            self.access_token = self.auth_manager.get_access_token(check_cache=False)
            self.sp = spotipy.Spotify(auth=self.access_token,
                                      oauth_manager = self.auth_manager)
            
            return True
    
        except spotipy.exceptions.SpotifyException:
            print("Something went wrong with the authentication")
            return False
        

    def change_client_id(self,id):
        self.auth_manager = SpotifyPKCE(client_id = id,
                                        redirect_uri=REDIRECT_URI,
                                        scope= " ".join(SCOPES),
                                        open_browser=True)
        

  
    def get_total_liked_songs(self):
        
        """
        Returns the number of liked songs
        """
        library = self.sp.current_user_saved_tracks(limit=50, offset=0)
        total = library['total']
        return total 

    def get_liked_songs(self):
        
        """
        Returns a list of songs where each song it's a dictionary :
            title   -   string
            artists -   [string]
        """

        liked_songs = []
        offset = 0
        library = self.sp.current_user_saved_tracks(limit=50, offset=offset)
        total = library['total']

        pbar = tqdm(total=total, desc="Getting liked songs", unit="song")

        while True:

            for song in library['items']:
                new_song = {}
                new_song['title'] = song['track']['name']

                artists = [artist['name'] for artist in song['track']['artists']]
                new_song['artists'] = artists
                
                liked_songs.append(new_song)
                pbar.update(1)  

            offset += 50
            if offset >= total:
                break

            
            library = self.sp.current_user_saved_tracks(limit=50, offset=offset)

        pbar.close()
        return liked_songs
    


    def get_playlist_info(self):

        """
        Returns:
            list of dict: Each dictionary contains:
                - name (str): The name of the playlist.
                - id (str): The identifier of the playlist.
        """

        playlist_info = []

    
        offset = 0
        
        playlists = self.sp.current_user_playlists(limit=50, offset=offset)
        total = playlists['total']

        pbar = tqdm(total=total, desc="Fetching playlists",unit="playlist")

        while True:
            for playlist in playlists['items']:

                new_playlist = {}
                new_playlist['name'] = playlist['name']
                new_playlist['id'] = playlist['id']
                playlist_info.append(new_playlist)
                pbar.update(1)

            offset += 50
            if offset >= total:
                break

            playlists = self.sp.current_user_playlists(limit=50, offset=offset)

        pbar.close()
        
        return playlist_info
    

    def get_playlist(self,id):
        """
        Returns the name of the playlist and all its songs for the given id.

        Returns:
            tuple: A pair containing:
                - name (str): The name of the playlist.
                - songs (list of dict): A list of songs, where each song is represented by:
                    - title (str): The title of the song.
                    - artists (list of str): The artists of the song.
        """
        
        offset = 0

        name = self.sp.playlist(id)['name']
        playlist_info = self.sp.playlist_items(id, offset=offset, limit=50)


        tracks = playlist_info['items']
        total_songs = playlist_info['total']

        playlist = []

        pbar = tqdm(total=total_songs, desc=f"Getting songs from {name}", unit="song")
        while True:

            for track in tracks:
                new_song = {}
                new_song['title'] = track['track']['name']
                new_song['artists'] = [artist['name'] for artist in track['track']['artists']]
                playlist.append(new_song)
                pbar.update(1)
            
            offset += 50
            if offset >= total_songs:
                break

        return name, playlist
        

    def find_song(self,song):
        """
        Search for a song on YouTube Music using a title and a list of artists.

        Args:
            song (dict): Dictionary with two keys:
                - title (str): The title of the song.
                - artists (list[str]): A list of artist names.

        Returns:
            The song id (str)
        """


        query = f'{song["title"]}'

        for artist in song['artists']:
            query += f' {artist}'

        results = self.sp.search(q=query, type="track", limit=5)
        results = results['tracks']['items']

        if len(results) != 0:
            return results[0]['id']

        return None
    
    def save_song(self, song_id):
        self.sp.current_user_saved_tracks_add(tracks=[song_id])

    def create_playlist(self,name):
        user_id = self.sp.current_user()["id"]

        new_playlist = self.sp.user_playlist_create(user=user_id,
                                                    name=name,
                                                    public="False",
                                                    description=CREDITS)

        return new_playlist['id']

    def add_song_to_playlist(self,playlist_id,song_id):
        self.sp.playlist_add_items(playlist_id,[song_id])


    

    
    
   
