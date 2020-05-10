"""
AppOpener Project to open apps (duh)
Version 1.0
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

# Functions

class Profile():
    def __init__(self, name, num, profile=None):
        self.name = name
        self.num = num
        if profile is None:
            self.profile = "settings" + str(self.num)
        else:
            self.profile = profile



def addApp():
    for widget in frame.winfo_children():
        widget.destroy()

    filename = filedialog.askopenfilename(initialdir="/", title="Select Apps to Open", filetypes=(("Executables(*.exe)", "*.exe"), ("All Files(*.*)", "*.*")))
    if len(filename) > 0:
        apps.append(filename)
    x = 0
    for app in apps:
        tempApp = app.split("/")
        tempApp = tempApp[-1][:-4].capitalize()
        label = tk.Label(frame, text=tempApp)
        label.place(relx=0.4, rely=0.08 * x)
        button = tk.Button(frame, text="Run", command=lambda x=x: openSingleApp(x))
        button.place(relx=0.7, rely= 0.08 * x)
        x += 1


def runApp():
    if apps:
        for app in apps:
            os.startfile(app)
    else:
        messagebox.showinfo("", "There are no apps to run!")


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
    messagebox.showinfo("About", "App Opener v1.0\nBy Aidan Shanley :)")


def myhelp():
    messagebox.showinfo("Help", "Click 'Select Apps' and choose an app to run.\nIt'll be added to a list on screen and "
                                "you can add as many as you want.\nClick on 'Run' beside any app name to run that app."
                                "\nClick 'Run Apps' to run all the apps.")


def addProfile():
    global top
    top = tk.Toplevel()
    top.title("Add Profile")
    top.resizable(False, False)
    nameLabel = tk.Label(top, text="Profile Name:")
    nameLabel.pack()
    input = tk.Entry(top, textvariable=tk.StringVar)
    input.pack()
    profileName.append(input)
    submitButton = tk.Button(top, text="Submit", command=createProfile)
    submitButton.pack()
    top.mainloop()


def createProfile():
    profile_name = profileName[-1].get()  # the text in the entry field for adding new profile
    print(profile_name)
    tempProfile = Profile(profile_name, len(profiles))  # creates a Profile object
    profiles.append(tempProfile)  # appends the Profile object to the profiles list
    top.destroy()


def selectProfile():
    pass


# Root app
root = tk.Tk()
root.title("App Opener")

# Makes window static size
root.resizable(False, False)

menu = tk.Menu(root)

profileMenu = tk.Menu(menu, tearoff=0)
profileMenu.add_separator()
profileMenu.add_command(label="Add New Profile", command=addProfile)

# menu.add_cascade(label="Profiles", menu=profileMenu)
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

openApps = tk.Button(root, text="Select Apps", padx=10, pady=5, command=addApp)
openApps.place(relx=0.2, rely=0.915)

runApps = tk.Button(root, text="Run Apps", padx=10, pady=5, command=runApp)
runApps.place(relx=0.41, rely=0.915)

clearApps = tk.Button(root, text="Clear Apps", padx=10, pady=5, command=clear)
clearApps.place(relx=0.6, rely=0.915)

# Runs app
root.mainloop()

if apps:
    with open("settings.txt", "w", newline="") as file:
        write = csv.writer(file)
        write.writerow(apps)
