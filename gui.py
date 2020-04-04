from app_info import *
from libcorallight import *
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tk_messagebox
import PIL
import os

def dataMapNames(datamap):
	return [datamap[key]['name'] for key in datamap.keys()]

def dataMapField(datamap, name):
	for val in datamap.values():
		if val['name'] == name:
			return val['key']
	return None

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
		self.dataMenu.add_command(label='New Database', command=self.new_database, accelerator='Ctrl+N')
		self.dataMenu.add_command(label='Open Database', command=self.open_database, accelerator='Ctrl+O')
		self.dataMenu.add_command(label='Import Data', command=self.import_data, accelerator='Ctrl+I')
		self.dataMenu.add_command(label='Show Current Database', command=self.show_current_database, accelerator='Ctrl+D')
		self.menuBar.add_cascade(label='Data', menu=self.dataMenu)

		self.chartMenu = tk.Menu(self.menuBar, tearoff=False)
		self.chartMenu.add_command(label='Save Chart', command=self.save_chart, accelerator='Ctrl+S')
		self.menuBar.add_cascade(label='Chart', menu=self.chartMenu)

		# Setup keyboard shortcuts
		self.root.bind_all('<Control-q>', self.quit)

		self.root.bind('<Control-w>', self.quit)
		self.root.bind('<Control-n>', self.new_database)
		self.root.bind('<Control-o>', self.open_database)
		self.root.bind('<Control-i>', self.import_data)
		self.root.bind('<Control-d>', self.show_current_database)

		self.root.config(menu=self.menuBar)

		# Setup chart generation controls

		self.displayLabel = tk.Label(self.root, width=50, height=25)
		self.displayLabel.pack(side='left')

		self.controlFrame = tk.Frame(self.root)
		self.controlFrame.pack(side='top')

		self.chartTitleLabel = tk.Label(self.controlFrame, text='Chart Title')
		self.chartTitleLabel.pack()

		self.chartTitleField = tk.Entry(self.controlFrame)
		self.chartTitleField.pack()

		self.chartTypeLabel = tk.Label(self.controlFrame, text='Chart Type')
		self.chartTypeLabel.pack()

		self.chartTypeBox = ttk.Combobox(self.controlFrame, values=('Pie', 'Bar'))
		self.chartTypeBox.pack()

		self.varLabel = tk.Label(self.controlFrame, text='Variable')
		self.varLabel.pack()

		self.varBox = ttk.Combobox(self.controlFrame, values=(dataMapNames(agrra.encounter_datamap)))
		self.varBox.pack()
		self.genButton = tk.Button(self.controlFrame, text='Generate Chart', command=self.gen_chart)
		self.genButton.pack()

	def exec_str(self, string):
		try:
			exec_str(string)
		except Exception as e:
			tk_messagebox.showerror('Error', str(e))

	def quit(self, event=None):
		self.root.destroy()

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

	def show_current_database(self, event=None):
		tk_messagebox.showinfo(title='Current Database', message=agrra.config.DB)


	def save_chart(self, event=None):
		pass

	def run(self):
		self.root.mainloop()

	def gen_chart(self):
		template = """@chart {0}
@title {1}
SELECT {2}, COUNT(*) FROM data
GROUP BY {2};"""

		chartType = self.chartTypeBox.get().lower()
		chartTitle = self.chartTitleField.get()
		chartVar = dataMapField(agrra.encounter_datamap, self.varBox.get())
		qry = template.format(chartType, chartTitle, chartVar)
		print(qry)
		self.exec_str(qry)

		newImg = PIL.ImageTk.PhotoImage(state.export.chart)
		self.displayLabel.configure(image=newImage)
		self.displayLabel.image = newImage

