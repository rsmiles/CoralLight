#!/usr/bin/env python3

import csv, sys

def toFloat(s):
	try:
		return float(s)
	except ValueError:
		return s

reader = csv.reader(sys.stdin)

for line in reader:
	l = len(line)

	s = ','.join([str(toFloat(x)) for x in line])

	print(s)


