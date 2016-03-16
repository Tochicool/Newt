import app.gui as gui
import app.userInput as input
import os
import pickle

user = {"First Name": "",
        "Last Name": ""}

'''
splashScreen = gui.splashh()
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



splash = gui.splash()
splash.fill()
splash.mainloop()

window = gui.window()
if os.path.isfile("data/user.pickle"):
    user = pickle.load(open("data/user.pickle", "rb"))
else:
    window.newUserForm = gui.newUserForm(window, submitNewUserForm)
window.createMainMenu(None)
#window.bodyText.set("Hello %s!" %(user["First Name"]))
window.mainloop()
