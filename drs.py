import tkinter as tk
from tkinter import ttk
import cv2
import PIL.Image,PIL.ImageTk
from functools import partial
import threading
import imutils
import time

stream=cv2.VideoCapture("clip.mp4")
flag = True
def play(speed):
    global flag
    print("playback speed is {}".format(speed))
    frame1=stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES,frame1+speed)

    grabbed,frame=stream.read()
    if not grabbed:
        exit()
    frame=imutils.resize(frame,width=SET_WIDTH,height=SET_HEIGHT)
    frame=PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tk.NW)
    if flag:
        canvas.create_text(150,20, fill="yellow", font="Times 30 bold",text="Decision pending")
    flag = not flag


def pending(decision):
    # 1. Display decision pending
    frame = cv2.cvtColor(cv2.imread("pending.jpg"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width = SET_WIDTH, height = SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image= frame, anchor=tk.NW)
    # 2. Wait for 3 second
    time.sleep(3)
    # 3. Display sponsor 
    frame = cv2.cvtColor(cv2.imread("sponsors.jpg"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width = SET_WIDTH, height = SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image= frame, anchor=tk.NW)
    # 4. Wait for 5 sec
    time.sleep(5)
    # 5. Display Result 
    if decision=='out':
        decisionImg='out.jpg'
    else:
        decisionImg='notout.jpg'
    
    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width = SET_WIDTH, height = SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image= frame, anchor=tk.NW)

   
    pass
# this is threading ... threading is used to handle two or more than two operation at a time 
# during the execution of python program 
def out():
    thread=threading.Thread(target=pending,args=("out",))
    thread.daemon = 1
    thread.start()
    print("Player is out")
    

def not_out():
    thread=threading.Thread(target=pending,args=("not_out",))
    thread.daemon = 1
    thread.start()
    print("player is not out")    



SET_WIDTH=650
SET_HEIGHT = 368
win=tk.Tk()
win.title("DRS kit")
cv_img=cv2.cvtColor(cv2.imread("main.jpg"),cv2.COLOR_BGR2RGB)
canvas = tk.Canvas(win, width = SET_WIDTH, height = SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0,0,anchor=tk.NW,image=photo)
canvas.pack()


#button to control playback
btn=tk.Button(win,text="<< Previous(fast)",width=50,command=partial(play,-25)) #partial function is used to run a  function with arguments
btn.pack()

btn=tk.Button(win,text="<< Previous(slow)",width=50,command=partial(play,-2))
btn.pack()

btn=tk.Button(win,text="Next(fast) >>",width=50,command=partial(play,+25))
btn.pack()

btn=tk.Button(win,text="Next(slow) >>",width=50,command=partial(play,+1))
btn.pack()

btn=tk.Button(win,text="Give NOTOUT",width=50,command=not_out)
btn.pack()

btn=tk.Button(win,text="Give OUT",width=50,command=out)

btn.pack()
win.mainloop()

