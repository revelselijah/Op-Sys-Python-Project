#!/usr/bin/env python3
from tkinter import *
from tkinter import filedialog
import os
import subprocess

# Constants
TB_WIDTH = 30
TB_HEIGHT = 6
FG = 'black'
BG = 'light gray'
ENCODING = "utf-8"
CPP_VER = ['', 'c++11', 'c++14']
initialdir = "~"
filetypes = [("C/C++ Files", "*.c *.cpp *.h *.hpp"), ("All Files", "*.*")]

root = Tk()
root.title("C++ Compiler")
root.resizable(False, False)
filenames = ("",)
outfile = ""
cppver = StringVar()
cppver.set("")
command = ["g++", "-pass-exit-codes", "", "-o", ""]

def importFile():
    global filenames
    filenameStr = filedialog.askopenfilenames(initialdir=initialdir, title="Please select files", filetypes=filetypes)
    
    if filenameStr == "":
        consoleText.config(state=NORMAL)
        consoleText.delete("1.0", END)
        consoleText.insert(END, "No file selected.\n")
        consoleText.see(END)
        consoleText.config(state=DISABLED)
    else:
        filenames += root.tk.splitlist(filenameStr)
        if filenames[0] == "":
            filenames = filenames[1:]
        selectedFiles.config(state=NORMAL)
        selectedFiles.delete("1.0", END)
        selectedFiles.insert(END, "\n".join(filenames))
        consoleText.see(END)
        selectedFiles.config(state=NORMAL)

        if cppver.get() != "":
            startButton.config(state=NORMAL)

def clearFile():
    global filenames
    selectedFiles.config(state=NORMAL)
    selectedFiles.delete("1.0", END)
    selectedFiles.config(state=DISABLED)
    filenames = ("",)
    consoleText.config(state=NORMAL)
    consoleText.delete("1.0", END)
    consoleText.insert(END, "Please select a file.\n")
    consoleText.see(END)
    consoleText.config(state=DISABLED)
    startButton.config(state=DISABLED)

def addDebug():
    global command
    if debug.get() == 0:
        command = command[0:(len(command)-1)]
    else:
        command.append("-g")

def setVer(cppver):
    global command
    consoleText.config(state=NORMAL)
    
    if cppver != "":
        consoleText.delete("1.0", END)
        consoleText.insert(END, "GCC set up for " + cppver + "\n")
        consoleText.see(END)

        command[2] = "-std=" + cppver
        
        if filenames != ("",):
            startButton.config(state=NORMAL)
    else:
        consoleText.delete("1.0", END)
        consoleText.insert(END, "Please select c++ version.\n")
        consoleText.see(END)
        startButton.config(state=DISABLED)
        
    consoleText.config(state=DISABLED)

def runGCC():
    global outfile, cppver, command

    startButton.config(state=DISABLED)
    
    outfile = outfileTextbox.get("1.0","end-1c")
    outfile.rstrip()
    command[4] = outfile
    command.extend(filenames)
    
    
    consoleText.config(state=NORMAL)
    consoleText.delete("1.0", END)
    for i in range(0, len(command)):
        consoleText.insert(END, command[i])
        consoleText.insert(END, " ")
    consoleText.insert(END, "\n")

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    if output.decode(ENCODING) == "" and error.decode(ENCODING) == "":
        consoleText.insert(END, "SUCCESS!\n")
        consoleText.see(END)
    else:
        consoleText.insert(END, output.decode(ENCODING))
        consoleText.see(END)

    errorText.config(state=NORMAL)
    errorText.delete("1.0", END)
    errorText.insert(END, error.decode(ENCODING))
    errorText.config(state=DISABLED)
    
    consoleText.config(state=DISABLED)
    
frame = Frame(root, bg='light gray')
frame.grid(padx=1, pady=1)

# Console Output
consoleLabel = Label(frame, text='Console', fg=FG, bg=BG)
consoleLabel.grid(row=7, column=0, columnspan=3)

consoleText = Text(frame, width=TB_WIDTH+30, height=TB_HEIGHT, state=DISABLED, fg=FG, bg=BG)
consoleText.grid(row=8, column=0, padx=10, pady=0, columnspan=3)

errorLabel = Label(frame, text='Errors', fg=FG, bg=BG)
errorLabel.grid(row=7, column=3, columnspan=3)

errorText = Text(frame, width=TB_WIDTH+30, height=TB_HEIGHT, state=DISABLED, fg=FG, bg=BG)
errorText.grid(row=8, column=3, padx=10, pady=0, columnspan=3)

# Input File(s)
inputLabel = Label(frame, text='Input File(s):', fg=FG, bg=BG)
inputLabel.grid(row=1, column=1, padx=5, rowspan = 2, sticky=E)

selectedFiles = Text(frame, width=TB_WIDTH*2, height=TB_HEIGHT, state=DISABLED, fg=FG, bg=BG)
selectedFiles.see("end")
selectedFiles.grid(row=1,column=2, padx=5, pady=10, columnspan=2, rowspan=2)

inputButton = Button(frame, text='Select Files', fg=FG, bg=BG, command=importFile)
inputButton.grid(row=1, column=4, padx=5, sticky=W)

clearButton = Button(frame, text='Clear Files', fg=FG, bg=BG, command=clearFile)
clearButton.grid(row=2, column=4, padx=5, sticky=W)

# Output File
outfileLabel = Label(frame, text='Output File:', fg=FG, bg=BG)
outfileLabel.grid(row=3, column=1, padx=5, sticky=E)

outfileTextbox = Text(frame, width=TB_WIDTH, height=1)
outfileTextbox.grid(row=3, column=2, padx=5, pady=10)

# Options
optionsLabel = Label(frame, text='Options:', fg=FG, bg=BG)
optionsLabel.grid(row=4, column=1, padx=5, rowspan=2, sticky=E)

debug = IntVar()
debugOption = Checkbutton(frame, text = "Debugging?", variable=debug, command=addDebug, fg=FG, bg=BG)
debugOption.grid(row=4, column=2, padx=5, pady=10, rowspan=2)

versionLabel = Label(frame, text='C++ Version', fg=FG, bg=BG)
versionLabel.grid(row=4, column=3, padx=10)

versionBox = OptionMenu(frame, cppver, *CPP_VER, command=setVer)
versionBox.grid(row=5, column=3, padx=5, pady=5)

# Start Compiling
startButton = Button(frame, text='COMPILE', fg=FG, bg=BG, command=lambda:runGCC(), state=DISABLED)
startButton.grid(row=6, column=1, pady=10, columnspan=4)

# Startup GUI
root.mainloop()
