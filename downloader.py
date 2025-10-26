from pywinauto import Desktop, Application
from pywinauto.keyboard import SendKeys
import pywinauto
import datetime
import time
import sys
import os
import winsound
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

print("Open iexplorer and window 'Playback'. Select mode 'by time' and rerun if errors.")

global observer_datetime
observer_datetime = datetime.datetime.now()

class FSHandler(FileSystemEventHandler):
    def on_created(self, event):
        global observer_datetime
        observer_datetime = datetime.datetime.now()

iexplore = Application(backend="win32").connect(path="iexplore.exe", title="Playback")
wplb = iexplore.Playback

picker = wplb.DateTimePicker1

sdate = picker.get_time()
sdate = datetime.datetime(sdate.wYear, sdate.wMonth, sdate.wDay)
cdate = datetime.datetime.today()

while sdate <= cdate:
    print("Download from: " + sdate.strftime("%d.%m.%Y"))
    
    picker.set_time(year=sdate.year,
                    month=sdate.month,
                    day_of_week=sdate.weekday(),
                    day=sdate.day,
                    hour=0,
                    minute=0,
                    second=0,
                    milliseconds=0)
    picker.click_input(coords=(9,9))
    picker.type_keys("{DOWN}")
    picker.type_keys("{UP}")
    
    time.sleep(2)
    
    wplb.Search.click()

    time.sleep(5)

    res = False
    for i in iexplore.windows():
        if "Prompt" in i.window_text() and i.is_visible():
            i.close();
            time.sleep(1)
            sdate = sdate + datetime.timedelta(days=1)
            res = True
            break
    if res:
        continue

    item = wplb.ListView.get_item(0)
    time.sleep(1)
    item.click()
    time.sleep(1)
    item.check()

    time.sleep(1)

    wplb.Download.click()

    time.sleep(5)
    
    observer = Observer()
    observer.schedule(FSHandler(), path="cam", recursive=False)
    observer.start()
    
    iexplore.Download.OK.click()

    observer_datetime = datetime.datetime.now()
    while True:
        time.sleep(2)
        if (datetime.datetime.now() - observer_datetime).total_seconds() > 420:
            print(str(datetime.datetime.now()) + " : possible error - last update in " + str(observer_datetime))
            winsound.PlaySound("error.wav", winsound.SND_FILENAME)

        res = False
        for i in iexplore.windows():
            if "Prompt" in i.window_text() and i.is_visible():
                i.close();
                observer.stop()
                res = True
                break
        if res:
            break

    time.sleep(5)
    os.rename("cam", sdate.strftime("%m.%d"))
    os.mkdir("cam")

    #Prepare for possible new loop
    wplb.Search.click()

    time.sleep(5)
    
    sdate = sdate + datetime.timedelta(days=1)
