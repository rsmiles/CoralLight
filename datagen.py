#!/usr/bin/env python3

import config, csv, os, sys
from datetime import datetime
from openpyxl import Workbook
from openpyxl import load_workbook

assert len(sys.argv) == 2, 'No data file specified'

DATAMAP_PATH = config.APP_PATH + 'datamap/'
SHEET_DATAMAP = DATAMAP_PATH + 'sheet.csv'
TRANSECT_DATAMAP = DATAMAP_PATH + 'transect.csv'
ENCOUNTER_DATAMAP = DATAMAP_PATH + 'encounter.csv'
DATAFILE = sys.argv[1]
NUM_SHEETS = 2

def isSheetEmpty(ws):
	return ws['A1'].value == None

def writeField(ws, dataMap, key, value):
	ws[dataMap[key]['pos']] = value

def createSheet(wb, title):
	global sheet_datamap
	ws = None
	if len(wb.worksheets) == 1:
		if isSheetEmpty(wb.worksheets[0]):
			ws = wb.active
			ws.title = title
		else:
			ws = wb.create_sheet(title=title)
	else:
		ws = wb.create_sheet(title=title)

	sheetTable = {'description': 'AGRRA Coral Data Entry Sheet',
					'version': '5.7: August 2015',
					'copyright': '© Ocean Research & Education Foundation',
					'revision': '2016-05-27',
					'surveyor': 'Test Surveyor',
					'AGRRA_code': 'N/A',
					'site_name': 'Test Site',
					'date': datetime.today().strftime('%d/%m/%Y'),
					'bottom_temp': 28,
					'bottom_temp_units': 'ºC',
					'instrument_type': 'Dive Computer',
					'level': 'detailed'}

	for key in sheetTable:
		writeField(ws, sheet_datamap, key, sheetTable[key])

	return ws

def createTransect():
	pass


sheet_datamap = {}
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
	wb = load_workbook(DATAFILE)
else:
	wb = Workbook()

sheetNum = 1
transectNum = 1

while sheetNum <= NUM_SHEETS:
	sheetTitle = 'Transect {0} + {1}'.format(str(transectNum), str(transectNum + 1))

	ws = createSheet(wb, sheetTitle)

	transectNum += 1
	transectNum += 1
	sheetNum += 1

wb.save(DATAFILE)

