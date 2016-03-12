from tkinter import *
from tkinter import ttk
import threading
import time

class splash(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.title("Splash Screen")
        frame = ttk.Frame(self.root, padding="3")
        #frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.grid_columnconfigure(3, weight=1)
        self.root.grid_rowconfigure(3,weight=1)

        self.root.wm_attributes('-topmost', True)
        self.root.wm_attributes('-fullscreen', True)
        #root.wm_attributes('-alpha', 0.5)

        self.progressBar = ttk.Progressbar(self.root, orient=HORIZONTAL, length=400, mode='determinate')
        self.progressBar.grid(column = 3, row = 3)

        self.root.mainloop()

splashScreen = splash()

import random
while splashScreen.progressBar['value'] < 100:
    time.sleep(0.01)
    splashScreen.progressBar['value'] += random.random()*5

#splashScreen.overrideredirect(True)



