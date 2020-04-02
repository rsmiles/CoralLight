#!/usr/bin/env python3

from libcorallight import *
import gui, sys

def main():
	if '-t' in sys.argv or '--text' in sys.argv:
		state.mode = 'INTERACTIVE'
	if '-n' in sys.argv or '--non-interactive' in sys.argv:
		state.mode = 'NON_INTERACTIVE'
	elif '-d' in sys.argv or '--debug' in sys.argv:
		state.mode = 'DEBUG'

	if state.mode == 'GUI':
		app = QtWidgets.QApplication(sys.argv)
		mainWindow = gui.MainWindow()
		mainWindow.run()
	else:
		if state.mode == 'INTERACTIVE':
			print_prompt()

		for chart in read_chart(sys.stdin):
			if state.mode == 'INTERACTIVE':
				try:
					exec_chart(chart)
					print_prompt()
				except Exception as e:
					print('Error in query starting at line: ' + str(state.query_start) + ': ' + str(e))
					print_prompt()
			elif state.mode == 'NON_INTERACTIVE':
				try:
					exec_chart(chart)
					print_prompt()
				except Exception as e:
					print('Error in query starting at line: ' + str(state.query_start) + ': ' + str(e))
					sys.exit(1)
			elif state.mode == 'DEBUG':
				try:
					exec_chart(chart)
					print_prompt()
				except Exception as e:
					print('Error in query starting at line: ' + str(state.query_start) + ': ' + str(e))
					raise e
			else:
				raise Exception('Unkown program mode: ' + state.mode)
		print()

if __name__ == '__main__':
	main()

