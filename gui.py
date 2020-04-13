from app_info import *
from libcorallight import *
import tkinter as tk
import tkinter.filedialog
from tkinter import ttk, messagebox, filedialog
from PIL import ImageTk
import os

PLUGIN_DIR = agrra.config.APP_PATH + 'chart_plugins/'
TITLE_FONT = 'Helvetica 12 bold'

def displayFormat(string):
	noCap = ['the', 'for', 'by']
	noExt = os.path.splitext(string)[0]
	wordList = noExt.split('_')

	formatList = []
	for i, word in enumerate(wordList):
		if i == 0 or word not in noCap:
			formatList.append(word[0].upper() + word[1:])
		else:
			formatList.append(word)

	displayString = ' '.join(formatList)
	return displayString
	

class ParamEntry:
	def __init__(self, parent, param):
		self.parent = parent
		self.param = param
		self.initUI()

	def initUI(self):
		self.root = tk.Frame(self.parent)

		self.label = tk.Label(self.root, text=displayFormat(self.param))
		self.label.pack()

		self.addButton = tk.Button(self.root, text='+', command=self.addEntry)
		self.addButton.pack()

		self.entries = []
		self.addEntry()

	def addEntry(self, event=None):
		self.addButton.pack_forget()
		entry = tk.Entry(self.root)
		self.entries.append(entry)
		entry.pack()
		self.addButton.pack()

	def get(self):
		return "'" + "', '".join([entry.get() for entry in entries]) + "'"

	def pack(self, **opts):
		self.root.pack(**opts)

class ChartEntry:
	def __init__(self, parent, params, number):
		self.parent = parent
		self.number = number
		self.params = params
		self.initUI()

	def initUI(self):
		self.root = tk.Frame(self.parent)

		self.label = tk.Label(self.root, text='Chart ' + str(self.number), font=TITLE_FONT)
		self.label.pack()

		self.titleLabel = tk.Label(self.root, text='Title')
		self.titleLabel.pack()

		self.titleEntry = tk.Entry(self.root)
		self.titleEntry.pack()

		self.entries = []
		for param in self.params:
			entry = ParamEntry(self.root, param)
			self.entries.append(entry)
			entry.pack()

	def pack(self, **opts):
		self.root.pack(**opts)
	

class PluginInterface:
	def __init__(self, parent, name):
		self.parent = parent
		self.name = name
		self.initText()
		self.initUI()

	def initText(self):
		self.title = None
		self.description = ''
		self.params =[]
		self.textList = []
		self.numCharts = 0

		with open(PLUGIN_DIR + self.name) as plugin:
			for line in plugin:
				if line[0] == '#':
					if not self.title:
						self.title = line[1:].strip()
					else:
						self.description += line[1:].strip()
				else:
					if line[0] == '@':
						splitLine = line.split(' ')
						if splitLine[0] == '@param':
							self.params.append(line[1])
						else:
							self.textList.append(line)
					else:
						self.textList.append(line)

	def initUI(self):
		self.root = tk.Frame(self.parent)

		self.titleLabel = tk.Label(self.root, text=self.title, font=TITLE_FONT)
		self.titleLabel.pack()

		self.descriptionLabel = tk.Label(self.root, text=self.description)
		self.descriptionLabel.pack()

		self.charts = []

		self.addButton = tk.Button(self.root, text='Add Chart', command=self.addChart)
		self.addButton.pack()
	
		self.addChart()

		self.genChartButton = tk.Button(text='Generate Charts', command=self.genChart)
		self.genChartButton.pack()

	def addChart(self):
		self.addButton.pack_forget()
		self.numCharts += 1
		chart = ChartEntry(self.root, self.params, self.numCharts)
		self.charts.append(chart)
		chart.pack()
		self.addButton.pack()

	def genChart(self):
		print('gen chart!')

	def pack(self, **opts):
		self.root.pack(**opts)

class MainWindow:
	def __init__(self):
		self.root = tk.Tk()
		self.root.title('{0} ({1})'.format(APP_NAME, APP_VERSION))
		self.root.geometry('300x300')
		pluginFiles = os.listdir(PLUGIN_DIR)
		self.plugins = [(plugin, displayFormat(plugin)) for plugin in pluginFiles]
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

		self.displayLabel = tk.Label(self.root)
#		self.displayLabel.pack('left', fill='both', expand='yes')

		self.controlFrame = tk.Frame(self.root)
		self.controlFrame.pack()

		self.chartTypeLabel = tk.Label(self.controlFrame, text='Chart Type', font=TITLE_FONT)
		self.chartTypeLabel.pack()

		self.chartTypeBox = ttk.Combobox(self.controlFrame, values=[plugin[1] for plugin in self.plugins])
		self.chartTypeBox.pack()
		self.chartTypeBox.bind('<<ComboboxSelected>>', self.loadPlugin)

		self.pluginInterface = None

	def getPluginName(self, f):
		for pluginFile, pluginName in self.plugins:
			if pluginFile == f:
				return pluginName
		return None

	def getPluginFile(self, n):
		for pluginFile, pluginName in self.plugins:
			if pluginName == n:
				return pluginFile
		return None

	def loadPlugin(self, event):
		self.root.geometry('')
		pluginFile = self.getPluginFile(self.chartTypeBox.get())
		self.pluginInterface = PluginInterface(self.controlFrame, pluginFile)
		self.pluginInterface.pack()

	def exec_str(self, string):
		try:
			exec_str(string)
		except Exception as e:
			tk.messagebox.showerror('Error', str(e))

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
		tk.messagebox.showinfo(title='Current Database', message=agrra.config.DB)

	def save_chart(self, event=None):
		fileName = tk.filedialog.asksaveasfilename()
		if not fileName:
			return

		state.export.chart.save(fileName)

	def run(self):
		self.root.mainloop()

