"""
AppOpener Project to open apps (duh)
Version 0.2.0
By Aidan Shanley
"""

# Imports
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import csv

# Initialising Variables
apps = []
profiles = []
profileName = []
defaultProfile = None

# Functions


class Profile:
    def __init__(self, name, num, apps_in=None):
        self.name = name
        self.num = num
        if apps_in is None:
            self.apps = []
        else:
            self.apps = apps_in

    def select(self):
        global defaultProfile
        defaultProfile = self

    def addApps(self, apps_in):
        if apps_in:
            self.apps = apps_in


def addApp():
    for widget in frame.winfo_children():
        widget.destroy()

    filename = filedialog.askopenfilename(initialdir="/", title="Select Apps to Open", filetypes=(("Executables(*.exe)",
                                                                                                   "*.exe"), ("All File"
                                                                                                              "s(*.*)",
                                                                                                              "*.*")))
    if len(filename) > 0:
        apps.append(filename)
    x = 0
    for app in apps:
        tempApp = app.split("/")
        tempApp = tempApp[-1][:-4].capitalize()
        label = tk.Label(frame, text=tempApp)
        label.place(relx=0.4, rely=0.08 * x)
        button = tk.Button(frame, text="Run", command=lambda x=x: openSingleApp(x))
        button.place(relx=0.7, rely=0.08 * x)
        x += 1


def runApp():
    for app in apps:
        os.startfile(app)


def clear():
    for i in range(len(apps)):
        for app in apps:
            apps.remove(app)
        for widget in frame.winfo_children():
            widget.destroy()
        if os.path.exists("settings.txt"):
            os.remove("settings.txt")
    messagebox.showinfo("", "App list cleared!")


def openSingleApp(index):
    os.startfile(apps[index])


def about():
    messagebox.showinfo("About", "App Opener v0.2.0\nBy Aidan Shanley :)")


def myhelp():
    messagebox.showinfo("Help", "- Click 'Select Apps' and choose an app to run.\nIt'll be added to a list on screen an"
                                "d you can add as many as you want.\n- Click on 'Run' beside any app name to run that "
                                "app."
                                "\n- Click 'Run Apps' to run all the apps."
                                "\n- Use the 'Profiles' option to save and load different presets.")


def addProfile():
    global top
    top = tk.Toplevel()
    top.title("Add Profile")
    top.resizable(False, False)
    nameLabel = tk.Label(top, text="Profile Name(Can't be blank):")
    nameLabel.pack()
    input = tk.Entry(top, textvariable=tk.StringVar)
    input.pack()
    profileName.append(input)
    submitButton = tk.Button(top, text="Submit", command=createProfile)
    submitButton.pack()
    top.mainloop()


def createProfile():
    check = []
    profile_name = profileName[-1].get()
    if len(profile_name) > 0:
        for profile in profiles:
            if profile.name != profile_name:
                check.append(True)
            else:
                check.append(False)
        if False not in check:
            tempProfile = Profile(profile_name, len(profiles), apps)  # creates a Profile object
            profiles.append(tempProfile)  # appends the Profile object to the profiles list
    top.destroy()


def selectProfile():
    if profiles:
        global top
        top = tk.Toplevel()
        top.title("Select Profile")
        top.minsize(200, 200)
        top.resizable(False, False)
        label = tk.Label(top, text="Choose a profile:")
        label.pack()
        x = 0
        for profile in profiles:
            label = tk.Label(top, text="- " + profile.name)
            label.place(relx=0.35, rely=0.15 * (x + 1))
            selectButton = tk.Button(top, text="Select", command=lambda x=x: makeDefaultActive(x))
            selectButton.place(relx=0.7, rely=0.15 * (x + 1))
            x += 1
    else:
        messagebox.showinfo("Error", "There are no profiles, please create one.")


def makeDefaultActive(index):
    global defaultProfile, apps, top
    top.destroy()
    defaultProfile = profiles[index]
    apps = defaultProfile.apps
    for widget in frame.winfo_children():
        widget.destroy()
    if apps:
        x = 0
        for app in apps:
            tempApp = app.split("/")
            tempApp = tempApp[-1][:-4].capitalize()
            label = tk.Label(frame, text=tempApp)
            label.place(relx=0.4, rely=0.08 * x)
            button = tk.Button(frame, text="Run", command=lambda x=x: openSingleApp(x))
            button.place(relx=0.7, rely=0.08 * x)
            x += 1


def loadDefault(index):
    global apps
    apps = profiles[index].apps
    x = 0
    for app in apps:
        tempApp = app.split("/")
        tempApp = tempApp[-1][:-4].capitalize()
        label = tk.Label(frame, text=tempApp)
        label.place(relx=0.4, rely=0.08 * x)
        button = tk.Button(frame, text="Run", command=lambda x=x: openSingleApp(x))
        button.place(relx=0.7, rely=0.08 * x)
        x += 1


def displayDelete():
    if profiles:
        global top
        top = tk.Toplevel()
        top.title("Delete Profile")
        top.minsize(200, 200)
        top.resizable(False, False)
        label = tk.Label(top, text="Choose a profile to delete:")
        label.pack()
        x = 0
        for profile in profiles:
            label = tk.Label(top, text="- " + profile.name)
            label.place(relx=0.35, rely=0.15 * (x + 1))
            button = tk.Button(top, text="Delete", command = lambda x=x: deleteProfile(x))
            button.place(relx=0.7, rely=0.15 * (x + 1))
            x += 1
    else:
        messagebox.showinfo("Error", "There are no profiles, please create one.")


def deleteProfile(profileIndex):
    global top
    deletedProfile = profiles[profileIndex]
    profiles.remove(deletedProfile)
    top.destroy()


# Root app
root = tk.Tk()
root.title("App Opener")

# Makes window static size
root.resizable(False, False)

menu = tk.Menu(root)

profileMenu = tk.Menu(menu, tearoff=0)
profileMenu.add_command(label="Select Profile", command=selectProfile)
profileMenu.add_separator()
profileMenu.add_command(label="Add New Profile", command=addProfile)
profileMenu.add_separator()
profileMenu.add_command(label="Delete a Profile", command=displayDelete)

menu.add_cascade(label="Profiles", menu=profileMenu)
menu.add_command(label="About", command=about)
menu.add_command(label="Help", command=myhelp)
menu.add_command(label="Exit", command=root.quit)
root.config(menu=menu)

canvas = tk.Canvas(root, height=500, width=500, bg="dark grey")
canvas.pack()

frame = tk.Frame(root, bg="white")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

if os.path.exists("settings.txt"):
    with open("settings.txt", "r") as file:
        apps = file.read().rstrip().split(",")
        x = 0
        for app in apps:
            tempApp = app.split("/")
            tempApp = tempApp[-1][:-4].capitalize()
            label = tk.Label(frame, text=tempApp)
            label.place(relx=0.4, rely=0.08 * x)
            button = tk.Button(frame, text="Run", command=lambda x=x: openSingleApp(x))
            button.place(relx=0.7, rely=0.08 * x)
            x += 1

if os.path.exists("profiles.txt"):
    with open("profiles.txt", "r") as file:
        tempList = file.read().rstrip().split("\n")
        for entry in tempList:
            appsList = entry[entry.index("[") + 1:entry.index("]")]
            tempAppsList = appsList.split(",")
            appsList = []
            for i in tempAppsList:
                if len(i) > 0:
                    appsList.append(i[i.index("'") + 1:-1])
            entry = entry.split(",")
            tempProfile = Profile(entry[0], entry[1], appsList)
            profiles.append(tempProfile)
        if defaultProfile is None:
            defaultProfile = 0
            loadDefault(defaultProfile)

openApps = tk.Button(root, text="Select Apps", padx=10, pady=5, command=addApp)
openApps.place(relx=0.2, rely=0.915)

runApps = tk.Button(root, text="Run Apps", padx=10, pady=5, command=runApp)
runApps.place(relx=0.41, rely=0.915)

clearApps = tk.Button(root, text="Clear Apps", padx=10, pady=5, command=clear)
clearApps.place(relx=0.6, rely=0.915)

# Runs app
root.mainloop()

if profiles:
    with open("profiles.txt", "w", newline="") as file:
        write = csv.writer(file)
        for profile in profiles:
            templist = [profile.name, profile.num, profile.apps]
            write.writerow(templist)

if apps and not profiles:
    with open("profiles.txt", "w", newline="") as file:
        write = csv.writer(file)
        tempProfile = Profile("Default", 0, apps)
        templist = [tempProfile.name, tempProfile.num, tempProfile.apps]
        write.writerow(templist)
