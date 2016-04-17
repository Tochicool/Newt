import app.gui as gui
import app.userInput as input
import app.questions as questions
import os
import pickle
import random

user = {"First Name": "",
        "Last Name": ""}

questionSet = list(questions.questions)

'''
splashScreen = gui.splash()
splashScreen.fillBar()
splashScreen.close()
'''

def submitNewUserForm(event=None):
    fName = window.newUserForm.firstNameEntry.get()
    lName = window.newUserForm.lastNameEntry.get()
    if not input.isWord(fName):
        window.newUserForm.errorLabel['text'] = "Error: First name is not valid"
    elif not input.isWord(lName):
        window.newUserForm.errorLabel['text'] = "Error: Last name is not valid"
    else:
        window.newUserForm.errorLabel['text'] = ":)"
        user["First Name"] = fName.title()
        user["Last Name"] = lName.title()
        pickleFile = open('data/user.pickle', 'wb')
        pickle.dump(user, pickleFile, pickle.HIGHEST_PROTOCOL)
        pickleFile.close()
        window.newUserForm.destroy()
        window.bodyText.set("Hello, "+user["First Name"]+"!")

def generateQuiz(event=None):
    global questionSet

    questionSet = list(questions.questions)

    topicsSelected = [window.menu.properties.quiz.topic1.get(),
                      window.menu.properties.quiz.topic2.get(),
                      window.menu.properties.quiz.topic3.get(),
                      window.menu.properties.quiz.topic4.get(),
                      window.menu.properties.quiz.topic5.get()]

    for question in questions.questions:
        for topic in question.topics:
            if not topicsSelected[topic-1]:
                questionSet.remove(question)
                break

    #questionSet = [x for x in questionSet if isinstance(x, questions.MultipleChoice)]

    random.shuffle(questionSet)
    window.menu.properties.quiz.noOfQuestions.set(min(len(questionSet), window.menu.properties.quiz.noOfQuestions.get()))
    questionSet = questionSet[:window.menu.properties.quiz.noOfQuestions.get()]
    questionSet = sorted(questionSet, key=lambda question: question.topics[0])
    questionSet = sorted(questionSet, key=lambda question: question.marks)

    txt=""
    for i in range(len(questionSet)):
        txt += str(i + 1)+") "+str(questionSet[i])+"\n"
    window.menu.properties.quiz.preview.set(txt)


def startQuiz(event=None):
    quiz = questions.Quiz(questionSet,
                          window.menu.properties.quiz.isTimed.get(),
                          window.menu.properties.quiz.giveHints.get()
                          )
    window.quiz = gui.quizFrame(window, quiz)

splash = gui.splash()
splash.fill()
splash.mainloop()

window = gui.window()
if os.path.isfile("data/user.pickle"):
    user = pickle.load(open("data/user.pickle", "rb"))
else:
    window.newUserForm = gui.newUserForm(window, submitNewUserForm)

window.menu = gui.menu(window)
window.menu.createProperties(generateQuiz, startQuiz)
generateQuiz()
#window.bodyText.set("Hello %s!" %(user["First Name"]))

window.mainloop()

