# main.py
from  spotify import SpotifyUser
from youtube import YouTubeMusicUser 
from view import MusicTransferGUI
from  presenter import Presenter
import sys



if __name__ == "__main__":

    
    # Redirige stdout y stderr a un archivo
    sys.stdout = open("log.txt", "w", encoding="utf-8")
    sys.stderr = open("log.txt", "w", encoding="utf-8")
    
    #Modelo 
    sp_user = SpotifyUser()
    yt_user = YouTubeMusicUser()
    app = MusicTransferGUI()

    #Presenter
    controler = Presenter(app,sp_user,yt_user)


    app.mainloop()
    
    


 








