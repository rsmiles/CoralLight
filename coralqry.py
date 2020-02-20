#!/usr/bin/env python3

import agrra, os, sys

qry = ''
saveas = ''
title = ''

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

def coralqry_title(*args):
	global title
	title = ' '.join(args)

def coralqry_importdir(*args):
	directory = ' '.join(args)

	if directory[-1] != '/':
		directory += '/'

	for f in os.listdir(directory):
		ext = os.path.splitext(f)[1]
		if ext == '.xlsx':
			coralqry_import(directory + f)

builtins = {'exit': coralqry_exit,
			'opendb': coralqry_opendb,
			'import': coralqry_import,
			'importdir': coralqry_importdir,
			'title': coralqry_title,
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

	agrra.piechart(qry, title=title, saveas=saveas, interactive=not non_interactive)

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

