import threading
import time

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

def centreWindow(root, w=800, h=650):
    sw = root.winfo_screenwidth()  # Width of the screen
    sh = root.winfo_screenheight()  # Height of the screen

    # Calculate x and y coordinates for the Tk root window
    x = (sw / 2) - (w / 2)
    y = (sh / 2) - (h / 2) - 20

    root.geometry("%dx%d+%d+%d" % (w, h, x, y))  # Positions window

def doNotClose():
    pass

class splash(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.protocol("WM_DELETE_WINDOW", doNotClose)
        w = self.winfo_screenwidth()
        self.wm_attributes("-topmost", True)

        self.progressBar = ttk.Progressbar(self, orient=HORIZONTAL, mode="determinate")
        self.progressBar.pack(expand=True, side=BOTTOM, fill=BOTH)

        load = Image.open("assets/images/splash.png")
        ratio = (w // 2) / load.width
        load = load.resize((w // 2, int(load.height * ratio)), Image.ANTIALIAS)
        centreWindow(self, w // 2, load.height)
        self.photo = ImageTk.PhotoImage(load)
        image = ttk.Label(self, image=self.photo)
        image.pack(expand=True, fill=BOTH, side=TOP)

        self.wm_overrideredirect(True)

    def fill(self, increment=1):
        self.progressBar["value"] += increment
        if self.progressBar["value"] <= 100:
            # read more bytes after 100 ms
            self.after(15, self.fill)
        else:
            self.close()

    def close(self):
        self.destroy()
        print(self)

class newUserForm(Toplevel):

    def __init__(self, master, submitNewUserForm):
        Toplevel.__init__(self, master)

        self.wm_title("New User Registration:")
        self.tkraise(self)
        self.resizable(width=False, height=False)
        self.wm_attributes("-topmost", True)
        centreWindow(self, 300, 150)

        frame = ttk.Frame(self, padding=10)
        frame.grid(row=0, column=0, sticky=(N, E, S, W))

        intro = ttk.Label(frame, text="Welcome to Newton's Laboratory! \nPlease enter in some details..", justify=LEFT)
        intro.grid(row=0, column=0, columnspan=3, sticky=(N, E, S, W))
        firstNameLabel = ttk.Label(frame, text="First Name:")
        firstNameLabel.grid(row=1, column=1, sticky=(S, E), padx=5, pady=5)
        lastNameLabel = ttk.Label(frame, text="Last Name:")
        lastNameLabel.grid(row=2, column=1, sticky=(S, E), padx=5, pady=5)

        self.firstNameEntry = ttk.Entry(frame)
        self.firstNameEntry.grid(row=1, column=2, columnspan=2, pady=5)
        self.lastNameEntry = ttk.Entry(frame)
        self.lastNameEntry.grid(row=2, column=2, columnspan=2, pady=5, sticky=W)

        okButton = ttk.Button(frame, text="Submit", command=submitNewUserForm)
        okButton.grid(row=1, column=5, rowspan=2, columnspan=2, sticky=W, padx=10)

        self.errorLabel = ttk.Label(frame, text="", foreground='red', justify=LEFT)
        self.errorLabel.grid(row=3, column=0, columnspan=5, pady=5, sticky=W)

        self.bind("<Return>", submitNewUserForm)

        self.protocol("WM_DELETE_WINDOW", doNotClose)

        self.focus()

    def close(self):
        self.master.focus()
        self.destroy()

class window(Tk):
    def __init__(self):
        Tk.__init__(self)
        #s = ttk.Style().theme_use('clam')

        centreWindow(self)
        self.wm_title("Newton's laboratory")
        self.bodyText = StringVar()
        #ttk.Label(self, textvariable = self.bodyText, padding = 10).grid(row=0, column =0)

        self.focus()


    def createNewUserForm(self, submitNewUserForm):
        self.newUserForm = Toplevel(self)
        self.newUserForm.wm_title("New User Registration:")
        self.newUserForm.tkraise(self)
        self.newUserForm.resizable(width=False, height=False)
        self.newUserForm.wm_attributes("-topmost", True)
        centreWindow(self.newUserForm, 300, 150)

        frame = ttk.Frame(self.newUserForm, padding=10)
        frame.grid(row=0, column=0, sticky=(N, E, S, W))

        intro = ttk.Label(frame, text="Welcome to Newton's Laboratory! \nPlease enter in some details..", justify=LEFT)
        intro.grid(row=0, column=0, columnspan=3, sticky=(N, E, S, W))
        firstNameLabel = ttk.Label(frame, text="First Name:")
        firstNameLabel.grid(row=1, column=1, sticky=(S, E), padx=5, pady=5)
        lastNameLabel = ttk.Label(frame, text="Last Name:")
        lastNameLabel.grid(row=2, column=1, sticky=(S, E), padx=5, pady=5)

        self.newUserForm.firstNameEntry = ttk.Entry(frame)
        self.newUserForm.firstNameEntry.grid(row=1, column=2, columnspan=2, pady=5)
        self.newUserForm.lastNameEntry = ttk.Entry(frame)
        self.newUserForm.lastNameEntry.grid(row=2, column=2, columnspan=2, pady=5, sticky=W)

        okButton = ttk.Button(frame, text="Submit", command=submitNewUserForm)
        okButton.grid(row=1, column=5, rowspan=2, columnspan=2, sticky=W, padx=10)

        self.newUserForm.errorLabel = ttk.Label(frame, text="", foreground='red', justify=LEFT)
        self.newUserForm.errorLabel.grid(row=3, column=0, columnspan=5, pady=5, sticky=W)

        self.newUserForm.bind("<Return>", submitNewUserForm)

        self.newUserForm.protocol("WM_DELETE_WINDOW", doNotClose)

        self.newUserForm.focus()

    def createMainMenu(self, switchScreenTo):
        self.wm_title("Newton's laboratory - Main Menu")

        menuItemsText = StringVar(value=(" - Generate Quiz", " - Free Simulation", " - Review Notes", " - Preferences"))

        self.mainMenu = ttk.Frame(self, padding=10)
        self.mainMenu.grid(column=0, row=0, columnspan=5, rowspan=3, sticky=(N, E, S, W))


        self.mainMenu.items = ttk.LabelFrame(self.mainMenu, text="Menu Items:", padding=10)
        self.mainMenu.items.grid(column=0, row=0, columnspan=2, rowspan=2, sticky=(N, E, S, W))

        self.mainMenu.items.choices = Listbox(self.mainMenu.items, listvariable=menuItemsText, activestyle=NONE)
        self.mainMenu.items.choices.pack(fill=BOTH, expand=1)

        self.mainMenu.desc = ttk.LabelFrame(self.mainMenu, padding=10, text="Description:")
        self.mainMenu.desc.grid(column=0, row=2, columnspan=2, rowspan=1, sticky=(N, E, S, W))

        self.mainMenu.desc.texts = ["trhbdvwegdwveorgreerrebefsebhthtsthrbb  tbbff brbfbfbbbreberrbbrbbberb"]
        ttk.Label(self.mainMenu.desc, text=self.mainMenu.desc.texts[0], justify=LEFT)\
            .pack(fill=BOTH)

        self.mainMenu.properties = ttk.LabelFrame(self.mainMenu, text="Properties:", padding = 10)
        self.mainMenu.properties.grid(column=2, row=0, columnspan=3, rowspan=3, sticky=(N, E, S, W))
        self.mainMenu.properties.thing = Listbox(self.mainMenu.properties, listvariable=menuItemsText, height=23)
        self.mainMenu.properties.thing.pack(fill=BOTH)

        self.mainMenu.columnconfigure(ALL, weight=3, minsize=100)
        self.mainMenu.rowconfigure(ALL, weight=1, minsize=100)
        self.columnconfigure(ALL, weight=3, minsize=100)
        self.rowconfigure(ALL, weight=1, minsize=100)

        self.focus()



