#!/usr/bin/env python3

import sys, AGRRA
from pprint import pprint

input_file = sys.argv[1]

data_sheets = AGRRA.load(input_file)

for sheet in data_sheets:
	pprint(data_sheets[sheet])

