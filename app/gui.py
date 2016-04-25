from tkinter import *
from tkinter import ttk, messagebox, filedialog

import app.questions as questions

headFont = ("Helvetica", 20, "bold")
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

        try:
            from PIL import Image, ImageTk

            w = self.winfo_screenwidth()
            load = Image.open("assets/images/splash.png")
            ratio = (w // 2) / load.width
            load = load.resize((w // 2, int(load.height * ratio)), Image.ANTIALIAS)
            # self["width"] = w//2
            # self["height"] = load.height
            self.photo = ImageTk.PhotoImage(load)
            image = ttk.Label(self, image=self.photo)
            image.pack(expand=True, fill=BOTH, side=TOP)

        except ImportError:
            print('Please install PIL library to view splash')

        self.protocol("WM_DELETE_WINDOW", doNotClose)
        self.wm_attributes("-topmost", True)
        self.wm_overrideredirect(True)

        self.progressBar = ttk.Progressbar(self, orient=HORIZONTAL, mode="determinate")
        self.progressBar.pack(expand=True, side=BOTTOM, fill=BOTH)

        centre(self)

    def fill(self, increment=5):
        self.progressBar["value"] += increment
        if self.progressBar["value"] <= 100:
            self.after(15, self.fill) # Recursive call
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
    def __init__(self, master):
        ttk.Frame.__init__(self, master, padding=10)

        master.wm_title("Newton's laboratory - Main Menu")

        itemsText = StringVar(value=(" - Generate Quiz", " - Free Simulation", " - Review Notes", " - Preferences"))

        self.grid(sticky="nesw")

        self.items = ttk.LabelFrame(self, text="Menu Items:", padding=10)
        self.items.grid(column=0, row=0, columnspan=2, rowspan=3, sticky="nesw", padx=5, pady=5)

        self.choice = StringVar
        self.items.choices = Listbox(self.items, listvariable=itemsText, activestyle=NONE, font=headFont)
        self.items.choices.pack(fill=BOTH, expand=1)

        self.desc = ttk.LabelFrame(self.items, padding=10, text="Description:")
        self.desc.pack(fill=BOTH, expand=1)

        self.desc.text = Text(self.desc, font=bodyFont, state=DISABLED, wrap=WORD)
        self.desc.text.pack(fill=BOTH,expand=1)
        self.properties = ttk.LabelFrame(self, text="Properties:", padding = 10)
        self.properties.grid(column=2, row=0, columnspan=1, rowspan=3, sticky="nesw", padx=5, pady=5)

        self.columnconfigure(ALL, weight=1)
        self.rowconfigure(ALL, weight=1)
        master.columnconfigure(ALL, weight=1)
        master.rowconfigure(ALL, weight=1)
        
        self.items.choices.bind('<<ListboxSelect>>', self.select)
        self.items.choices.selection_set(0)

    def createProperties(self, generateQuiz, startQuiz, startSim):
        # Quiz
        self.properties.quiz = quiz = ttk.Frame(self.properties)
        quiz.pack(fill=BOTH, expand=1)
        quiz.generateQuiz = generateQuiz
        topics = ttk.LabelFrame(self.properties.quiz, text="Topics to cover:", padding=10)
        topics.grid(column=0, row=0, columnspan=2, rowspan=3, padx=5, pady=5, sticky="nesw")

        quiz.topic1 = BooleanVar(value=True)
        quiz.topic2 = BooleanVar(value=True)
        quiz.topic3 = BooleanVar(value=True)
        quiz.topic4 = BooleanVar(value=False)
        quiz.topic5 = BooleanVar(value=True)
        quiz.isTimed = BooleanVar(value=True)
        quiz.giveHints = BooleanVar(value=True)
        quiz.noOfQuestions = IntVar(value=20)
        quiz.difficulty = IntVar(value=2)
        quiz.preview = StringVar(value="")

        ttk.Checkbutton(topics, text="Motion", var=quiz.topic1, command=generateQuiz).pack(fill=BOTH, expand=1)
        ttk.Checkbutton(topics, text="Forces & Vectors", var=quiz.topic2, command=generateQuiz).pack(fill=BOTH, expand=1)
        ttk.Checkbutton(topics, text="Work, Energy & Power", var=quiz.topic3, command=generateQuiz).pack(fill=BOTH, expand=1)
        ttk.Checkbutton(topics, text="Materials", var=quiz.topic4, command=generateQuiz).pack(fill=BOTH, expand=1)
        ttk.Checkbutton(topics, text="Newton's laws & Momentum", var=quiz.topic5, command=generateQuiz).pack(fill=BOTH, expand=1)

        quiz.questions = ttk.LabelFrame(quiz, text="The questions are:", padding=10)
        quiz.questions.grid(column=2, row=0, columnspan=2, rowspan=10, padx=5, pady=5, sticky="nesw")

        ttk.Label(quiz.questions, textvariable=quiz.preview, width=50).pack(fill=BOTH, side=TOP)

        ttk.Label(quiz, text="Difficulty:").grid(column=0, row=3, sticky="e")
        ttk.Scale(quiz, from_=1, to=3, orient=HORIZONTAL, variable=quiz.difficulty, command=generateQuiz).grid(column=1, row=3, sticky="w", pady=10)

        ttk.Label(quiz, text="Number of questions:").grid(column=0, row=4, sticky="e")
        spinBox = Spinbox(quiz, textvariable=quiz.noOfQuestions, from_=1, to=50, font=bodyFont, width=2,
                          command=generateQuiz)
        spinBox.grid(column=1, row=4, sticky="w", pady=10)
        spinBox.bind("<Key>", generateQuiz)

        ttk.Checkbutton(quiz, text="Timed", var=quiz.isTimed).grid(column=1, row=5, sticky="sw")
        ttk.Checkbutton(quiz, text="Give Hints", var=quiz.giveHints).grid(column=1, row=6, sticky="nw")

        quiz.start = ttk.Button(quiz, text="START!", command=startQuiz).grid(column=0, row=5, rowspan=2, padx=10, pady=10, sticky="nesw")

        self.properties.sim = sim = ttk.Frame(self.properties)
        sim.visual = BooleanVar(value=True)
        sim.G = StringVar(value="0.00000000006674")
        sim.airResistance = BooleanVar(value=False)
        sim.steps = StringVar(value=32)

        ttk.Checkbutton(sim, text="Visual simulation", var=sim.visual).pack(anchor="w", pady=5)
        ttk.Checkbutton(sim, text="Air resistance", var=sim.airResistance).pack(anchor="w", pady=5)

        ttk.Label(sim, text="Value of G:").pack(anchor="sw", pady=5)
        ttk.Entry(sim, textvariable=sim.G).pack(anchor="nw", pady=5)
        ttk.Label(sim, text="Steps").pack(anchor="sw", pady=5)
        ttk.Entry(sim, textvariable=sim.steps).pack(anchor="nw", pady=5)
        ttk.Button(sim, text="START!", command=startSim).pack(anchor="w", pady=5)

        return



    def setDescription(self, text):
        self.desc.text["state"] = NORMAL
        self.desc.text.delete("1.0", END)
        self.desc.text.insert(END, text)
        self.desc.text["state"] = DISABLED

    def select(self, event=None):
        choice = self.items.choices.curselection()[0]
        self.properties.quiz.pack_forget()
        self.properties.sim.pack_forget()
        if choice == 0:
            self.properties.quiz.pack()
            self.setDescription("Generate a random set of questions based on your configuration")
        elif choice == 1:
            self.properties.sim.pack()
            self.setDescription("Start a 2D-physics simulation environment for experiments and demonstrations")
        elif choice == 2:
            self.setDescription("View notes and explanations on select topics")
        elif choice == 3:
            self.setDescription("Modify global settings for the application")

class quizFrame(ttk.Frame):
    def __init__(self, master, quiz):
        ttk.Frame.__init__(self, master, padding=10)

        self.master.menu.grid_forget()

        self.quiz = quiz
        self.questionText = Text(self, font=bodyFont, padx= 10, pady=10,  state="disabled", height=3, wrap=WORD)

        master.wm_title("Newton's laboratory - Quiz")

        self.grid(sticky="new")

        toolbar = self.toolbar = ttk.LabelFrame(self, text="Toolbar", padding=10)
        toolbar.pack(fill=X)

        ttk.Button(toolbar, text="\u2190 Back", command=lambda: self.ask(quiz.questionSet[quiz.index - 1])).grid(
            row=0, column=0, rowspan=1, columnspan=1, sticky="nw", padx=10)

        self.timeLeft = Variable(value=str(self.quiz.time)+" seconds remaining")

        ttk.Label(toolbar, textvariable=self.timeLeft).grid(
            row=1, column=0, rowspan=1, columnspan=3, padx=10)

        ttk.Button(toolbar, text="Hint", command=self.showHint, state=(DISABLED, ACTIVE)[self.quiz.showHints]).grid(
            row=0, column=4, rowspan=1, columnspan=1, padx=10)

        self.markButton = ttk.Button(toolbar, text="Mark", command=self.mark)
        self.markButton.grid(row=0, column=5, rowspan=1, columnspan=1, padx=10)

        ttk.Button(toolbar, text="Next \u2192", command=lambda: self.ask(quiz.questionSet[quiz.index + 1])).grid(
            row=0, column=6, rowspan=1, columnspan=2, padx=10)

        ttk.Button(toolbar, text="Save", command=self.save).grid(
            row=0, column=8, rowspan=1, columnspan=1, padx=10)

        ttk.Button(toolbar, text="Load", command=self.load).grid(
            row=0, column=9, rowspan=1, columnspan=1, padx=10)

        self.questionText.pack(fill=X, side=TOP)

        self.responseArea = ttk.LabelFrame(self, text="Your Response")
        self.responseArea.pack(fill=BOTH, side=TOP)

        self.ask(self.quiz.questionSet[self.quiz.index])

        if not self.quiz.time == '\u221E':
            self.after(1000, self.countdown)

    def update(self):
        question = self.quiz.questionSet[self.quiz.index]
        try:
            if isinstance(question, questions.Qualitative):
                question.response = self.responseArea.response.get(1.0, END)
                print(question.response)
            elif isinstance(question, questions.MultipleChoice):
                selection = self.responseArea.options.curselection()[0]
                question.response = question.options[selection]
        except AttributeError:
            pass  # When widgets are first created

    def ask(self, question):

        self.update()

        for child in self.responseArea.winfo_children():
            child.destroy()

        self.quiz.index = self.quiz.questionSet.index(question)
        self.questionText["state"] = NORMAL
        self.questionText.delete("1.0", END)
        self.questionText.insert(END, str(self.quiz.index+1)+") "+str(question)+"\n("+str(question.maxMarks)+" marks)")
        self.questionText["state"] = DISABLED

        if question.isMarked:
            self.markButton["state"] == DISABLED
        else:
            self.markButton["state"] == ACTIVE

        if isinstance(question, questions.Qualitative):
            self.responseArea.response = Text(self.responseArea, font=bodyFont, padx=10, pady=10,
                                              height=question.marks * 3, wrap=WORD)
            if question.response is not None:
                self.responseArea.response.insert(END, question.response)
                print(self.responseArea.response.get(1.0, END))
            self.responseArea.response.pack(fill=BOTH, expand=1, padx=10, pady=10)
        elif isinstance(question, questions.MultipleChoice):
            self.responseArea.optionsText = Variable(value=tuple(question.options))
            self.responseArea.options = Listbox(
                self.responseArea, listvariable=self.responseArea.optionsText, font=headFont,
                height=len(question.options))
            if question.response is not None:
                self.responseArea.options.selection_set(question.options.index(question.response))
            else:
                self.responseArea.options.selection_set(0)
            self.responseArea.options.pack(fill=BOTH, expand=1, padx=10, pady=10)
        elif isinstance(question, questions.Qualitative):
            self.responseArea.response = ttk.Entry(self.responseArea, width=7)
            self.responseArea.response.pack(expand=1, padx=10, pady=10)

        if question.isMarked:
            self.mark()

    def countdown(self):
        if not self.quiz.completed:
            if self.quiz.time > 0:
                self.quiz.time -= 1
                self.timeLeft.set(str(self.quiz.time) + " seconds remaining")
                self.after(1000, self.countdown)
            else:
                self.finished()

    def showHint(self):
        if self.quiz.showHints:
            messagebox.showinfo(
                "Hint",
                self.quiz.questionSet[self.quiz.index].hint
            )

    def mark(self):

        self.update()

        question = self.quiz.questionSet[self.quiz.index]

        self.answerArea = ttk.LabelFrame(self.responseArea, text="Result:")
        self.answerArea.pack(fill=BOTH, expand=1, padx=10, pady=10)

        if isinstance(question, questions.Qualitative):
            self.responseArea.response["state"] = DISABLED
            marks = question.mark(self.responseArea.response.get(1.0, END))

            answer = Text(self.answerArea, font = bodyFont, padx = 10, pady = 10, height = 6, wrap = WORD)
            answer.pack(fill=BOTH, expand=1, padx=10, pady=10)
            answer.insert(END, question.answer)
            ttk.Label(self.answerArea, text="You scored "+str(question.marks)+" out of "+str(question.maxMarks)).pack(
                fill=BOTH, side=BOTTOM, expand=1, padx=10, pady=10)
            answer["state"] = DISABLED
            question.isMarked = True

        elif isinstance(question, questions.MultipleChoice):
            selection = self.responseArea.options.curselection()[0]
            response = question.options[selection]
            if '\u0336' in self.responseArea.optionsText.get()[selection]:
                return
            elif question.mark(response) != -1:
                self.responseArea.options["state"] = DISABLED
                optionsText = list(self.responseArea.optionsText.get())
                text = optionsText[question.options.index(question.answer)]
                text += ' \u2714'  # tick sign
                optionsText[question.options.index(question.answer)] = text
                self.responseArea.optionsText.set(tuple(optionsText))
                ttk.Label(self.answerArea, text="You scored " + str(question.marks) + " out of " + str(question.maxMarks)).pack(
                    fill=BOTH, side=BOTTOM, expand=1, padx=10, pady=10)
                question.isMarked = True
            else:
                optionsText =  list(self.responseArea.optionsText.get())
                text = optionsText[selection]
                text = '\u0336'.join(text) + '\u0336' #strikethrough
                optionsText[selection] = text
                question.options[selection] = text
                self.responseArea.optionsText.set(tuple(optionsText))

        elif isinstance(question, questions.Qualitative):
            self.responseArea.response = ttk.Entry(self.responseArea, width=7)
            self.responseArea.response.pack(expand=1, padx=10, pady=10)

        if self.quiz.numberAnswered() == len(self.quiz.questionSet):
            self.finished()

    def save(self):
        with filedialog.asksaveasfile(mode="wb", initialfile='untitled', defaultextension='quiz',
                                      filetypes=[("Newton's Laboratory Quiz File", ".quiz")]) as quizFile:
            self.quiz.save(quizFile)

    def load(self):
        with filedialog.askopenfile(mode="rb", filetypes=[("Newton's Laboratory Quiz File", ".quiz")]) as quizFile:
            self.quiz = self.quiz.load(quizFile)
        self.quiz.index = 0
        self.ask(self.quiz.questionSet[0])

    def finished(self):
        if self.quiz.completed:
            return
        messagebox.showinfo(
            "Quiz Results",
            "Your total score for this quiz is:\n"+str(self.quiz.score())+" out of "+str(self.quiz.maxScore())
        )
        self.quiz.completed = True
        self.save()
        self.master.menu.grid()
        self.master.menu.properties.quiz.generateQuiz()
        self.destroy()

class window(Tk):
    def __init__(self):
        Tk.__init__(self)
        #s = ttk.Style().theme_use('clam')
        s = ttk.Style()
        s.configure(".", font=bodyFont)
        s.configure("TButton", font=buttonFont)

        self.wm_title("Newton's laboratory")
        self.wm_state("zoomed")
        self.wm_minsize(700, 500)
        self.bodyText = StringVar()
        #ttk.Label(self, textvariable = self.bodyText, padding = 10).grid(row=0, column =0)

        iconImg = PhotoImage(file='assets/images/icon.png')
        self.tk.call('wm', 'iconphoto', self._w, iconImg)

        self.focus()
        centre(self)
