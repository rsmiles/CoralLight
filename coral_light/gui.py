from .app_info import *
from .text_mode import *
from . import backend

import tkinter as tk
import tkinter.filedialog
import traceback
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from PIL import ImageTk
import os

PLUGIN_DIR = backend.APP_PATH + 'chart_plugins/'
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
	

def getFieldValues(field):
	backend.cursor.execute('SELECT DISTINCT TRIM({0}) AS fval\nFROM data\nORDER by fval;'.format(field))
	values = backend.cursor.fetchall()
	return list([value[0] for value in values])

class ButtonPair:
	def __init__(self, parent, leftText=None, leftCommand=None, rightText=None, rightCommand=None):
		self.parent = parent
		self.root = tk.Frame(self.parent)

		self.left = tk.Button(self.root, text=leftText, command=leftCommand)
		self.left.pack(side='left')

		self.right = tk.Button(self.root, text=rightText, command=rightCommand)
		self.right.pack(side='left')

	def pack(self, **opts):
		self.root.pack(**opts)

	def pack_forget(self):
		self.root.pack_forget()

	def lower(self):
		self.root.lower()
		self.right.lower()
		self.left.lower()

	def lift(self, aboveThis=None):
		self.root.lift(aboveThis)

class ParamEntry:
	def __init__(self, parent, param, paramType='text', extraInfo=None):
		self.parent = parent
		self.param = param
		self.paramType = paramType
		self.extraInfo = extraInfo
		self.initUI()

	def initUI(self):
		self.root = tk.Frame(self.parent)

		self.label = tk.Label(self.root, text=displayFormat(self.param))
		self.label.pack()

		self.buttons = None

		if self.paramType == 'textlist' or self.paramType == 'fieldlist':
			self.buttons = ButtonPair(self.root, leftText='+', leftCommand=self.addEntry, rightText='-', rightCommand=self.removeEntry)
			self.buttons.pack()

		self.entries = []
		self.addEntry()

	def addEntry(self, event=None):
		if self.buttons:
			self.buttons.pack_forget()

		entry = None
		if self.paramType == 'text' or self.paramType == 'textlist':
			entry = tk.Entry(self.root)
		elif self.paramType == 'field' or self.paramType == 'fieldlist':
			fieldValues = getFieldValues(self.extraInfo)
			entry = ttk.Combobox(self.root, values=fieldValues)
		elif self.paramType == 'date':
			entry = DateEntry(self.root)
		else:
			raise ValueError('Unkown input type: ' + self.paramType)

		self.entries.append(entry)
		entry.pack()

		if self.buttons:
			self.buttons.pack()
			self.buttons.lift(self.entries[-1])

	def removeEntry(self, event=None):
		if len(self.entries) > 1:
			self.entries[-1].pack_forget()
			self.entries.pop()

	def get(self):
		string = None
		if self.paramType == 'raw':
			string = self.entries[0].get()
		if self.paramType == 'text' or self.paramType == 'field':
			string = "'" + self.entries[0].get() + "'"
		elif self.paramType == 'textlist' or self.paramType == 'fieldlist':
			string = "('" + "', '".join([entry.get() for entry in self.entries]) + "')"
		elif self.paramType == 'date':
			string = "'" + str(self.entries[0].get_date()) + "'"
		else:
			raise ValueError('Unkown input type: ' + self.paramType)

		return string

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
			entry = ParamEntry(self.root, *param)
			self.entries.append(entry)
			entry.pack()

	def getEntries(self):
		return [(entry.param, entry.get()) for entry in self.entries]

	def getTitle(self):
		return self.titleEntry.get()

	def pack(self, **opts):
		self.root.pack(**opts)

	def pack_forget(self):
		self.root.pack_forget()

class PluginInterface:
	def __init__(self, parent, name):
		self.parent = parent
		self.name = name
		self.initText()
		self.initUI()

	def initText(self):
		self.title = None
		self.description = ''
		self.params = []
		self.text = ''
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
						if splitLine[0] == '@input':
							self.params.append(list(field.strip() for field in splitLine[1:]))
						else:
							self.text += line
					else:
						self.text += line
			self.text += ';'

	def initUI(self):
		self.root = tk.Frame(self.parent)

		self.titleLabel = tk.Label(self.root, text=self.title, font=TITLE_FONT)
		self.titleLabel.pack()

		self.descriptionLabel = tk.Label(self.root, text=self.description)
		self.descriptionLabel.pack()

		self.charts = []

		self.buttons = ButtonPair(self.root, leftText='Add Chart', leftCommand=self.addChart, rightText='Remove Chart', rightCommand=self.removeChart)
		self.buttons.pack()
	
		self.addChart()

	def addChart(self):
		self.buttons.pack_forget()
		self.numCharts += 1
		chart = ChartEntry(self.root, self.params, self.numCharts)
		self.charts.append(chart)
		chart.pack()
		self.buttons.pack()
		self.buttons.lift(self.charts[-1].root)

	def removeChart(self):
		if len(self.charts) > 1:
			self.charts[-1].pack_forget()
			self.charts.pop()
			self.numCharts -= 1

	def getQuery(self):
		params = {}
		for param in self.params:
			params[param[0]] = ''
		params['title'] = ''

		for chart in self.charts:
			for param, value in chart.getEntries():
				params[param] += value + '|'
			params['title'] += chart.getTitle() + '|'

		# remove final pipe symbol from each row
		for param in params:
			params[param] = params[param][:-1]

		qry = ''
		for param in params:
			qry += '@param {0} {1}\n'.format(param, params[param])

		qry += '@title $title\n'
		qry += self.text

		return qry

	def pack(self, **opts):
		self.root.pack(**opts)

	def pack_forget(self):
		self.root.pack_forget()

class ChartBrowser:
	def __init__(self, parent):
		self.parent = parent
		self.charts = None
		self.index = None
		self.initUI()

	def initUI(self):
		self.root = tk.Frame(self.parent)

		self.display = tk.Label(self.root)
		self.display.pack()

		self.controlFrame = tk.Frame(self.root)
		self.controlFrame.pack()

		self.leftButton = tk.Button(self.controlFrame, text='<', command=self.left)
		self.leftButton.pack(side='left')

		self.rightButton = tk.Button(self.controlFrame, text='>', command=self.right)
		self.rightButton.pack(side='left')
	
		self.indexEntry = tk.Entry(self.controlFrame, width=2, text=str(self.index))
		self.indexEntry.pack(side='left')

		self.totalLabel = tk.Label(self.controlFrame, text='')
		self.totalLabel.pack(side='left')

		self.goButton = tk.Button(self.controlFrame, text='Go', command=self.go)
		self.goButton.pack(side='left')

	def setIndex(self, index):
		try:
			assert index >= 0, 'Cannot view before first chart'
			assert index < len(self.charts), 'Cannot view after last chart'
			self.index = index
			self.indexEntry.delete(0, tk.END)
			self.indexEntry.insert(0, str(index + 1))
			self.display.configure(image=self.charts[self.index])
		except Exception as e:
			print(traceback.format_exc())
			tk.messagebox.showerror('Error', str(e))

	def setCharts(self, charts):
		self.charts = [ImageTk.PhotoImage(chart) for chart in charts]
		self.setIndex(0)
		self.totalLabel.configure(text='/ {0}'.format(len(self.charts)))

	def left(self):
		if self.index > 0:
			self.setIndex(self.index - 1)

	def right(self):
		if self.index < len(self.charts) - 1:
			self.setIndex(self.index + 1)

	def go(self):
		index = None 
		try:
			index = int(self.indexEntry.get())
		except Exception as e:
			print(traceback.format_exc())
			tk.messagebox.showerror('Error', 'Only integers accepted')
			return

		self.setIndex(index - 1)
			

	def pack(self, **args):
		self.root.pack(**args)

class MainWindow:
	def __init__(self):
		self.root = tk.Tk()
		self.root.title('{0} ({1})'.format(APP_NAME, APP_VERSION))
		self.root.geometry('200x300')
		pluginFiles = os.listdir(PLUGIN_DIR)
		self.plugins = [(plugin, displayFormat(plugin)) for plugin in pluginFiles]
		self.initUI()

	def initUI(self):
		self.menuBar = tk.Menu(self.root)

		self.coralLightMenu = tk.Menu(self.menuBar, tearoff=False)
		self.coralLightMenu.add_command(label='Quit ' + APP_NAME, command=self.quit, accelerator='Ctrl+Q')
		self.menuBar.add_cascade(label=APP_NAME, menu=self.coralLightMenu)

		self.dataMenu = tk.Menu(self.menuBar, tearoff=False)
		self.dataMenu.add_command(label='New Database', command=self.newDatabase, accelerator='Ctrl+N')
		self.dataMenu.add_command(label='Open Database', command=self.openDatabase, accelerator='Ctrl+O')
		self.dataMenu.add_command(label='Import Data', command=self.importData, accelerator='Ctrl+I')
		self.dataMenu.add_command(label='Show Current Database', command=self.showCurrentDatabase, accelerator='Ctrl+D')
		self.menuBar.add_cascade(label='Data', menu=self.dataMenu)

		self.chartMenu = tk.Menu(self.menuBar, tearoff=False)
		self.chartMenu.add_command(label='Save Current', command=self.saveCurrentChart, accelerator='Ctrl+S')
		self.chartMenu.add_command(label='Save All', command=self.saveAllCharts, accelerator='Ctrl+Shift+S')
		self.menuBar.add_cascade(label='Chart', menu=self.chartMenu)

		# Setup keyboard shortcuts
		self.root.bind_all('<Control-q>', self.quit)

		self.root.bind('<Control-w>', self.quit)
		self.root.bind('<Control-n>', self.newDatabase)
		self.root.bind('<Control-o>', self.openDatabase)
		self.root.bind('<Control-i>', self.importData)
		self.root.bind('<Control-d>', self.showCurrentDatabase)
		self.root.bind('<Control-s>', self.saveCurrentChart)
		self.root.bind('<Control-Shift-S>', self.saveAllCharts)

		self.root.config(menu=self.menuBar)

		self.chartBrowser = None

		self.controlFrame = tk.Frame(self.root)
		self.controlCanvas = tk.Canvas(self.controlFrame)
		self.controlWindow = tk.Frame(self.controlCanvas)
		self.scrollbar = tk.Scrollbar(self.controlFrame, orient='vertical', command=self.controlCanvas.yview)
		self.controlCanvas.configure(yscrollcommand=self.scrollbar.set)

		self.controlFrame.pack(fill='both', expand=True)
		self.controlCanvas.pack(side='left', fill='both', expand=True)
		self.scrollbar.pack(side='left', fill='y')
		self.controlCanvas.create_window((4, 4), window=self.controlWindow, anchor='nw', tags='self.controlWindow')

		self.controlWindow.bind('<Configure>', self.controlFrameConfigure)

		self.chartTypeLabel = tk.Label(self.controlWindow, text='Chart Type', font=TITLE_FONT)
		self.chartTypeLabel.pack()

		self.chartTypeBox = ttk.Combobox(self.controlWindow, values=[plugin[1] for plugin in self.plugins])
		self.chartTypeBox.pack()
		self.chartTypeBox.bind('<<ComboboxSelected>>', self.loadPlugin)

		self.pluginInterface = None
		self.genChartsButton = tk.Button(self.controlWindow, text='Generate Charts', command=self.genCharts)

	def controlFrameConfigure(self, event):
		self.controlCanvas.configure(scrollregion=self.controlCanvas.bbox('all'))

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
		if self.pluginInterface:
			self.pluginInterface.pack_forget()
			self.genChartsButton.pack_forget()
		self.pluginInterface = PluginInterface(self.controlWindow, pluginFile)
		self.pluginInterface.pack()
		self.genChartsButton.pack()
		self.genChartsButton.lift(self.pluginInterface.root)

	def genCharts(self):
		global state
		qry = self.pluginInterface.getQuery()
		self.execStr(qry)
		if not self.chartBrowser:
			self.controlFrame.pack_forget()
			self.chartBrowser = ChartBrowser(self.root)
			self.controlFrame.pack(side='left', fill='both', expand=True)
			self.chartBrowser.pack(side='left', fill='both', expand=True)
		self.chartBrowser.setCharts(state.export.charts)

	def execStr(self, string):
		try:
			exec_str(string)
		except Exception as e:
			print(traceback.format_exc())
			tk.messagebox.showerror('Error', str(e))

	def quit(self, event=None):
		self.root.destroy()

	def newDatabase(self, event=None):
		fileName = tk.filedialog.asksaveasfilename()
		if not fileName:
			return

		elif os.path.isfile(fileName):
			os.remove(fileName)
		self.execStr('@opendb {0};'.format(fileName))

	def openDatabase(self, event=None):
		fileName = tk.filedialog.askopenfilename()
		if not fileName:
			return

		self.execStr('@opendb {0};'.format(fileName))

	def importData(self, event=None):
		fileNames = tk.filedialog.askopenfilenames()
		for fileName in fileNames:
			self.execStr('@import {0};'.format(fileName))

	def showCurrentDatabase(self, event=None):
		tk.messagebox.showinfo(title='Current Database', message=backend.config.DB)

	def saveCurrentChart(self, event=None):
		global state
		fileName = tk.filedialog.asksaveasfilename()
		if not fileName:
			return

		state.export.charts[self.chartBrowser.index].save(fileName)

	def saveAllCharts(self, event=None):
		global state
		dirName = tk.filedialog.asksaveasfilename()
		if not dirName:
			return

		os.mkdir(dirName)

		for index, chart in enumerate(state.export.charts):
			chart.save(dirName + '/' + str(index + 1) + '.png')

	def run(self):
		self.root.mainloop()

