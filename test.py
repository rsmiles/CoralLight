#!/usr/bin/env python3

import AGRRA
from tkinter import *
from tkinter import filedialog


root = Tk()
mesg = Label(root, text='¡Hola Mundo!')
mesg.pack()
fname  = filedialog.askopenfilename(initialdir='.', title='Select a File')
root.mainloop()

