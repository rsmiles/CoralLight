from libcorallight import *
import agrra
from PySide2 import QtWidgets, QtGui

def dataMapNames(datamap):
	return [datamap[key]['name'] for key in datamap]

class ChartCreatorWindow(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.chartTypeLabel = QtWidgets.QLabel('Chart Type')
		self.chartTypeBox = QtWidgets.QComboBox()
		self.chartTypeBox.addItems(('Pie', 'Bar'))

		varBoxItems = dataMapNames(agrra.encounter_datamap)
		self.varLabel = QtWidgets.QLabel('Variable')
		self.varBox = QtWidgets.QComboBox()
		self.varBox.addItems(varBoxItems)

		layout = QtWidgets.QFormLayout()
		layout.addRow(self.chartTypeLabel, self.chartTypeBox)
		layout.addRow(self.varLabel, self.varBox)

		self.setWindowTitle(APP_NAME + ' Chart Creator')
		self.setGeometry(300, 300, 640, 480)
		self.setLayout(layout)
		self.show()

class MainWindow(QtWidgets.QMainWindow):

	def __init__(self):
		super(MainWindow, self).__init__()
		self.initUI()

	def exec_str(self, string):
		try:
			exec_str(string)
		except Exception as e:
			mesg = str(e)
			mesgBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, 'Error', mesg)
			mesgBox.exec()

	def newDatabase(self):
		fname, ftype = QtWidgets.QFileDialog.getSaveFileName()
		if fname:
			self.exec_str('@opendb {0};'.format(fname))
			self.dbIndicator.setText(agrra.config.DB)

	def openDatabase(self):
		fname, ftype = QtWidgets.QFileDialog.getOpenFileName()
		if fname:
			self.exec_str('@opendb {0};'.format(fname))
			self.dbIndicator.setText(agrra.config.DB)

	def importData(self):
		fnames, ftypes = QtWidgets.QFileDialog.getOpenFileNames(filter='*.xlsx')
		for fname in fnames:
			self.exec_str('@import {0};'.format(fname))

	def newChart(self):
		self.chartCreator = ChartCreatorWindow()

	def initUI(self):
		exitAction = QtWidgets.QAction(QtGui.QIcon(''), '&Quit {0}'.format(APP_NAME), self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Quit {0}'.format(APP_NAME))
		exitAction.triggered.connect(self.close)

		newDatabaseAction = QtWidgets.QAction(QtGui.QIcon(''), '&New Database', self)
		newDatabaseAction.setShortcut('Ctrl+Shift+N')
		newDatabaseAction.setStatusTip('Create a new database')
		newDatabaseAction.triggered.connect(self.newDatabase)
	
		openDatabaseAction = QtWidgets.QAction(QtGui.QIcon(''), '&Open Database', self)
		openDatabaseAction.setShortcut('Ctrl+O')
		openDatabaseAction.setStatusTip('Open and existing database')
		openDatabaseAction.triggered.connect(self.openDatabase)

		importDataAction = QtWidgets.QAction(QtGui.QIcon(''), '&Import Data', self)
		importDataAction.setShortcut('Ctrl+I')
		importDataAction.setStatusTip('Import Excel File')
		importDataAction.triggered.connect(self.importData)

		newChartAction = QtWidgets.QAction(QtGui.QIcon(''), '&New Chart', self)
		newChartAction.setShortcut('Ctrl+N')
		newChartAction.setStatusTip('Create a new chart')
		newChartAction.triggered.connect(self.newChart)

		self.dbIndicator = QtWidgets.QLabel(agrra.config.DB)

		self.statusBar()
		self.statusBar().addWidget(self.dbIndicator)

		menuBar = self.menuBar()
		appMenu = menuBar.addMenu('&{0}'.format(APP_NAME))
		appMenu.addAction(exitAction)

		dataMenu = menuBar.addMenu('&Data')
		dataMenu.addAction(newDatabaseAction)
		dataMenu.addAction(openDatabaseAction)
		dataMenu.addAction(importDataAction)

		chartMenu = menuBar.addMenu('&Chart')
		chartMenu.addAction(newChartAction)

		self.setGeometry(300, 300, 640, 480)
		self.setWindowTitle('{0} ({1})'.format(APP_NAME, APP_VERSION))
		self.show()

