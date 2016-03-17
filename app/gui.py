from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

headFont = ("Helvetica", 35, "bold")
buttonFont = ("Helvetica", 20, "bold")
bodyFont = ("Helvetica", 13)

def centre(window):
    window.update_idletasks()
    screenWidth = window.winfo_screenwidth()  # Width of the screen
    screenHeight= window.winfo_screenheight()  # Height of the screen

    # Calculate x and y coordinates for the Tk root window
    x = (screenWidth//2) - (window.winfo_width()//2)
    y = (screenHeight//2) - (window.winfo_height()//2)

    window.geometry("+%d+%d" % (x,y)) # Positions window

def doNotClose(): pass

class splash(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.protocol("WM_DELETE_WINDOW", doNotClose)
        self.wm_attributes("-topmost", True)
        self.wm_overrideredirect(True)

        self.progressBar = ttk.Progressbar(self, orient=HORIZONTAL, mode="determinate")
        self.progressBar.pack(expand=True, side=BOTTOM, fill=BOTH)

        w = self.winfo_screenwidth()
        load = Image.open("assets/images/splash.png")
        ratio = (w // 2) / load.width
        load = load.resize((w // 2, int(load.height * ratio)), Image.ANTIALIAS)
        #self["width"] = w//2
        #self["height"] = load.height
        self.photo = ImageTk.PhotoImage(load)
        image = ttk.Label(self, image=self.photo)
        image.pack(expand=True, fill=BOTH, side=TOP)

        centre(self)

    def fill(self, increment=1):
        self.progressBar["value"] += increment
        if self.progressBar["value"] <= 100:
            # read more bytes after 100 ms
            self.after(15, self.fill)
        else:
            self.close()

    def close(self):
        self.destroy()

class newUserForm(Toplevel):

    def __init__(self, master, submitNewUserForm):
        Toplevel.__init__(self, master)

        self.wm_title("New User Registration:")
        self.tkraise(aboveThis=master)
        self.resizable(width=False, height=False)
        self.wm_attributes("-topmost", True)

        frame = ttk.Frame(self, padding=10)
        frame.grid(row=0, column=0, sticky="nesw")

        intro = ttk.Label(frame, text="Welcome to Newton's Laboratory! \nPlease enter in some details..", justify=LEFT)
        intro.grid(row=0, column=0, columnspan=3, sticky="nesw")
        firstNameLabel = ttk.Label(frame, text="First Name:")
        firstNameLabel.grid(row=1, column=1, sticky="nesw", padx=5, pady=5)
        lastNameLabel = ttk.Label(frame, text="Last Name:")
        lastNameLabel.grid(row=2, column=1, sticky="nesw", padx=5, pady=5)

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
        centre(self)


    def close(self):
        self.master.focus()
        self.destroy()

class menu(ttk.Frame):
    def __init__(self, master, switchScreenTo):
        ttk.Frame.__init__(self, master, padding=10)

        master.wm_title("Newton's laboratory - Main Menu")

        itemsText = StringVar(value=(" - Generate Quiz", " - Free Simulation", " - Review Notes", " - Preferences"))

        self.grid(sticky="nesw")

        self.items = ttk.LabelFrame(self, text="Menu Items:", padding=10)
        self.items.grid(column=0, row=0, columnspan=1, rowspan=2, sticky="nesw", padx=5, pady=5)

        self.items.choices = Listbox(self.items, listvariable=itemsText, activestyle=NONE, font=headFont, width=1)
        self.items.choices.pack(fill=BOTH, expand=1)

        self.desc = ttk.LabelFrame(self, padding=10, text="Description:")
        self.desc.grid(column=0, row=1, rowspan=2, sticky="nesw", padx=5, pady=5)

        self.desc.texts = ""
        for i in range(10):
            self.desc.texts += "a "
        self.desc.l = ttk.Label(self.desc, text=self.desc.texts, justify=LEFT, wraplength=200).pack(fill=BOTH,expand=1)
        self.properties = ttk.LabelFrame(self, text="Properties:", padding = 10)
        self.properties.grid(column=2, row=0, columnspan=2, rowspan=3, sticky="nesw", padx=5, pady=5)
        self.properties.thing = Listbox(self.properties, listvariable=itemsText)
        self.properties.thing.pack(fill=BOTH, expand=1)

        self.columnconfigure(ALL, weight=3)
        self.rowconfigure(ALL, weight=1)
        master.columnconfigure(ALL, weight=3)
        master.rowconfigure(ALL, weight=1)



class window(Tk):
    def __init__(self):
        Tk.__init__(self)
        #s = ttk.Style().theme_use('clam')
        s = ttk.Style()
        s.configure(".", font=bodyFont)
        s.configure("TButton", font=buttonFont)

        self.wm_title("Newton's laboratory")
        self.wm_state("zoomed")
        self.wm_minsize(800, 500)
        self.bodyText = StringVar()
        #ttk.Label(self, textvariable = self.bodyText, padding = 10).grid(row=0, column =0)

        self.focus()
        centre(self)


