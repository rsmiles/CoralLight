from libcorallight import *
from PySide2 import QtWidgets, QtGui

class MainWindow(QtWidgets.QMainWindow):

	def __init__(self):
		super(MainWindow, self).__init__()
		self.initUI()

	def initUI(self):
		exitAction = QtWidgets.QAction(QtGui.QIcon('exit.png'), '&Quit {0}'.format(APP_NAME), self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Quit {0}'.format(APP_NAME))
		exitAction.triggered.connect(self.close)

		self.statusBar()

		menubar = self.menuBar()
		appMenu = menubar.addMenu('&{0}'.format(APP_NAME))
		appMenu.addAction(exitAction)

		self.setGeometry(300, 300, 250, 150)
		self.setWindowTitle('{0} ({1})'.format(APP_NAME, APP_VERSION))
		self.show()

