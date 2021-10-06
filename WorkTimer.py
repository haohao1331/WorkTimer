from tkinter import *
from tkinter import messagebox
from datetime import datetime
from env import *
import time
import requests

key = KEY
token = TOKEN
checklistId = CHECKLIST_ID
checkListUrl = f'https://api.trello.com/1/checklists/{checklistId}/checkItems'

# print(checkListUrl)
# print(key, token, checklistId)

timeout = 5

class Timer:
    def __init__(self):
        self.running = True
        self.lastRecordedDate = datetime.today().strftime('%Y-%m-%d')
        self.startTime = time.time()
        self.root = Tk()
        # root.geometry("500x200")
        self.root.title("Work Timer")
        self.title = Entry(self.root)
        self.title.grid(row=0, column=0)
        self.timeText = StringVar()
        self.timer = Label(self.root, textvariable=self.timeText, padx=100, pady=30).grid(row=1, column=0)
        self.stop = Button(self.root, text="I'm Done!", padx=100, pady=10, command=self.StopTimer).grid(row=3)
        self.UpdateTimer()
        self.root.mainloop()
        
    def StopTimer(self):
        if len(self.title.get()) == 0:
            return
        self.running = False
        try:
            query = {
                'name': f'{TrelloFormatTime(self.timeText.get())} {self.title.get()}',
                'pos': 'bottom',
                'key': key,
                'token': token
            }
            response = requests.request(
                "POST",
                checkListUrl,
                params=query,
                timeout=timeout
            )
            messagebox.showinfo("You Are Done!", f"You worked for {self.timeText.get()}!")
            print(response.text)
            
            newRecordDate = datetime.today().strftime('%Y-%m-%d')
            if(newRecordDate != self.lastRecordedDate):
                self.lastRecordedDate = newRecordDate
                query = {
                    'name': str(self.lastRecordedDate),
                    'pos': 'bottom',
                    'key': key,
                    'token': token
                }
                response = requests.request(
                    "POST",
                    checkListUrl,
                    params=query,
                    timeout=timeout
                )
        except (requests.ConnectionError, requests.Timeout) as exception:
            messagebox.showinfo("No Connection", f"You worked for {self.timeText.get()}! Note this in your notepad. ")
        
        # response = messagebox.askquestion("You Are Done!", "You worked for {}!\nDo you want to resume?".format(self.timeText.get()))
        self.title.delete(0, 'end')
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
    
def TrelloFormatTime(x : str):
    (hours, minutes, seconds) = [int(i) for i in x.split(':')]
    # print(hours, minutes, seconds)
    minutes += int(seconds >= 30)
    hours = str(hours + minutes // 60)
    minutes = str(minutes % 60)
    return f'{FormatedTime(hours)}:{FormatedTime(minutes)}'
    
    
timer = Timer()