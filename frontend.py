# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 19:06:25 2023

@author: suvan
"""

import tkinter
import tkinter.messagebox
import customtkinter
import requests

from PIL import Image
 
import firebase_admin
from firebase_admin import credentials, storage
from firebase_admin import firestore
from firebase_admin import db

from google.cloud import storage
from google.oauth2 import service_account

from pygame import mixer
import os

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from supabase import create_client, Client

# try:
#     #  https://storage.googleapis.com/download/storage/v1/b/https://console.firebase.google.com/project/music-app-ffa78/storage/music-app-ffa78.appspot.com/files/o/songs%2FCloser.mp3?alt=media
#     cred = credentials.Certificate("./music-app-ffa78-firebase-adminsdk-qeepk-25d73c2a31.json")
#     firebase_admin.initialize_app(cred,{'storageBucket' : 'music-app-ffa78.appspot.com'})
#     print("Database connected successfully")

# except:
#     print("Error in connecting to database")

url: str ="https://argjkahpbsjcwfwisulc.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFyZ2prYWhwYnNqY3dmd2lzdWxjIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTYwNTkyNzQsImV4cCI6MjAxMTYzNTI3NH0.mull5uIl1E4EjNzrvK-agYtwfSETUfiIWnj3SCIA8Os"


try:
    supabase: Client = create_client(url, key)
    print ("Client created successfully")
except Exception as e:
    print ("Error creating client: ", e)

mixer.init()

songname=[]

try:
    response = supabase.table('SongList').select("Song Name").execute().dict()
    for i in response['data']:
        print(i['Song Name'])
        songname.append(i['Song Name'])
   
    print ("Data fetched successfully")
except Exception as e:
    print ("Error fetching data: ", e)

Songnames=[]
Imagenames=[]

try:
    res_songs = supabase.storage.from_('songs').list()
    res_imgs = supabase.storage.from_('images').list()
    print("listing files")
     
    for songs in res_songs:
        print (songs['name'])
        Songnames.append(songs['name'])
    
    for images in res_imgs:
        print (images['name'])
        Imagenames.append(images['name'])
       

except Exception as e:
    print ("Error fetching data: ", e)


songurl=[]

#getting song path for local storage
try:
    response = supabase.table('SongList').select("song_url").execute().dict()
    for i in response['data']:
        print(i['song_url'])
        songurl.append(i['song_url'].rstrip('\r\n'))
   
    print ("Data fetched successfully")
except Exception as e:
    print ("Error fetching data: ", e)

#getting image path for local storage
imgurl = []
try:
    response = supabase.table('SongList').select("img_url").execute().dict()
    for i in response['data']:
        print(i['img_url'])
        imgurl.append(i['img_url'].rstrip('\r\n'))
   
    print ("Data fetched successfully")
except Exception as e:
    print ("Error fetching data: ", e)

artist = []
try:
    response = supabase.table('SongList').select("Artist").execute().dict()
    for i in response['data']:
        print(i['Artist'])
        artist.append(i['Artist'].rstrip('\r\n'))
   
    print ("Data fetched successfully")
except Exception as e:
    print ("Error fetching data: ", e)

Name = []
try:
    response = supabase.table('SongList').select("Song Name").execute().dict()
    for i in response['data']:
        print(i['Song Name'])
        Name.append(i['Song Name'].rstrip('\r\n'))
   
    print ("Data fetched successfully")
except Exception as e:
    print ("Error fetching data: ", e)

# num=int(input("Enter the song number: "))

#Downloading songs from suvan
# try:
#     # set variable destination to the music folder under the root folder ./music/
#     songdestination = songurl[num]
#     print(Songnames[num])
#     with open(songdestination, 'wb+') as f:
#         download_song = supabase.storage.from_('songs').download(Songnames[num])
#         f.write(download_song)

# except Exception as e:
#     print ("Error fetching data: ", e)
    

#Downloading images from suvan
# try:

#     imgdestination = imgurl[num]
#     print(Imagenames[num])
#     with open(imgdestination, 'wb+') as f:
#         download_image = supabase.storage.from_('images').download(Imagenames[num])
#         f.write(download_image)

# except Exception as e:
#     print ("Error fetching data: ", e)

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("purple")  # Themes: "blue" (standard), "green", "dark-blue"

# db=firestore.client()
# collection = db.collection('songlist')

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volume.GetMute()
volume.GetMasterVolumeLevel()
volume.GetVolumeRange()






class App(customtkinter.CTk):

    name=""
    artist=""
    song_url=""
    img_url=""
    currentsong=0
    paused = False
    song_loaded = False
    song_paused = False
    songlength = 0
    songdict={}

    # global paused, song_loaded, song_paused

    def __init__(self):
        super().__init__()
        

        # configure window
        self.title("Tune Wave")
        self.geometry(f"{1280}x{720}")

        # configure grid layout (4x4)
        self.grid_columnconfigure((1), weight=1)
        
        self.grid_rowconfigure((1), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)  

        #create label for songname and artist
        self.playings_label = customtkinter.CTkLabel(self.sidebar_frame, text="Now Playing: ", fg_color="transparent", bg_color="transparent", font=customtkinter.CTkFont(size=30, weight="normal"))
        self.playings_label.grid(row=0, column=0, padx=(20, 20), pady=(10), sticky="nsew")
        self.song_name_label =  customtkinter.CTkLabel(self.sidebar_frame, text="name", fg_color="transparent", bg_color="transparent", font=customtkinter.CTkFont(size=20, weight="normal"))
        self.song_name_label.grid(row=1, column=0, padx=(20, 20), pady=(10,5), sticky="nsew")
        self.song_artist_label = customtkinter.CTkLabel(self.sidebar_frame, text="artist", fg_color="transparent",  bg_color="transparent", font=customtkinter.CTkFont(size=15, weight="normal"))
        self.song_artist_label.grid(row=2, column=0, padx=(20), pady=(5,10), sticky="nsew") 
        
        #assign images to buttons
        self.play_picture = customtkinter.CTkImage(light_image=Image.open("./assets/play.png"),size=(32, 32))
        self.skip_f_picture = customtkinter.CTkImage(light_image=Image.open("./assets/skip_f.png"),size=(32, 32))
        self.skip_p_picture = customtkinter.CTkImage(light_image=Image.open("./assets/skip_p.png"),size=(32, 32))
        self.pause_picture = customtkinter.CTkImage(light_image=Image.open("./assets/pause.png"),size=(32, 32))
        self.load_picture = customtkinter.CTkImage(light_image=Image.open("./assets/download.png"),size=(32, 32))

        #create control buttons
        self.forward_button = customtkinter.CTkButton(self.sidebar_frame, image=self.skip_f_picture, text="" , fg_color="transparent", border_width=0, text_color=("gray10", "#DCE4EE"), command=self.next)
        self.forward_button.grid(row=5, column=0, padx=(20, 20), pady=(10), sticky="nsew")

        self.play_pause_btn = customtkinter.CTkButton(master=self.sidebar_frame, image=self.load_picture, text="" , fg_color="transparent", border_width=0, text_color=("gray10", "#DCE4EE"), command=self.download_files)
        self.play_pause_btn .grid(row=6, column=0, padx=(20, 10), pady=(10, 10), sticky="nsew")   
        
        self.previous_button = customtkinter.CTkButton(self.sidebar_frame, image=self.skip_p_picture, text="" , fg_color="transparent", border_width=0, text_color=("gray10", "#DCE4EE"), command=self.previous)
        self.previous_button.grid(row=7, column=0, padx=(20, 20), pady=(10), sticky="nsew")

        #scaling Menu

        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        # self.entry = customtkinter.CTkEntry(self, placeholder_text="Search Bar")
        # self.entry.grid(row=0, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        # self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.read)
        # self.main_button_1.grid(row=0, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

        
      
        # create slider frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=3, column=1, columnspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)    
        


        # create  photo image
        self.cover_image = customtkinter.CTkImage(light_image=Image.open("./assets/music.png"),size=(200, 200))
        self.album_cover_button = customtkinter.CTkButton(self,image=self.cover_image, text="" , fg_color="transparent", border_width=0,  state="disabled", height=400 , text_color=("gray10", "#DCE4EE"))
        self.album_cover_button.grid(row=1, rowspan=2, column=1, padx=(20, 20), pady=(20, 20), sticky="ew")

        
        self.slider_1 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=1, command = self.playback)
        self.slider_1.grid(row=4, column=0, padx=(20, 10), pady=(10, 10), sticky="nsew")   
        
        self.slider_2 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=1, orientation="vertical", command=self.changeVol)
        self.slider_2.grid(row=0, column=1, rowspan=2, padx=(10, 10), pady=(10, 10), sticky="ns")

        self.slider_2.set(0.405)
        self.slider_1.set(0)

        

    def download_files(self):
        # self.read('Closer')
        # credentials = service_account.Credentials.from_service_account_file("./music-app-ffa78-firebase-adminsdk-qeepk-25d73c2a31.json")
        try:
            for i in range(int(len(Songnames))):
                self.songdict[i]=[ songurl[i],imgurl[i],artist[i],Name[i] ]

            self.read()
        except Exception as e:
            print(e)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")
        
    def read(self):
        # song_metadata = collection.document(songname).get().to_dict()
        # # print(song_metadata)

        self.name = self.songdict[self.currentsong][3]
        # print(self.name)
        self.artist = self.songdict[self.currentsong][2]
        # print(self.artist)
        
        # set imgurl to imgurl value from songdict of the index currentsong
        self.img_url = self.songdict[self.currentsong][1]
        self.song_url = self.songdict[self.currentsong][0]
        print(f"{0}\n{1}\n{2}\n{3}\n",self.song_url,self.img_url,self.artist,self.name)
        self.play()

    def play(self):
        
        if not self.song_loaded:
           
            print("changing image...")
            self.cover_image = customtkinter.CTkImage(light_image=Image.open(self.img_url),size=(300, 300))
            self.album_cover_button.configure(image=self.cover_image)
            print('changing name...')
            self.song_name_label.configure(text=self.name)
            print('changing artist...')
            self.song_artist_label.configure(text=self.artist)
            print(" playing...")
            self.play_pause_btn.configure(image=self.pause_picture)
            self.song_loaded = True
            mixer.music.load(self.song_url)
            # mixer.music.set_pos(0.0) 
            self.song_length = 245
            mixer.music.play()
            # mixer.music.set_endevent(self.next)
        
        if self.paused:                
                self.paused = False
                self.song_paused = False
                self.play_pause_btn.configure(image=self.pause_picture)
                mixer.music.unpause()
                
        else:
            self.paused = True
            self.song_paused = True
            self.play_pause_btn.configure(image=self.play_picture)
           
            mixer.music.pause()
            
    def next(self):
        print ("Next")
        # mixer.music.queue()
        mixer.music.stop()
        self.song_loaded = False
        self.currentsong+=1
        self.read()
        self.play()

    def previous(self): 
        print ("Previous")
        # mixer.music.queue()
        mixer.music.stop()
        self.song_loaded = False
        if (self.currentsong-1) < 0:
            self.currentsong=0

        else:
            self.currentsong-=1
            self.read()
            self.play()

    def changeVol(self,args):
        volRange = volume.GetVolumeRange()
        minVol = volRange[0]
        maxVol = volRange[1]
        value=self.slider_2.get()     
        
        currentVol=(1 - value) * minVol + value * maxVol
        
        volume.SetMasterVolumeLevel(currentVol, None)

    def playback(self,args):
        song_pos = mixer.music.get_pos()
        song_pos = (song_pos / 1000 ) % 60
        print('The  {} seconds.'.format(song_pos))
        value=self.slider_1.get()
        print(value)
        currentpos = value * song_pos

        print('The song is currently at {} seconds.'.format(currentpos))
        mixer.music.set_pos(currentpos)


if __name__ == "__main__":
    app = App()
    app.mainloop()

#kivy