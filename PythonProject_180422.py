#!/usr/bin/env python3
from tkinter import *
import os

TB_WIDTH = 30
TB_HEIGHT = 6
FG = 'black'
BG = 'light gray'
CPP_VER = ['', 'c++11', 'c++14']
initialdir = "~"
filetypes = [("C/C++ Files", "*.c *.cpp *.h *.hpp"), ("All Files", "*.*")]

root = Tk()
root.title("C++ Compiler")
root.resizable(False, False)
filenames = ""

def importFile():
    global filenames
    selectedFiles.config(state=NORMAL)
    selectedFiles.delete("1.0", END)
    selectedFiles.config(state=DISABLED)
    filenameStr = filedialog.askopenfilenames(initialdir=initialdir, title="Please select files", filetypes=filetypes)
    
    if filenameStr == "":
        consoleText.config(state=NORMAL)
        consoleText.insert(END, "No file selected.\n")
        consoleText.see(END)
        consoleText.config(state=DISABLED)
        startButton.config(state=DISABLED)
    else:
        filenames = root.tk.splitlist(filenameStr)
        selectedFiles.config(state=NORMAL)
        selectedFiles.insert(END, "\n".join(filenames))
        consoleText.see(END)
        selectedFiles.config(state=NORMAL)
        if cppver.get() != "":
            startButton.config(state=NORMAL)

def setupGCC(cppver):
    consoleText.config(state=NORMAL)
    if cppver != "":
        consoleText.insert(END, "GCC set up for " + cppver + "\n")
        consoleText.see(END)
        if filenames != "":
            startButton.config(state=NORMAL)
    else:
        consoleText.insert(END, "Please select c++ version.\n")
        consoleText.see(END)
        startButton.config(state=DISABLED)
        
    consoleText.config(state=DISABLED)

def runGCC():
    consoleText.config(state=NORMAL)
    consoleText.insert(END, "GCC is running...\n")
    consoleText.see(END)
    consoleText.config(state=DISABLED)

frame = Frame(root, bg='light gray')
frame.grid(padx=1, pady=1)


# Console Output
consoleLabel = Label(frame, text='Console', fg=FG, bg=BG)
consoleLabel.grid(row=6, column=1, columnspan=2)

consoleText = Text(frame, width=TB_WIDTH, height=TB_HEIGHT, state=DISABLED, fg=FG, bg=BG)
consoleText.grid(row=7, column=1, padx=10, pady=0, columnspan=2)

errorLabel = Label(frame, text='Errors', fg=FG, bg=BG)
errorLabel.grid(row=6, column=3, columnspan=2)

errorText = Text(frame, width=TB_WIDTH, height=TB_HEIGHT, state=DISABLED, fg=FG, bg=BG)
errorText.grid(row=7, column=3, padx=10, pady=0, columnspan=2)

# Start Compiling
startButton = Button(frame, text='COMPILE', fg=FG, bg=BG, command=lambda:runGCC(), state=DISABLED)
startButton.grid(row=5, column=1, pady=10, columnspan=4)

# Input File(s)
inputLabel = Label(frame, text='Input File(s):', fg=FG, bg=BG)
inputLabel.grid(row=1, column=1, padx=5)

selectedFiles = Text(frame, width=TB_WIDTH+15, height=TB_HEIGHT, state=DISABLED, fg=FG, bg=BG)
selectedFiles.see("end")
selectedFiles.grid(row=1,column=2, padx=5, pady=10, columnspan=2)

inputButton = Button(frame, text='Select Files', fg=FG, bg=BG, command=importFile)
inputButton.grid(row=1, column=4, padx=5)

# Output File
outfileLabel = Label(frame, text='Output File:', fg=FG, bg=BG)
outfileLabel.grid(row=2, column=1, padx=5)

outfileTextbox = Text(frame, width=TB_WIDTH, height=1)
outfileTextbox.grid(row=2, column=2, padx=5, pady=10)

# Options
optionsLabel = Label(frame, text='Options:', fg=FG, bg=BG)
optionsLabel.grid(row=3, column=1, padx=5, rowspan=2)

debug = IntVar()
debugOption = Checkbutton(frame, text = "Debugging?", variable=debug, fg=FG, bg=BG)
debugOption.grid(row=3, column=2, padx=5, pady=10, rowspan=2)

versionLabel = Label(frame, text='C++ Version', fg=FG, bg=BG)
versionLabel.grid(row=3, column=3, padx=10)

cppver = StringVar()
cppver.set("")
versionBox = OptionMenu(frame, cppver, *CPP_VER, command=setupGCC)
versionBox.grid(row=4, column=3, padx=5, pady=5)

# Startup GUI
root.mainloop()
