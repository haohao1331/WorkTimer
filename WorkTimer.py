from tkinter import *
import time
from tkinter import messagebox

root = Tk()
# root.geometry("500x200")
root.title("Work Timer")
title = Label(root, text="Work Timer", padx=100, pady=30).grid(row=0, column=0)
timeText = StringVar()
timer = Label(root, textvariable=timeText, padx=100, pady=30).grid(row=1, column=0)

def StopTimer():
    global running, startTime
    stopTime = time.time()
    running = False
    response = messagebox.askquestion("You Are Done!", "You worked for {}!\nDo you want to resume?".format(timeText.get()))
    print(response)
    if response == "yes":
        running = True
        startTime = time.time() - stopTime + startTime
        UpdateTimer()
    if response == "no":
        running = True
        startTime = time.time()
        UpdateTimer()

stop = Button(root, text="I'm Done!", padx=100, pady=10, command=StopTimer).grid(row=3)

running = True
def UpdateTimer():
    if not running: 
        return
    hours = FormatedTime(str(int(time.time() - startTime) // 3600))
    minutes = FormatedTime(str((int(time.time() - startTime) // 60) % 60))
    seconds = FormatedTime(str(int(time.time() - startTime) % 60))
    timeText.set(hours + ":" + minutes + ":" + seconds)
    root.after(1000, UpdateTimer)

def FormatedTime(x):
    if len(x) < 2:
        return "0" + x
    else:
        return x

startTime = time.time()

UpdateTimer()

root.mainloop()