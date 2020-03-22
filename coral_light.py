#!/usr/bin/env python3

import agrra, os, sys

class CoralLight_State:
    def __init__(self):
        self.query = ''
        self.saveas = ''
        self.title = ''
        self.ymax = ''
        self.chart = 'pie'
        self.interactive = True

state = CoralLight_State()

if '-n' in sys.argv or '--non-interactive' in sys.argv:
	state.interactive = False

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
	if state.interactive:
		sys.stdout.write(PROMPT)
		sys.stdout.flush()

def exec_qry():
	global state
	chart = agrra.chart(state.query, state.chart, title=state.title, ymax=state.ymax)
	if state.interactive:
	    chart.show()
	else:
		assert state.saveas, 'No save file specified when running in non-interactive mode'

	if state.saveas:
		chart.save(state.saveas)
	state.query = ''

print_prompt()

for line in sys.stdin:
	if line[0] == '#':
		pass
	elif line[0] == '@':
		command = line[:-1].split(' ')
		run_command(command)
	else:
		queries = line.split(';')
		if len(queries) > 1:
			for query in queries[:-1]:
				state.query += query
				exec_qry()
		else:
			state.query += queries[0]

	print_prompt()

print()

