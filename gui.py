import tkinter as tk

queries = []
charts = []

class MainWindow(tk.Frame):
	def __init__(self):
		super().__init__()
		self.pack()
		self.initUI()

	def initUI(self):
		self.hello = tk.Button(self)
		self.hello['text'] = 'Hello World\n(Click Me)'
		self.hello['command'] = self.greet
		self.hello.pack(side='top')

	def greet(*args):
		print('hello world!')
	
	def run(self):
		self.mainloop()
