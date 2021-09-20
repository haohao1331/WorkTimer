from tkinter import *
import time
from tkinter import messagebox


class Timer:
    def __init__(self):
        self.running = True
        self.startTime = time.time()
        self.root = Tk()
        # root.geometry("500x200")
        self.root.title("Work Timer")
        self.title = Label(self.root, text="Work Timer", padx=100, pady=30).grid(row=0, column=0)
        self.timeText = StringVar()
        self.timer = Label(self.root, textvariable=self.timeText, padx=100, pady=30).grid(row=1, column=0)
        self.stop = Button(self.root, text="I'm Done!", padx=100, pady=10, command=self.StopTimer).grid(row=3)
        self.UpdateTimer()
        self.root.mainloop()
        
    def StopTimer(self):
        stopTime = time.time()
        self.running = False
        response = messagebox.askquestion("You Are Done!", "You worked for {}!\nDo you want to resume?".format(self.timeText.get()))
        print(response)
        if response == "yes":
            self.running = True
            self.startTime = time.time() - stopTime + self.startTime
            self.UpdateTimer()
        if response == "no":
            self.running = True
            self.startTime = time.time()
            self.UpdateTimer()
    
    def UpdateTimer(self):
        if not self.running: 
            return
        hours = FormatedTime(str(int(time.time() - self.startTime) // 3600))
        minutes = FormatedTime(str((int(time.time() - self.startTime) // 60) % 60))
        seconds = FormatedTime(str(int(time.time() - self.startTime) % 60))
        self.timeText.set(hours + ":" + minutes + ":" + seconds)
        self.root.after(1000, self.UpdateTimer)


def FormatedTime(x):
    if len(x) < 2:
        return "0" + x
    else:
        return x
    
timer = Timer()