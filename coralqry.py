#!/usr/bin/env python3

import agrra, sys

qry = ''
saveas = ''

non_interactive = False

if '-n' in sys.argv or '--non-interactive' in sys.argv:
	non_interactive = True

def coralqry_exit():
	sys.exit()

def coralqry_opendb(*args):
	agrra.open_db(' '.join(args))

def coralqry_import(xlsx):
	agrra.import_xlsx(xlsx)

def coralqry_saveas(*args):
	global saveas
	if args == 0:
		saveas = ''
	else:
		saveas = ' '.join(args)

builtins = {'exit': coralqry_exit,
			'opendb': coralqry_opendb,
			'import': coralqry_import,
			'saveas': coralqry_saveas}

def run_command(command):
	return builtins[command[0][1:]](*command[1:])

PROMPT = 'coralqry_$: '

def print_prompt():
	if not non_interactive:
		sys.stdout.write(PROMPT)
		sys.stdout.flush()

def exec_qry():
	global qry

	if non_interactive:
		if saveas == '':
			raise Exception('No name specified for piechart')
		else:
			agrra.piechart(qry, saveas)
	else:
		if saveas == '':
			agrra.piechart(qry)
		else:
			agrra.piechart(qry, saveas)

	qry = ''

print_prompt()

for line in sys.stdin:
	if line[0] == '#':
		pass
	elif line[0] == ',':
		command = line[:-1].split(' ')
		run_command(command)
	else:
		queries = line.split(';')
		if len(queries) > 1:
			for query in queries[:-1]:
				qry += query
				exec_qry()
		else:
			qry += queries[0]

	print_prompt()

print()

