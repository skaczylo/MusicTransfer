# main.py
from  spotify import SpotifyUser
from youtube import YouTubeMusicUser 
from view import MusicTransferGUI
from  presenter import Presenter



if __name__ == "__main__":
    #Modelo 
    sp_user = SpotifyUser()
    yt_user = YouTubeMusicUser()
    app = MusicTransferGUI()

    #Presenter
    controler = Presenter(app,sp_user,yt_user)


    app.mainloop()
    
    


 








