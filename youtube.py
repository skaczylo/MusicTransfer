from ytmusicapi import YTMusic
from tqdm import tqdm
import ytmusicapi

INF = 10**6
CREDITS = "Support development: paypal.me/AdrianCarlosSkaczylo"

def filter(request_header):


    pos = request_header.find("accept:")
    if pos == -1:
        pos = request_header.find("Accept")
    if pos == -1:
        pos = request_header.find("accept")
    
    request_header = request_header[pos:]

    filtered_request = request_header.split("\n")

    if(len(filtered_request) == 50):
        
        new_request = []
        for index,head in enumerate(filtered_request):
            new_request.append(head)
            if index % 2 == 0:
                new_request.append(": ")
            else:
                new_request.append("\n")

        new_request = "".join(new_request)
        
        return new_request
            

    return request_header


class YouTubeMusicUser:

    def __init__(self):
        self.ytmusic = None
        self.page = None


    def sign_in(self,request_header):

        new_request_header = filter(request_header)
        
        ytmusicapi.setup(filepath="browser.json",headers_raw=new_request_header) #Creates browser.json
        self.ytmusic = YTMusic("browser.json")
    

    def get_total_liked_songs(self):
        """
        Returns the number of liked songs
        """

        liked_songs = self.ytmusic.get_liked_songs()

        return liked_songs["trackCount"]
    
    def get_liked_songs(self):
        """
        Return a list of songs where each song it's a dictionary :
            title   -   string
            artists -   [string]
        """

        liked_songs = self.ytmusic.get_library_songs(limit= INF)
        songs = []

        for song in liked_songs:

            new_song = {}
            new_song['title']= song['title']

            artists = []
            for artist in song['artists']:
                artists.append(artist['name'])

            new_song['artists'] = artists

            songs.append(new_song)
            

        return songs
    

    def get_playlist_info(self):
        """
        Returns:
            list of dict: Each dictionary contains:
                - name (str): The name of the playlist.
                - id (str): The identifier of the playlist.
        """

        playlists = self.ytmusic.get_library_playlists(limit=INF)
        playlist_info  = []
        
        for playlist in tqdm(playlists,desc="Fetching playlists",unit="playlist"):

            playlist_info.append({"name":playlist['title'],"id":playlist['playlistId']})
        
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

        playlist_info = self.ytmusic.get_playlist(playlistId= id,limit=INF)
        songs = playlist_info["tracks"]

        playlist = []

        for song in tqdm(songs,desc=f"Fetching songs from {playlist_info['title']}",unit="song"):
            new_song = {}
            new_song['title'] = song['title']
            new_song['artists'] = [artist['name'] for artist in song["artists"]]

            playlist.append(new_song)


        return playlist_info['title'], playlist
    

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

        results = self.ytmusic.search(query=query,
                                     filter="songs")
        
        if len(results) != 0:
            return results[0]['videoId']
        
        return None
    

    def save_song(self, song_id):
        
        self.ytmusic.rate_song(song_id, "LIKE")
        
    
    def create_playlist(self,name):
        playlist_id = self.ytmusic.create_playlist(title=name,
                                                   description=CREDITS,
                                                   privacy_status="PRIVATE") #New playlist
        return playlist_id
    

    def add_song_to_playlist(self,playlist_id,song_id):
        self.ytmusic.add_playlist_items(playlistId=playlist_id,
                                        videoIds=[song_id])
        

        
   
        


  

    



    



    