from app_info import *
from libcorallight import *
import tkinter as tk
import os

class MainWindow():
	def __init__(self):
		self.root = tk.Tk()
		self.initUI()

	def initUI(self):
		self.menuBar = tk.Menu(self.root)

		self.coralLightMenu = tk.Menu(self.menuBar, tearoff=False)
		self.coralLightMenu.add_command(label='Quit ' + APP_NAME, command=self.exit)
		self.menuBar.add_cascade(label=APP_NAME, menu=self.coralLightMenu)

		self.dataMenu = tk.Menu(self.menuBar, tearoff=False)
		self.dataMenu.add_command(label='New Database', command=self.new_database)
		self.dataMenu.add_command(label='Open Database', command=self.open_database)
		self.dataMenu.add_command(label='Import Data', command=self.import_data)
		self.menuBar.add_cascade(label='Data', menu=self.dataMenu)

		self.root.config(menu=self.menuBar)

	def new_database(self):
		fileName = tk.filedialog.asksaveasfilename()
		if not fileName:
			return

		elif os.path.isfile(fileName):
			os.remove(filename)
		exec_str('@opendb {0};'.format(fileName))

	def open_database(self):
		fileName = tk.filedialog.askopenfilename()
		if not fileName:
			return

		exec_str('@opendb {0};'.format(fileName))

	def import_data(self):
		fileNames = tk.filedialog.askopenfilenames()
		for fileName in fileNames:
			exec_str('@import {0};'.format(fileName))

	def run(self):
		self.root.mainloop()

	def exit(self):
		self.root.destroy()

