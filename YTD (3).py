#!/usr/bin/env python
# coding: utf-8

# # Libraries

# In[156]:


import tkinter as tk # Software GUI
from tkinter import * # For accessing all the tkinter libs/modules
from tkinter import filedialog , Text , Button # for  creating filedialog , Text fiels , Buttons
from pytube import YouTube , Playlist # For dowloading Youtube video
from PIL import ImageTk,Image   #Importing Png/Jpg images in Tkinter as tkinter doesn't support png/jpg
import re # As for date: 04-08-2020 pytube have error in its video url regex
import os # Accessing all system files,commands


# # CODE

# In[157]:


#Function for opening file explorer and saving the selected path
def browsefunc():
    output_path.append(filedialog.askdirectory())
    textBox1.insert('1.0',output_path[0] )
    textBox.insert("1.0","selected Folder : {}\n".format(output_path[0] ) )
#Opening the selected folder for download
def output():
        textBox.insert("1.0","opening the Output Folder : {}\n".format(output_path[0] ) )
        os.startfile(output_path[0])

#dowloading video with different resolutions 
def video():
    val = textBox2.get("1.0",'end-1c') #getting the text box input 
    
    if len(YouTube(val).streams.filter(res=res[-1],progressive=True) ) == 0: #check if the resoultion for video is progressive or adaptive
        out_file= YouTube(val).streams.filter(only_audio = True).first().download(output_path = output_path[0] ) #first download Audio
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file) #convert the audio to mp3
        vid = YouTube(val).streams.filter(res=res[-1]).first().download(output_path = output_path[0]) #download the video (adaptive type video don't have audio)
        file = output_path[0] +"/out.mp4" # for making temp output
        ffmpeg.concat(ffmpeg.input(vid),ffmpeg.input(new_file),v=1,a=1).output(file).run() #combined temp video
        os.remove(new_file) #remove source audio from output folder
        temp = vid #remove all the support files
        os.remove(vid)#remove all the support files
        os.rename(file,temp) #rename the final file to orignal 
        textBox.insert("1.0","Your Video is READY !! \n" )
    else: #if the video type is progressive 
        textBox.insert("1.0","Your Video is READY !! \n" )
        YouTube(val).streams.filter(res = res[-1],progressive=True).first().download(output_path = output_path[0])
#For downloading the playlist videos
def play_List():
    j = 1 #Numbering the video
    val = textBox2.get("1.0",'end-1c') #getting url
    playlist = Playlist(val) #adding the playlist 
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)") #There was an error in pytube i.e two many values to unpack which i fixed by recompiling the regular expersion
    for url in playlist.video_urls: #getting all the videos URL
        x =  YouTube(url).title 
        x = "[No"+" "+str(j)+" "+"]"+x #Name of video updated with indexing
        YouTube(url,on_progress_callback=on_progress).streams.first().download(output_path = output_path[0],filename=x)
        j+=1
    textBox.insert("1.0","Your Playlist is Downloaded !! \n" )
#downloading AUDIO
def audio():
    val = textBox2.get("1.0",'end-1c')#getting  URL
    out_file= YouTube(val,on_progress_callback=on_progress).streams.filter(only_audio = True).first().download(output_path = output_path[0] )
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3' 
    os.rename(out_file, new_file)#converting the file to mp3 format
    textBox.insert("1.0","Your Audio is READY !! \n" )
    
#Getting the selected option menu 
def callback(val):
    res.append(val) #getting the selected values from option
    download_btn = Button(root,command=video,image= btn,border=0)
    download_btn.place(x=60,y=690) #overlay the prev button
    output_btn = Button(root,  command=output,image= btn2,border=0)
    output_btn.place(x=300,y=690)#overlay the prev button

    
    
#defining Advance Radio buttons command Functions for video , audio and Playlist 

def r_Video():
    OptionList = []
    val = textBox2.get("1.0",'end-1c')
    textBox.insert("1.0","Downloading the video : {}".format(YouTube(val).title ) )
    for i in YouTube(val).streams:
        OptionList.append(str(i.resolution))
    OptionList = set(OptionList) #removing the duplicates values 
    OptionList = list(OptionList)
    OptionList.sort()  
    OptionList.pop(-1) #removing the none value
    variable = tk.StringVar(root)
    variable.set("Resolution")
    opt = tk.OptionMenu(root, variable, *OptionList,command=callback)
    opt.config(width=10, font=('Helvetica', 12))
    opt.place(x=10,y=300)
    
    variable.trace("w", callback)
   
    
def r_Audio():
    download_btn = Button(root, command=audio,image= btn,border=0)
    download_btn.place(x=60,y=690)#overlay the prev button
    output_btn = Button(root,  command=output,image= btn2,border=0)
    output_btn.place(x=300,y=690)#overlay the prev button
def r_Playlist():
    download_btn = Button(root, text="Playlist", command=play_List,image= btn, border=0 ,)
    download_btn.place(x=60,y=690)#overlay the prev button
    output_btn = Button(root,  command=output,image= btn2,border=0)
    output_btn.place(x=300,y=690)#overlay the prev button
    
#########################################################

# GUI CODE / MAIN CODE

########################################################
    
root = tk.Tk() #intializing the window
root.title("Youtube_Downloader_TS") #putting title to root window
root.resizable(False, False) # Not allowing Resizing of window
icon = ImageTk.PhotoImage(file = "C:/Users/Tumun/Desktop/jj.png") #icon image for Window
root.iconphoto(False, icon) #setting up the icon 

v = tk.IntVar() #intializing tkinter int variable
output_path = [] # storing the download location
res = [] # capturing resolution
#button Images
btn = ImageTk.PhotoImage(Image.open("C:/Users/Tumun/Desktop/btn1.png")) 
btn2 = ImageTk.PhotoImage(Image.open("C:/Users/Tumun/Desktop/btn3.png")) 
#Background image
img = ImageTk.PhotoImage(Image.open("C:/Users/Tumun/Desktop/ab.jpg")) 

canvas = tk.Canvas(root,height=780,width=600,)# adding another window inside root.
canvas2 = tk.Canvas(root,height=400,width=400,) # adding another window inside root.
label = Label(root, text="Download Folder  :",bg="#79e8e8") # making a label for User friendly GUI
label.place(x=10,y=20) # placing the widget in x,y position
textBox1=Text(root, height=1, width=55) # Text field for getting download folder path
textBox1.place(x=120,y=20) # placing the widget in x,y position
label1 = Label(root, text="Youtube URL:",bg="#fac3c3",width = 14) # making a label for User friendly GUI
label1.place(x=10,y=200) # placing the widget in x,y position
textBox=Text(root, height=14, width=70) # Output Textbox
textBox.place(x=10,y=458) # placing the widget in x,y position
textBox2=Text(root, height=1, width=70)
textBox2.insert('1.0', 'PUT THE URL  HERE') # text field for getting url input
textBox2.place(x=120,y=200) # placing the widget in x,y position

#Radio Buttons for VIDEO , AUDIO and PLAYLISTS 

R1 = Radiobutton( text="Video",
                  indicatoron = 0,
                  width = 15,
                  padx = 20, 
                  variable=v, 
                  command=r_Video,
                  value=2,
                activebackground="#fac3c3")
R1.place(x=30,y=230) # placing the widget in x,y position

R2 = Radiobutton(root, text="MP3", indicatoron = 0,
                  width = 15,
                  padx = 20, 
                  variable=v, 
                  command=r_Audio,
                activebackground="#fac3c3")
R2.place(x=240,y=230) # placing the widget in x,y position

R3 = Radiobutton(root, text="Playlist", value=3,indicatoron = 0,
                  width = 15,
                  padx = 20, 
                  variable=v, 
                  command=r_Playlist,
                activebackground="#fac3c3")
R3.place(x=420,y=230) # placing the widget in x,y position
browsebutton = Button(root, text="OutPut Folder", command=browsefunc,activebackground="#79e8e8") # Browse button for getting the output folder path
browsebutton.place(x=450,y=45) # placing the widget in x,y position
download_btn = Button(root, text="Playlist",image= btn, border=0 ) #default Download btn
download_btn.place(x=60,y=690) # placing the widget in x,y position
output_btn = Button(root,  command=output,image= btn2,border=0) #default Output btn
output_btn.place(x=300,y=690) # placing the widget in x,y position
# here, image option is used to 
# set image on button 
canvas.pack()# binding the canvas to root
canvas.create_image(120,-50, anchor=NW, image=img) #remeber to put this always after the x.pack()
root.mainloop()#loop for our window


# In[ ]:




