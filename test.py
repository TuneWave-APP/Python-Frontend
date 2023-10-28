import os
from supabase import create_client, Client

url: str ="https://argjkahpbsjcwfwisulc.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFyZ2prYWhwYnNqY3dmd2lzdWxjIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTYwNTkyNzQsImV4cCI6MjAxMTYzNTI3NH0.mull5uIl1E4EjNzrvK-agYtwfSETUfiIWnj3SCIA8Os"

#Creating client from suvan
try:
    supabase: Client = create_client(url, key)
    print ("Client created successfully")
except Exception as e:
    print ("Error creating client: ", e)

songname=[]
#Retrieving data from database from suvan
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

#Retrieving data from storage from suvan
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



print("\nFirst song name is: ",Songnames[0])


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

num=int(input("Enter the song number: "))

#Downloading songs from suvan
try:
    # set variable destination to the music folder under the root folder ./music/
    songdestination = songurl[num]
    print(Songnames[num])
    with open(songdestination, 'wb+') as f:
        download_song = supabase.storage.from_('songs').download(Songnames[num])
        f.write(download_song)

except Exception as e:
    print ("Error fetching data: ", e)
    

#Downloading images from suvan
try:

    imgdestination = imgurl[num]
    print(Imagenames[num])
    with open(imgdestination, 'wb+') as f:
        download_image = supabase.storage.from_('images').download(Imagenames[num])
        f.write(download_image)

except Exception as e:
    print ("Error fetching data: ", e)