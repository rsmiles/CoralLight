#!/usr/bin/env python3

import agrra, os, sys

class CoralLight_State:
	def __init__(self):
		self.query = ''
		self.title = ''
		self.saveas = ''
		self.ymax = ''
		self.chart = 'pie'
		self.mode = 'INTERACTIVE'

state = CoralLight_State()

def subvar(query, var_name, value):
	return query.replace('$' + var_name, value)

def subvars(query, var_list):
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

if '-n' in sys.argv or '--non-interactive' in sys.argv:
	state.mode = 'NON_INTERACTIVE'

def corallight_exit():
	sys.exit()

def corallight_opendb(*args):
	agrra.open_db(' '.join(args))

def corallight_import(xlsx):
	agrra.import_xlsx(xlsx)

def corallight_saveas(*args):
	global state
	if args == 0:
		state.saveas = ''
	else:
		state.saveas = ' '.join(args)

def corallight_title(*args):
	global state 
	state.title = ' '.join(args)

def corallight_importdir(*args):
	directory = ' '.join(args)

	if directory[-1] != '/':
		directory += '/'

	for f in os.listdir(directory):
		ext = os.path.splitext(f)[1]
		if ext == '.xlsx':
			corallight_import(directory + f)

def corallight_chart(arg):
	global state
	state.chart = arg

def corallight_ymax(arg):
	global state
	state.ymax = int(arg)


builtins = {'exit': corallight_exit,
			'opendb': corallight_opendb,
			'import': corallight_import,
			'importdir': corallight_importdir,
			'title': corallight_title,
			'saveas': corallight_saveas,
			'chart': corallight_chart,
			'ymax': corallight_ymax}

def run_command(command):
	return builtins[command[0][1:]](*command[1:])

PROMPT = 'corallight_$: '

def print_prompt():
	global state
	if state.mode == 'INTERACTIVE':
		sys.stdout.write(PROMPT)
		sys.stdout.flush()

def exec_query(query, chart, title, ymax, saveas):
	if query == '':
		return

	chart = agrra.chart(query, chart, title=title, ymax=ymax)
	if state.mode == 'INTERACTIVE':
	    chart.show()
	else:
		assert saveas, 'No save file specified when running in non-interactive mode'

	if saveas:
		chart.save(saveas)

def exec_lines(lines):
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
	params = []
	new_lines = []
	for line in lines:
		stripped = line.strip()
		stripped_line = stripped.split(' ')
		if stripped_line[0] == '@param':
			param_name = stripped_line[1]
			param_vals = ' '.join(stripped_line[2:]).split(',')
			params.append((param_name, [x.strip() for x in param_vals]))
		else:
			new_lines.append(line)

	expanded = subvars(''.join(new_lines), params)
	return [query.split('\n') for query in expanded]

def read_chart(lines):
	chart_lines = []
	for line in lines:
		split_line = line.split(';')
		if len(split_line) == 1:
			chart_lines.extend(split_line)
		else:
			while len(split_line) > 1:
				chart_lines.append(split_line.pop(0) + '\n')
				yield chart_lines[:]
				chart_lines = []

print_prompt()
for chart in read_chart(sys.stdin):
	for query in expand_lines(chart):
		exec_lines(query)
	print_prompt()
print()

