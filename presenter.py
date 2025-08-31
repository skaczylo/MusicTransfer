import view
import youtube
import spotify
import threading

MESSAGE = (
    "✅ Done!\n\n"
    "Thank you for using MusicTransfer! I hope it has been helpful.\n\n"
    "If you found it useful and would like to support the development of the app, "
    "I would greatly appreciate any contribution you consider appropriate. "
    "Your support helps me continue improving MusicTransfer.\n\n"
    "You can donate via PayPal here:  paypal.me/AdrianCarlosSkaczylo\n\n"
    "Thank you again for your support and feedback!"
)


class Presenter:

    def __init__(self,gui,spotify_user,ytmusic_user):

        self.gui = gui
        self.spotify_user =spotify_user
        self.ytmusic_user = ytmusic_user

        self.source = None
        self.destination = None

        self.playlists = [] #Playlists ids to transfer from the source
    
        self.transfer_liked_songs = True

        #SELECT SOURCE FRAME
        self.gui.frames["SelectSource"].spotify_button.configure(command= self.spotify_source)
        self.gui.frames["SelectSource"].ytMusic_button.configure(command= self.youtube_source)


        #SPOTIFY SIGN IN FRAME
        self.gui.frames["SpotifySignIn"].sign_in_button.configure(command= self.spotify_sign_in)

        #YOUTUBE SIGN IN FRAME
        self.gui.frames["YoutubeSignIn"].sign_in_button.configure(command= self.youtube_sign_in)

        #DATA SELECTION
        self.gui.frames["DataSelection"].confirm_button.configure(command= self.confirm_selection)



    def change_frame(self,frame):
        frame = self.gui.frames[frame]
        frame.lift()

    def spotify_source(self):
        self.source = self.spotify_user
        self.destination = self.ytmusic_user
        self.change_frame("SpotifySignIn")

    def youtube_source(self):
        self.source = self.ytmusic_user
        self.destination = self.spotify_user
        self.change_frame("YoutubeSignIn")


    def confirm_selection(self):


        frame = self.gui.frames["DataSelection"]
        checkboxes = frame.checkboxes



        checked_playlists = []

        #Transfer liked songs
        if checkboxes[0].get() == 1:
            self.transfer_liked_songs = True
               
        else:
            self.transfer_liked_songs = False

        #Playlists
        for index, checkbox in enumerate(checkboxes):

            if checkbox.get() == 1 and index >=1 : #Checkedd
              checked_playlists.append(self.playlists[index-1])


        self.playlists = checked_playlists
        

        if self.source is self.ytmusic_user:
            self.change_frame("SpotifySignIn")
        else:
            self.change_frame("YoutubeSignIn")


    def youtube_sign_in(self):

        #Sign in 
        frame = self.gui.frames["YoutubeSignIn"]
        request_header = frame.request_header.get("0.0", "end-1c") #get request header
        self.ytmusic_user.sign_in(request_header)

        #Display data
        if self.source is self.ytmusic_user:

            self.playlists = self.ytmusic_user.get_playlist_info() 
            total_saved_songs = self.ytmusic_user.get_total_liked_songs()

            self.gui.frames["DataSelection"].update_frame(self.playlists,total_saved_songs)
            self.change_frame("DataSelection")
        
        else:
            self.change_frame("ProgressFrame")
            threading.Thread(target=self.start_transfer, daemon=True).start()
    

 
    def spotify_sign_in(self):


        #Sign in 
        client_id = self.gui.frames["SpotifySignIn"].client_id.get("0.0", "end-1c") #gets de client id
        self.spotify_user.change_client_id(client_id)
        self.spotify_user.sign_in()

        #Display data
        if self.source is self.spotify_user:
            

            self.playlists = self.spotify_user.get_playlist_info()
            total_saved_songs = self.spotify_user.get_total_liked_songs()


            self.gui.frames["DataSelection"].update_frame(self.playlists,total_saved_songs)
            self.change_frame("DataSelection")
            
        else:
            self.change_frame("ProgressFrame")
            threading.Thread(target=self.start_transfer, daemon=True).start()



    def start_transfer(self):
        frame = self.gui.frames["ProgressFrame"]
        self.transfer_data(fetching_callback=frame.update_label,
                           progress_callback=frame.update_progress)
        
        frame.update_label(text=MESSAGE)
        frame.progress.set(1)

    def transfer_data(self,fetching_callback = None,progress_callback = None):
        
        #Count items
        total_items = 0
        if self.transfer_liked_songs:
            total_items += self.source.get_total_liked_songs()

        for playlist in self.playlists:
            _ , songs = self.source.get_playlist(playlist['id'])
            total_items += len(songs)

            if fetching_callback:
                fetching_callback(f"Fetching data...{playlist['name']}")


        items_done = 0
        #Transfer liked songs
        if self.transfer_liked_songs:
            liked_songs = self.source.get_liked_songs()

            for liked_song in liked_songs:
                song_id = self.destination.find_song(liked_song)

                if song_id is not None:
                    self.destination.save_song(song_id)


                items_done +=1
                # Notificar progreso
                if progress_callback:
                    progress_callback(done = items_done, 
                                      total = total_items,
                                      current_item = "Library")



        #Transfer playlist
        for playlist in self.playlists:

            new_playlist_id = self.destination.create_playlist(playlist['name'])
            _ , songs = self.source.get_playlist(playlist['id'])

            for song in songs:
                song_id = self.destination.find_song(song)

                if song_id is not None:
                    self.destination.add_song_to_playlist(playlist_id = new_playlist_id,
                                                           song_id = song_id)
                    
                items_done +=1
                # Notificar progreso
                if progress_callback:
                    progress_callback(done = items_done, 
                                      total = total_items,
                                      current_item = playlist['name'])



    


    
