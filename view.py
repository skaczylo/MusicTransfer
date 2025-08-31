import tkinter
import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Canvas
import customtkinter as ctk
import time
import threading

BUTTON_COLOR ="#219ebc"
HOVER_COLOR = "#0e728b"
FRAME = "#8ecae6"


ctk.set_appearance_mode("Light")


class DualScrollFrame(ctk.CTkFrame):

    def __init__(self, parent, width=400, height=300, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        
        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.grid(row=0, column=0, sticky="nsew")

    
        # Scrollbars
        self.v_scrollbar = ctk.CTkScrollbar(self , orientation="vertical", command=self.canvas.yview)
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.h_scrollbar = ctk.CTkScrollbar(self , orientation="horizontal", command=self.canvas.xview)
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")

        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)

       
        self.inner_frame = ctk.CTkFrame(self.canvas)
        self.inner_frame.grid(sticky = "nsew")
        self.inner_frame_id = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

       
        self.inner_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

    def _on_frame_configure(self, event):
        
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        
        canvas_width = event.width
        canvas_height = event.height
        frame_width = self.inner_frame.winfo_reqwidth()
        frame_height = self.inner_frame.winfo_reqheight()

        new_width = max(frame_width, canvas_width)
        new_height = max(frame_height, canvas_height)

        self.canvas.itemconfig(self.inner_frame_id, width=new_width, height=new_height)



class ProgressFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

      
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0,weight=1)
       

        self.pb_frames = ctk.CTkFrame(self)
        self.pb_frames.grid(row = 0,column = 0,padx = 10,pady = 10,sticky = "nsew")
        self.pb_frames.grid_columnconfigure(0,weight=1)
        self.pb_frames.grid_rowconfigure((0,1),weight=1)
        # Text
        self.label = ctk.CTkLabel(self.pb_frames, text="Fetching data...")
        self.label.grid(row=0, column=0, sticky="nsew")

        #Progress Bar
        self.progress = ctk.CTkProgressBar(self.pb_frames)
        self.progress.grid(row=1, column=0, pady=5, padx=20, sticky="ew")
        self.progress.set(0)

    def update_label(self,text):
        self.label.configure(text = text)

    def update_progress(self, done, total, current_item):
        self.label.configure(text=f"Processing {done}/{total}: {current_item}")
        self.progress.set(done / total)


class YoutubeSignIn(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_rowconfigure((0,1,2),weight=1)
        self.grid_columnconfigure(0,weight=1)
        
       #How to sign in frame
        self.text_frame = DualScrollFrame(self)
        self.text_frame.grid(row=0, column=0,rowspan=5,padx=10, pady=(10, 0), sticky="nsew")

        for i in range(0,9):
            self.text_frame.inner_frame.grid_rowconfigure(i,weight=1)
        self.text_frame.inner_frame.grid_columnconfigure(0,weight=1)

        self.title_label = ctk.CTkLabel(
            self.text_frame.inner_frame,
            text="How to sign in Youtube Music",
            fg_color="gray70", corner_radius=6
        )
        self.title_label.grid(row=0, column=0, padx=10, pady=(10, 20), sticky="ew")

        # Steps content
        steps = [
            "1. Open a new incognito/private tab in your browser and go to https://music.youtube.com.",
            "2. Sign in to your account.",
            "3. Make sure you are successfully logged in.",
            "4. Click on 'My Library'.",
            "5. Open the developer tools (Ctrl+Shift+I) and select the 'Network' tab.",
            "6. Use the search/filter box and type '/browse'.",
            "7. Click on the Name of any matching request. In the 'Headers' tab, scroll down to the 'Request headers' section and copy everything to the end of that section.",
            "This might seem a little concerning, but don’t worry — just like with Spotify, only you can access this data, and it stays on your computer."
        ]


        for i, step in enumerate(steps,start=1):
            label = ctk.CTkLabel(
                self.text_frame.inner_frame,
                text=step,
                wraplength=750,      
                justify="left",      
                font=ctk.CTkFont(size=12)
            )
            label.grid(row=i, column=0, padx=10, pady=(5, 10), sticky="w")


        #Copy hear Request Header
        self.placeholder_text = "Copy here Request Header"
        self.request_header = ctk.CTkTextbox(self, width=200, height=30)
        self.request_header .insert("0.0", self.placeholder_text)
        self.request_header.grid(row = 6,column=0, sticky="ew", padx=10, pady=20)
        self.request_header.configure(text_color="gray", fg_color="#f0f0f0")
        self.request_header.bind("<FocusIn>", self.on_focus_in)
        self.request_header.bind("<FocusOut>", self.on_focus_out)
    

        self.sign_in_button = ctk.CTkButton(self, 
                                            text="Sign In",
                                            fg_color=BUTTON_COLOR,
                                            hover_color=HOVER_COLOR
                                            )
        self.sign_in_button.grid(row = 7, column=0, padx=10, pady=20,sticky="ns")

    def on_focus_in(self, event):
        if self.request_header.get("0.0", "end-1c") == self.placeholder_text:
            self.request_header.delete("0.0", "end")
            self.request_header.configure(text_color="gray", fg_color="#f0f0f0")

    def on_focus_out(self, event):
        if self.request_header.get("0.0", "end-1c") == "":
            self.request_header.insert("0.0", self.placeholder_text)
            self.request_header.configure(text_color="gray", fg_color="#f0f0f0")
    def update_frame(self):
        pass    
  

        
  
class DataSelection(ctk.CTkFrame):
 
    def __init__(self, master):
        super().__init__(master)
        
        self.checkboxes = []
        
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure((0,1,2),weight=1)

          #Boton Confirm
        self.confirm_button = ctk.CTkButton(self, 
                                            text="Confirm",
                                            fg_color=BUTTON_COLOR,
                                            hover_color=HOVER_COLOR)
        self.confirm_button.grid(row = 5,column = 0,padx=20, pady=20,sticky = "nsew")
        

    def update_frame(self,playlists_info,total_saved_songs):
        
    
        self.checkboxes = []
        self.grid_rowconfigure(0, weight=0)  
        self.grid_rowconfigure(1, weight=1)  
        self.grid_columnconfigure(0, weight=1) 
       
        #Library Frame
        self.library_frame = ctk.CTkFrame(self)
        self.library_frame.grid_columnconfigure(0, weight=1)
        self.library_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
        self.library_frame.grid_propagate(True) 

        library_var = tkinter.IntVar(value=1)
        self.library_checkbox = ctk.CTkCheckBox(self.library_frame, text=f"Library: {total_saved_songs} songs",variable=library_var)
        self.library_checkbox.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")

        self.title = ctk.CTkLabel(self.library_frame, text="Library", fg_color="gray70", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
        self.checkboxes.append(self.library_checkbox)

        #Playlist Frame
        self.playlist_frame = ctk.CTkScrollableFrame(self,label_text="Playlist")
        self.playlist_frame.grid(row=1, column=0, rowspan = 2, padx=10, pady=(10, 0), sticky="nsew")


        for i, value in enumerate(playlists_info):
            var = tkinter.IntVar(value=1)
            checkbox = ctk.CTkCheckBox(self.playlist_frame, text=value['name'],variable=var)
            checkbox.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")
            self.checkboxes.append(checkbox)

      

   
      
class SpotifySignIn(ctk.CTkFrame):

    def __init__(self,master):
        super().__init__(master)
       
        self.grid_rowconfigure((0,1,2),weight=1)
        self.grid_columnconfigure(0,weight=1)

    
        #How to sign in frame
        self.sing_in_frame = DualScrollFrame(self)
        self.sing_in_frame.grid(row=0, column=0,rowspan = 5,padx=10, pady=(10, 0), sticky="nsew")
       
        self.sing_in_frame.inner_frame.grid_columnconfigure(0,weight=1)
        for i in range(0,6):
            self.sing_in_frame.inner_frame.grid_rowconfigure(i,weight=1)

        self.title = ctk.CTkLabel(self.sing_in_frame.inner_frame, text="How to sign in Spotify", fg_color="gray70", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 20), sticky="nsew")

        #Title How to sign in
        instructions_text = [
        "To use this program, you need a Spotify Developer account, as Spotify only accepts applications from organizations (not individuals).",
        "Getting started is easy — just follow these steps:",
        "1. Go to https://developer.spotify.com",
        "2. Log in with your Spotify account",
        "3. Once logged in, go to the Dashboard",
        "4. Click on 'Create an App'",
        "5. Fill in the required information. In the Redirect URIs section, enter 'http://127.0.0.1:8888/callback'",
        "6. After creating the app, copy your Client ID",
        "7. Once you've completed these steps, click 'Sign In'. A browser window will open (if two windows appear, just close one). Spotify will ask for permission to access things like your saved songs and playlists. This might seem concerning, but there’s no risk: the app runs only on your computer and connects directly to Spotify. No external servers are involved, and nobody else can access your data. Your information remains completely private between you and Spotify.",
        "8. After granting permission, just wait a moment."
        ]


        #Instructions
        for i, step in enumerate(instructions_text, start=2):
            label = ctk.CTkLabel(
                self.sing_in_frame.inner_frame,
                text=step,
                wraplength=1000,      
                justify="left",    
                font=ctk.CTkFont(size=12)
            )
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

        
        #Copy here Cliente ID

        self.placeholder_text = "Copy here Client ID"
        self.client_id = ctk.CTkTextbox(self, width=200, height=30)
        self.client_id .insert("0.0", self.placeholder_text)
        self.client_id.grid(row = 6,column=0, sticky="ew", padx=10, pady=20)
        self.client_id.configure(text_color="gray", fg_color="#f0f0f0")
        self.client_id.bind("<FocusIn>", self.on_focus_in)
        self.client_id.bind("<FocusOut>", self.on_focus_out)


        #Sign in button
        self.sign_in_button = ctk.CTkButton(self, 
                                            text="Sign In",
                                            fg_color=BUTTON_COLOR,
                                            hover_color=HOVER_COLOR,
                                            )
        self.sign_in_button.grid(row = 7, column=0, padx=10, pady=20,sticky="ns")
       

    def on_focus_in(self, event):
        if self.client_id.get("0.0", "end-1c") == self.placeholder_text:
            self.client_id.delete("0.0", "end")
            self.client_id.configure(text_color="gray", fg_color="#f0f0f0")

    def on_focus_out(self, event):
        if self.client_id.get("0.0", "end-1c") == "":
            self.client_id.insert("0.0", self.placeholder_text)
            self.client_id.configure(text_color="gray", fg_color="#f0f0f0")
    def update_frame(self):
        pass    
  
        

class SelectSource(ctk.CTkFrame):

    def __init__(self,master):
        super().__init__(master)
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)

        #FRAME
        self.frame = ctk.CTkFrame(self)
        self.frame.grid(row = 0,column = 0,padx = 30,pady=30,sticky = "nsew")
        self.frame.grid_rowconfigure((0,1),weight=1)
        self.frame.grid_columnconfigure((0,1),weight=1)

        #LABEL
        self.label = ctk.CTkLabel(self.frame,text="Select source", fg_color="transparent",text_color="black",font=("Arial", 24))
        self.label.grid(row=0,column = 0,padx=20, pady=20,sticky = "ew", columnspan=2)

        #SPOTIFY BUTTON
        self.spotify_button = ctk.CTkButton(self.frame,
                                            width=400,
                                            height=200,
                                            text="Spotify",
                                            fg_color=BUTTON_COLOR,
                                            hover_color=HOVER_COLOR,
                                            font=("Arial", 40))
        
        self.spotify_button.grid(row = 1,column = 0,padx=20, pady=20)
      
    
        #YOUTUBE BUTTON
        self.ytMusic_button = ctk.CTkButton(self.frame,
                                            width=400,
                                            height=200,
                                            text="Youtube Music",
                                            fg_color=BUTTON_COLOR,
                                            hover_color=HOVER_COLOR,
                                            font=("Arial", 40)
                                            )
        
        self.ytMusic_button.grid(row = 1,column = 1,padx=20, pady=20)

      
       
    
    def update_frame(self):
        pass
   

class MusicTransferGUI(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Music Transfer")
        self.geometry("1000x600")

        self.frames = {}
        self.frames["SelectSource"] = SelectSource(self)
        self.frames["SpotifySignIn"] = SpotifySignIn(self)
        self.frames["DataSelection"] = DataSelection(self)
        self.frames["YoutubeSignIn"] = YoutubeSignIn(self)
        self.frames["ProgressFrame"] = ProgressFrame(self)

        for frame in self.frames.values():
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)


        self.frames["SelectSource"].lift()




    

    
