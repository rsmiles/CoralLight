#!/usr/bin/env python3

import config, csv, os, sys
from openpyxl import Workbook
from openpyxl import load_workbook

DATAMAP_PATH = config.APP_PATH + 'datamap/'
SHEET_DATAMAP = DATAMAP_PATH + 'sheet.csv'
TRANSECT_DATAMAP = DATAMAP_PATH + 'transect.csv'
ENCOUNTER_DATAMAP = DATAMAP_PATH + 'encounter.csv'
sheet_datamap = {}

assert len(sys.argv == 2), 'No data file specified'

DATAFILE = sys.argv[1]

with open(SHEET_DATAMAP) as mapfile:
	reader = csv.DictReader(mapfile)
	for row in reader:
		sheet_datamap[row['key']]=row
		if row['key'] == 'min_row' or row['key'] == 'max_col':
			sheet_datamap[row['key']]['pos'] = int(sheet_datamap[row['key']]['pos']) # convert positional values read to integers

transect_datamap = {}
with open(TRANSECT_DATAMAP) as mapfile:
	reader = csv.DictReader(mapfile)
	for row in reader:
		transect_datamap[row['key']]=row
		transect_datamap[row['key']]['pos']=int(transect_datamap[row['key']]['pos']) # convert positional values read to integers

encounter_datamap = {}
with open(ENCOUNTER_DATAMAP) as mapfile:
	reader = csv.DictReader(mapfile)
	for row in reader:
		encounter_datamap[row['key']]=row
		encounter_datamap[row['key']]['pos']=int(encounter_datamap[row['key']]['pos']) # convert positional values read to integers

wb = None
if os.path.isfile(DATAFILE):
	wb = load_workbook(datafile)
else:
	wb = Workbook()

wb.save(DATAFILE)
