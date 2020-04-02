import gi, sys

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MainWindow:
	def __init__(self):
		self.gladefile = 'main.glade'
		self.builder = Gtk.Builder()
		self.builder.add_from_file(self.gladefile)
		self.builder.connect_signals(self)
		self.main_window = self.builder.get_object('main_window')
		self.main_window.show()

	def exit(self, *args):
		Gtk.main_quit()

	def run(self):
		Gtk.main()
