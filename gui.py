from libcorallight import *
from PySide2 import QtWidgets, QtGui


class MainWindow(QtWidgets.QMainWindow):

	def __init__(self):
		super(MainWindow, self).__init__()
		self.initUI()

	def newDatabase(self):
		fname, ftype = QtWidgets.QFileDialog.getSaveFileName()
		if fname:
			exec_str('@opendb {0};'.format(fname))
			self.dbIndicator.setText(agrra.config.DB)

	def openDatabase(self):
		fname, ftype = QtWidgets.QFileDialog.getOpenFileName()
		if fname:
			exec_str('@opendb {0};'.format(fname))
			self.dbIndicator.setText(agrra.config.DB)

	def importData(self):
		fnames, ftypes = QtWidgets.QFileDialog.getOpenFileNames(filter='*.xlsx')
		for fname in fnames:
			exec_str('@import {0};'.format(fname))

	def initUI(self):
		exitAction = QtWidgets.QAction(QtGui.QIcon(''), '&Quit {0}'.format(APP_NAME), self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Quit {0}'.format(APP_NAME))
		exitAction.triggered.connect(self.close)

		newDatabaseAction = QtWidgets.QAction(QtGui.QIcon(''), '&New Database', self)
		newDatabaseAction.setShortcut('Ctrl+N')
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

		self.setGeometry(300, 300, 640, 480)
		self.setWindowTitle('{0} ({1})'.format(APP_NAME, APP_VERSION))
		self.show()


