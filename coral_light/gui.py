"""
gui.py

CoralLight's graphical user interface.

Copyright (c) 2020 Robert Smiley, all rights reserved.
Contents of this module are available under the terms of the GNU General Public
License, version 3. See LICENSE for details.
"""

from .app_info import *
from .text_mode import *
from . import backend

import tkinter as tk
import tkinter.filedialog
import traceback
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from PIL import ImageTk
import os, shutil
from os import path

PLUGIN_DIR = backend.APP_PATH + 'chart_plugins/'
TITLE_FONT = 'Helvetica 12 bold'

DB_FILETYPES = (('SQLite3 Databases', ('*.sqlite3', '*.sqlite', '*.db')),)
DATA_FILETYPES = (('Microsoft Excel Workbooks', '*.xlsx'),)
CORALLIGHT_PLUGIN_FILETYPES = (('CoralLight Plugins', '*.clight'),)

def sanitize(fieldName, string, escapeSingleQuote=True):
	BLACKLIST = ';'
	for char in string:
		assert char not in BLACKLIST, 'Forbidden character in {0}: {1}.'.format(fieldName, char)

	if escapeSingleQuote:
		return "''".join(string.split("'"))
	else:
		return string

def showError(error):
	print(traceback.format_exc())
	tk.messagebox.showerror('Error', str(error))

def displayFormat(string):
	noCap = ['the', 'for', 'by']
	noExt = os.path.splitext(string)[0]
	wordList = noExt.split('_')

	formatList = []
	for i, word in enumerate(wordList):

		if word == '':
			continue

		if i == 0 or word not in noCap:
			formatList.append(word[0].upper() + word[1:])
		else:
			formatList.append(word)

	displayString = ' '.join(formatList)
	return displayString
	

def getFieldValues(table, field):
	backend.cursor.execute('SELECT DISTINCT TRIM({0}) AS fval\nFROM {1}\nORDER by fval;'.format(field, table))
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

	def lift(self, aboveThis=None):
		self.root.lift(aboveThis)

class ParamEntry:
	def __init__(self, parent, param, paramType='text', *extraInfo):
		OPTIONS = (':upper',)

		self.parent = parent
		self.param = param
		self.paramType = paramType
		self.extraInfo = []
		self.options = []
		for e in extraInfo:
			if e[0] == ':':
				self.options.append(e)
			else:
				self.extraInfo.append(e)
		
		for option in self.options:
			assert option in OPTIONS, 'Invalid input option: ' + option + '.'
		
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
			fieldValues = getFieldValues(self.extraInfo[0], self.extraInfo[1])
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
		fieldName = displayFormat(self.param)

		for entry in self.entries:
			assert entry.get() != '', 'No value entered for field "{0}".'.format(fieldName)


		if self.paramType == 'raw':
			string = self.entries[0].get()
		if self.paramType == 'text' or self.paramType == 'field':
			string = "'" + sanitize(fieldName, self.entries[0].get()) + "'"
		elif self.paramType == 'textlist' or self.paramType == 'fieldlist':
			string = "('" + "', '".join([sanitize(fieldName, entry.get()) for entry in self.entries]) + "')"
		elif self.paramType == 'date':
			string = "'" + sanitize(fieldName, str(self.entries[0].get_date())) + "'"
		else:
			raise ValueError('Unkown input type: ' + self.paramType)

		if ':upper' in self.options:
			return string.upper()
		else:
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

		self.typeLabel = tk.Label(self.root, text='Format')
		self.typeLabel.pack()

		self.typeBox = ttk.Combobox(self.root, values=['Pie', 'Bar'])
		self.typeBox.pack()

		self.titleLabel = tk.Label(self.root, text='Title')
		self.titleLabel.pack()

		self.titleEntry = tk.Entry(self.root)
		self.titleEntry.pack()

		self.entries = []
		for param in self.params:
			entry = ParamEntry(self.root, *param)
			self.entries.append(entry)
			entry.pack()

	def setType(self, value):
		self.typeBox.set(value)

	def getEntries(self):
		return [(entry.param, entry.get()) for entry in self.entries]

	def getTitle(self):
		chartTitle = self.titleEntry.get()
		assert chartTitle != '', 'No title Entered for Chart {0}.'.format(str(self.number))
		return chartTitle

	def getType(self, forQuery=False):
		chartType = self.typeBox.get().strip().lower()
		if forQuery:
			assert chartType != '', 'No format selected for Chart {0}.'.format(str(self.number))
		return chartType

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

		self.descriptionMessage = tk.Message(self.root, text=self.description)
		self.descriptionMessage.pack()

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

		# default chart type if more than one
		if self.numCharts > 1:
			chart.setType(displayFormat(self.charts[-2].getType()))

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
		params['_title'] = ''
		params['_type'] = ''

		try:
			for chart in self.charts:
				for param, value in chart.getEntries():
					params[param] += value + '|'
				params['_title'] += sanitize('Title', chart.getTitle(), escapeSingleQuote=False) + '|'
				params['_type'] += sanitize('Format', chart.getType(forQuery=True)) + '|'
		except Exception as e:
			showError(e)
			return ''

		# remove final pipe symbol from each row, and ensure there are values
		for param in params:
			params[param] = params[param][:-1]

		qry = ''
		for param in params:
			qry += '@param {0} {1}\n'.format(param, params[param])

		qry += '@title $_title\n'
		qry += '@chart $_type\n'
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
			assert index >= 0, 'Cannot view before first chart.'
			assert index < len(self.charts), 'Cannot view after last chart.'
			self.index = index
			self.indexEntry.delete(0, tk.END)
			self.indexEntry.insert(0, str(index + 1))
			self.display.configure(image=self.charts[self.index])
		except Exception as e:
			showError(e)

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
			showError(e)
			return

		self.setIndex(index - 1)
			

	def pack(self, **args):
		self.root.pack(**args)

class MainWindow:
	def __init__(self):
		self.root = tk.Tk()
		self.root.title('{0} ({1})'.format(APP_NAME, APP_VERSION))
		self.root.geometry('200x300')
		self.plugins = []
		self.initUI()
		self.refreshPlugins()
		self.pluginLoaded = False
		self.chartsGenerated = False

	def refreshPlugins(self):
		pluginFiles = os.listdir(PLUGIN_DIR)
		self.plugins = [(plugin, displayFormat(plugin)) for plugin in pluginFiles]
		self.plugins.sort(key=lambda x: x[1])
		pluginList = [displayFormat(x[1]) for x in self.plugins]
		self.chartTypeBox.configure(values = pluginList)
		self.chartTypeBox.values = pluginList

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
		self.chartMenu.add_command(label='Install Chart Plugin', command=self.installChartPlugin, accelerator='Ctrl+Shift+I')
		self.menuBar.add_cascade(label='Chart', menu=self.chartMenu)


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

		while not backend.config.DB or not os.path.isfile(backend.config.DB):
			title = 'Setup Database'
			message = 'No database is currently loaded. Would you like to open an existing one? (If not, you will be prompted to create a new database.)'

			if tk.messagebox.askyesno(title=title, message=message):
				self.openDatabase()
			else:
				self.newDatabase()

		self.chartTypeLabel = tk.Label(self.controlWindow, text='Chart Type', font=TITLE_FONT)
		self.chartTypeLabel.pack()

		self.chartTypeBox = ttk.Combobox(self.controlWindow, values=[plugin[1] for plugin in self.plugins])
		self.chartTypeBox.pack()
		self.chartTypeBox.bind('<<ComboboxSelected>>', self.loadPlugin)

		self.pluginInterface = None
		self.genChartsButton = tk.Button(self.controlWindow, text='Generate Charts', command=self.genCharts)

		# Setup keyboard shortcuts
		self.root.bind_all('<Control-q>', self.quit)

		self.root.bind('<Control-w>', self.quit)
		self.root.bind('<Control-n>', self.newDatabase)
		self.root.bind('<Control-o>', self.openDatabase)
		self.root.bind('<Control-i>', self.importData)
		self.root.bind('<Control-d>', self.showCurrentDatabase)
		self.root.bind('<Control-s>', self.saveCurrentChart)
		self.root.bind('<Control-Shift-S>', self.saveAllCharts)
		self.root.bind('<Control-Shift-I>', self.installChartPlugin)
		self.root.bind('<Control-g>', self.genCharts)
		self.root.bind('<Control-Left>', self.chartLeft)
		self.root.bind('<Control-Right>', self.chartRight)
		self.root.bind('<Control-Prior>', self.scrollUp)
		self.root.bind('<Control-Next>', self.scrollDown)
		self.root.bind('<Prior>', self.pageUp)
		self.root.bind('<Next>', self.pageDown)

		# Setup mouse wheel scrolling
		self.root.bind('<Button-4>', self.mouseWheel)
		self.root.bind('<Button-5>', self.mouseWheel)
		self.root.bind('<MouseWheel>', self.mouseWheel)

	def mouseWheel(self, event):
		delta = 0
		if event.num == 4:
			delta = -1
		elif event.num == 5:
			delta = 1
		else:
			delta = event.delta

		self.controlCanvas.yview_scroll(delta, 'units')

	def scrollUp(self, event):
		self.controlCanvas.yview_scroll(-1, 'units')

	def scrollDown(self, event):
		self.controlCanvas.yview_scroll(1, 'units')

	def pageUp(self, event):
		self.controlCanvas.yview_scroll(-1, 'pages')

	def pageDown(self, event):
		self.controlCanvas.yview_scroll(1, 'pages')

	def chartLeft(self, event):
		if self.chartsGenerated:
			self.chartBrowser.left()

	def chartRight(self, event):
		if self.chartsGenerated:
			self.chartBrowser.right()

	def controlFrameConfigure(self, event):
		self.controlCanvas.configure(scrollregion=self.controlCanvas.bbox('all'))

	def getPluginName(self, f):
		for pluginFile, pluginName in self.plugins:
			if pluginFile == f:
				return pluginName
		return None

	def getPluginFile(self, n):
		for pluginFile, pluginName in self.plugins:
			if pluginName.lower() == n.strip().lower():
				return pluginFile
		return None

	def loadPlugin(self, event):
		try:
			self.root.geometry('')
			pluginFile = self.getPluginFile(self.chartTypeBox.get())
			if self.pluginInterface:
				self.pluginInterface.pack_forget()
				self.genChartsButton.pack_forget()
			self.pluginInterface = PluginInterface(self.controlWindow, pluginFile)
			self.pluginInterface.pack()
			self.genChartsButton.pack()
			self.genChartsButton.lift(self.pluginInterface.root)
		except Exception as e:
			showError(e)
		else:
			self.pluginLoaded = True

	def genCharts(self, event=None):
		# Prevent user from activating this with a keyboard shortcut before a plugin is loaded.
		if not self.pluginLoaded:
			return

		global state
		qry = self.pluginInterface.getQuery()
		if qry != '':
			self.execStr(qry)
			if not self.chartBrowser:
				self.controlFrame.pack_forget()
				self.chartBrowser = ChartBrowser(self.root)
				self.controlFrame.pack(side='left', fill='both', expand=True)
				self.chartBrowser.pack(side='left', fill='both', expand=True)
			self.chartBrowser.setCharts(state.export.charts)
			self.chartsGenerated = True

	def execStr(self, string):
		try:
			exec_str(string)
		except Exception as e:
			showError(e)
			return False
		return True

	def quit(self, event=None):
		self.root.destroy()

	def newDatabase(self, event=None):
		fileName = tk.filedialog.asksaveasfilename(filetypes=DB_FILETYPES)
		if not fileName:
			return

		if os.path.isfile(fileName):
			os.remove(fileName)

		try:
			self.execStr('@opendb {0};'.format(fileName))
		except Exception as e:
			showError(e)
		else:
			message='Database "{0}" created successfully.'.format(os.path.basename(fileName))
			tk.messagebox.showinfo(title='Success', message=message)

	def openDatabase(self, event=None):
		fileName = tk.filedialog.askopenfilename(filetypes=DB_FILETYPES)
		if not fileName:
			return

		result = self.execStr('@opendb {0};'.format(fileName))

		if result:
			message='Database "{0}" opened successfully.'.format(os.path.basename(fileName))
			tk.messagebox.showinfo(title='Success', message=message)

	def importData(self, event=None):
		fileNames = tk.filedialog.askopenfilenames(filetypes=DATA_FILETYPES)
		for fileName in fileNames:
			result = self.execStr('@import {0};'.format(fileName))

		if result:			 
			if len(fileNames) == 0:
				return
			elif len(fileNames) == 1:
				message='File "{0}" imported successfully.'.format(os.path.basename(fileNames[0]))
			else:
				message='{0} files imported successfully.'.format(str(len(fileNames)))

			tk.messagebox.showinfo(title='Success', message=message)
		

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

	def installChartPlugin(self, event=None):
		plugins = tk.filedialog.askopenfilenames(filetypes=CORALLIGHT_PLUGIN_FILETYPES)
		installed = 0
		for plugin in plugins:
			bname = os.path.basename(plugin)
			if os.path.isfile(PLUGIN_DIR + bname):
				message='A plugin named "{0}" is already installed. Would you like to replace it?'.format(bname)
				if tk.messagebox.askyesno(title='Plugin Exists', message=message):
					shutil.copy(plugin, PLUGIN_DIR + bname)
					installed += 1
				else:
					continue
			else:
				shutil.copy(plugin, PLUGIN_DIR + bname)
				installed += 1

			if installed == 0:
				pass
			elif installed == 1:
				message='Chart Plugin "{0}" installed successfully.'.format(os.path.basename(plugins[0]))
				tk.messagebox.showinfo(title='Success', message=message)
			else:
				message = '{0} chart plugins installed successfully'.format(str(installed))
				tk.messagebox.showinfo(title='Success', message=message)

			self.refreshPlugins()

	def run(self):
		self.root.mainloop()

