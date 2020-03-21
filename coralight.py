#!/usr/bin/env python3

import agrra, os, sys

class CoraLight_State():
    def __init__(self):
        self.query = ''
        self.title = ''
        self.save_as = ''
        self.chart_type = 'pie'
        self.max_y = None
        self.interactive = True

state = CoraLight_State()

if '-n' in sys.argv or '--non-interactive' in sys.argv:
    state.interactive = False

def coralight_exit():
    sys.exit()

def coralight_opendb(*args):
    agrra.open_db(' '.join(args))

def coralight_import(xlsx):
    agrra.import_xlsx(xlsx)

def coralight_saveas(*args):
    global state
    if args == 0:
        state.save_as = ''
    else:
        state.save_as = ' '.join(args)

def coralight_title(*args):
    global state
    state.title = ' '.join(args)

def coralight_importdir(*args):
    directory = ' '.join(args)

    if directory[-1] != '/':
         directory += '/'

    for f in os.listdir(directory):
        ext = os.path.splitext(f)[1]
        if ext == '.xlsx':
            coralight_import(directory + f)

def coralight_chart(arg):
    global state
    state.chart_type = arg

def coralight_ymax(arg):
    global state 
    state.max_y = int(arg)

builtins = {'exit': coralight_exit,
            'opendb': coralight_opendb,
            'import': coralight_import,
            'importdir': coralight_importdir,
            'title': coralight_title,
            'saveas': coralight_saveas,
            'chart': coralight_chart,
            'ymax': coralight_ymax}

def run_command(command):
    return builtins[command[0][1:]](*command[1:])

PROMPT = 'coralight_$: '

def print_prompt():
    global state
    if state.interactive:
        sys.stdout.write(PROMPT)
        sys.stdout.flush()

def exec_qry():
    global state
    agrra.chart(state.query, state.chart_type, title=state.title, saveas=state.save_as, ymax=state.max_y, interactive=state.interactive)
    state.query = ''

print_prompt()

try:
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
                    qry += queries[0]
        print_prompt()

except Exception as ex:
    print(ex)
    if not state.interactive:
        raise ex

print()

