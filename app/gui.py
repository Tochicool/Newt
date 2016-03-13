import threading
import time

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

class splash(threading.Thread):
    setUp = False
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

        while not self.setUp:
            pass

    def close(self):
        self.root.quit()

    def run(self):
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        self.root.geometry('%dx%d+%d+%d' % (w//2, h//2, w//4, h//4))
        self.root.wm_attributes('-topmost', True)

        load = Image.open('assets/images/splash.png')
        ratio = (w//2)/load.width
        load = load.resize((w//2, int(load.height*ratio)), Image.ANTIALIAS)
        self.root.geometry('%dx%d+%d+%d' % (w//2, load.height, w//4, h//4))
        render = ImageTk.PhotoImage(load)
        image = ttk.Label(self.root, image=render)

        self.progressBar = ttk.Progressbar(self.root, orient=HORIZONTAL, length=w, mode='determinate')
        self.progressBar.pack(expand = True, side = BOTTOM, fill = BOTH)
        print(self.progressBar['value'])
        image.pack(expand = True, side = TOP, fill = BOTH)

        self.root.overrideredirect(True)
        self.setUp = True
        self.root.mainloop()

    def fillBar(self):
        for i in range(101):
            self.progressBar['value'] = i
            time.sleep(0.01)

if __name__ == '__main__':
    splashScreen = splash()
    splashScreen.fillBar()





