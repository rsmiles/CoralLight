"""
text_mode.py

Copyright (c) 2020 Robert Smiley, all rights reserved.
Contents of this module are available under the terms of the GNU General Public
License, version 3. See LICENSE for details.

Code for running CoralLight's text mode.

Allows for reading SQL Code with CoralLight annotations and producing charts
from said code.
"""

import os, sys
from .backend import *

class CoralLight_Export:
	"""
	Collection of fields that may be accessed by other parts of CoralLight,
	most notably the GUI.
	"""
	def __init__(self):
		self.query = None
		self.charts = None
		self.title = None
		self.ymax = None
		self.saveas = None

class CoralLight_State:
	"""
	Main state of the CoralLight program. Contains running mode, variables set
	by CoralLight annotations to SQL, and the section to be exported to the GUI.
	"""

	def __init__(self):
		self.query = ''
		self.title = ''
		self.saveas = ''
		self.ymax = ''
		self.chart = 'pie'
		self.mode = 'GUI'
		self.query_start = 0 # Line the current expression began on
		self.query_fin = 0 # Line the current expression ended on
		self.export = CoralLight_Export() # Section other program components access (i.e. GUI)

state = CoralLight_State()

def subvar(query, var_name, value):
	"""
	Search query for the string var_name, preceeded by a dollar sign ($). Substitute
	said string for the specified value. Return substituted string.
	"""
	return query.replace('$' + var_name, value)

def subvars(query, var_list):
	"""
	Substitute all variables in query, with their definitions in var_list.

	query: A string, representing an SQL query. Within the string, are variables,
			appearing as names preceeded by dollar signs ($).
	var_list: A list of tuples, each tuple has two elements, a variable name, and
				the value to be assigned to that variable.
	"""
	if len(var_list) == 0:
		return [query]

	nvals = len(var_list[0][1])

	for binding in var_list:
		assert len(binding[1]) == nvals, 'All variables must have the same number of values'

	results = []
	val_index = 0
	while val_index < nvals:
		new_query = query
		for binding in var_list:
			new_query = subvar(new_query, binding[0], binding[1][val_index])

		results.append(new_query)
		val_index += 1

	return results

def corallight_exit():
	"""Available in CoralLight's text mode. Exits CoralLight, performing any necessary cleanup code."""
	sys.exit()

def corallight_opendb(*args):
	"""Available in CoralLight's text mode. Opens the database specified by *args. *args are joined by spaces to form database name."""
	backend.open_db(' '.join(args))

def corallight_import(*args):
	"""Available in CoralLight's text mode. Imports the excel file specified by *args. *args are joined by spaces to form file name."""
	xlsx = ' '.join(args)
	backend.import_xlsx(xlsx)

def corallight_saveas(*args):
	"""Available in CoralLight's text mode. Specifies the name of the file to save the next chart to after generating it. *args are joined by spaces to form file name."""
	global state
	if args == 0:
		state.saveas = ''
	else:
		state.saveas = ' '.join(args)

def corallight_title(*args):
	"""Available in CoralLight's text mode. Specifies the name of the next chart's title. *args are joined by spaces to form the title."""
	global state 
	state.title = ' '.join(args)

def corallight_importdir(*args):
	"""Available in CoralLight's text mode. Import all files with a .xlsx extension. *args are joined by spaces to form directory name."""
	directory = ' '.join(args)

	if directory[-1] != '/':
		directory += '/'

	for f in os.listdir(directory):
		ext = os.path.splitext(f)[1]
		if ext == '.xlsx':
			corallight_import(directory + f)

def corallight_chart(arg):
	"""Available in CoralLight's text mode. Specifies the type of chart that the next chart should be. arg should be either "pie" or "bar"."""
	global state
	state.chart = arg

def corallight_ymax(arg):
	"""Available in CoralLight's text mode. If the next chart wll be a bar graph, specifies the y value at the top of the visible graph. Can be used to set a specific height for the graph."""
	global state
	state.ymax = int(arg)

def corallight_input(*args):
	"""Available in CoralLight's text mode. Raises an exception informing the user that this command should only be used from the GUI."""
	raise Exception('"@input" should be used in input code for the graphical interface only')

# Map builtin commands in CoralLight to their function names.
builtins = {'exit': corallight_exit,
			'opendb': corallight_opendb,
			'import': corallight_import,
			'importdir': corallight_importdir,
			'title': corallight_title,
			'saveas': corallight_saveas,
			'chart': corallight_chart,
			'ymax': corallight_ymax,
			'input': corallight_input}

def run_command(command):
	"""Run the specified command. The command should be a list, containing the command name, followed by it's arguments."""
	return builtins[command[0][1:]](*command[1:])

PROMPT = 'corallight_$: '

def print_prompt():
	"""Print the CoralLight user prompt, if in INTERACTIVE mode, otherwise do nothing."""
	global state
	if state.mode == 'INTERACTIVE':
		sys.stdout.write(PROMPT)
		sys.stdout.flush()

def exec_query(query, chart, title, ymax, saveas):
	"""
	Execute the specified query, creating a chart from the query, then act according to program mode.

	query: The SQL query to use to generate the chart.
	title: The title of the chart.
	ymax: If the chart is a bar graph, the y value at the top of the chart. Can be used to specify chart height.
	saveas: The name of the file to save the resulting chart to.

	If in interactive mode, save the chart, if a save file name was given, and display it.
	If in non-interactive mode, save the chart, if a save file name was given, otherwise throw an error.
	If in gui mode, append the chart to state.export.charts so the GUI can retrieve it.
	"""
	global state

	if query == '':
		return

	chart_img = backend.chart(query, chart, title=title, ymax=ymax)
	if state.mode == 'GUI':
		state.export.query = query
		state.export.charts.append(chart_img)
		state.export.title = title
		state.export.ymax = ymax
		state.export.saveas = saveas
	elif state.mode == 'INTERACTIVE':
	    chart_img.show()
	else:
		assert saveas, 'No save file specified when running in non-interactive mode'

	if saveas:
		chart_img.save(saveas)

def exec_lines(lines):
	"""
	Execute the provided lines of SQL with CoralLight annotations.

	Run any CoralLight commands encountered and execute the SQL to generate one or more charts.

	lines: A sequence of strings.
	"""
	global state
	for line in lines:
		if line == '':
			pass
		elif line[0] == '#':
			pass
		elif line[0] == '@':
			command = line.strip().split(' ')
			run_command(command)
		else:
			state.query += line + '\n'

	exec_query(state.query, state.chart, state.title, state.ymax, state.saveas)
	state.query = ''

def expand_lines(lines):
	"""
	Perform variable expansion on the given lines. This means multiple copies of
	the given lines are returned, each with substitutions of different assigned
	variable values.

	lines: A sequence of strings.
	returns: A list of strings.
	"""
	params = []
	new_lines = []
	for line in lines:
		stripped = line.strip()
		stripped_line = stripped.split(' ')
		if stripped_line[0] == '@param':
			assert len(stripped_line) > 2, 'Parameters must have values'
			param_name = stripped_line[1]
			param_vals = ' '.join(stripped_line[2:]).split('|')
			params.append((param_name, [x.strip() for x in param_vals]))
		else:
			new_lines.append(line)

	expanded = subvars('\n'.join(new_lines), params)
	return [query.split('\n') for query in expanded]

def read_chart(lines):
	"""
	Read one SQL expression and any CoralLight annotations contained within.

	Reads from lines until a semicolon (;) is encountered.

	lines: A sequence of strings.
	returns: A list of strings.
	"""
	global state
	state.query_start = state.query_fin + 1
	chart_lines = []
	for line in lines:
		state.query_fin += 1
		split_line = line.split(';')
		if len(split_line) == 1:
			chart_lines.extend(split_line)
		else:
			while len(split_line) > 1:
				chart_lines.append(split_line.pop(0) + '\n')
				yield chart_lines[:]
				state.query_start = state.query_fin + 1
				chart_lines = []
		

def exec_chart(chart):
	"""
	Execute a given SQL expression with CoralLight annotations.

	chart: A sequence of strings representing the expression.
	"""
	for query in expand_lines(chart):
		exec_lines(query)

def exec_str(string):
	"""
	Execute a given string.

	string: A string.
	"""
	global state
	state.export.charts = []
	for q in read_chart(string.split('\n')):
		exec_chart(q)

