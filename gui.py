from app_info import *
from libcorallight import *
import tkinter as tk
import tkinter.messagebox as tk_messagebox
import os

class MainWindow():
	def __init__(self):
		self.root = tk.Tk()
		self.root.title('{0} ({1})'.format(APP_NAME, APP_VERSION))
		self.initUI()

	def initUI(self):
		self.menuBar = tk.Menu(self.root)

		self.coralLightMenu = tk.Menu(self.menuBar, tearoff=False)
		self.coralLightMenu.add_command(label='Quit ' + APP_NAME, command=self.quit, accelerator='Ctrl+Q')
		self.menuBar.add_cascade(label=APP_NAME, menu=self.coralLightMenu)

		self.dataMenu = tk.Menu(self.menuBar, tearoff=False)
		self.dataMenu.add_command(label='New Database', command=self.new_database, accelerator='Ctrl+Shift+N')
		self.dataMenu.add_command(label='Open Database', command=self.open_database, accelerator='Ctrl+O')
		self.dataMenu.add_command(label='Import Data', command=self.import_data, accelerator='Ctrl+I')
		self.dataMenu.add_command(label='Show Current Database', command=self.show_current_database, accelerator='Ctrl+D')
		self.menuBar.add_cascade(label='Data', menu=self.dataMenu)

		# Setup keyboard shortcuts
		self.root.bind_all('<Control-q>', self.quit)

		self.root.bind('<Control-w>', self.quit)
		self.root.bind('<Control-Shift-N>', self.new_database)
		self.root.bind('<Control-o>', self.open_database)
		self.root.bind('<Control-i>', self.import_data)
		self.root.bind('<Control-d>', self.show_current_database)

		self.root.config(menu=self.menuBar)

	def exec_str(self, string):
		try:
			exec_str(string)
		except Exception as e:
			tk_messagebox.showerror('Error', str(e))

	def quit(self, event=None):
		self.root.destroy()

	def show_current_database(self, event=None):
		tk_messagebox.showinfo(title='Current Database', message=agrra.config.DB)

	def new_database(self, event=None):
		fileName = tk.filedialog.asksaveasfilename()
		if not fileName:
			return

		elif os.path.isfile(fileName):
			os.remove(filename)
		self.exec_str('@opendb {0};'.format(fileName))

	def open_database(self, event=None):
		fileName = tk.filedialog.askopenfilename()
		if not fileName:
			return

		self.exec_str('@opendb {0};'.format(fileName))

	def import_data(self, event=None):
		fileNames = tk.filedialog.askopenfilenames()
		for fileName in fileNames:
			self.exec_str('@import {0};'.format(fileName))

	def run(self):
		self.root.mainloop()

