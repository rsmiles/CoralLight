from openpyxl import load_workbook
from config import *
import csv

# agrra.py, by Robert Smiley
# Copyright (c) Global Volunteers International, All Rights Reserved
# Library for loading AGRRA coral transects

metamap = {}
with open(METAMAP) as mapfile:
	reader = csv.DictReader(mapfile)
	for row in reader:
		metamap[row['key']]=row
		if row['key'] == 'min_row' or row['key'] == 'max_col':
			metamap[row['key']]['pos'] = int(metamap[row['key']]['pos']) # convert positional values read to integers

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

def load_sheet(ws):
	data = {}

	data['title'] = ws.title

	for key in metamap:
		if key != 'min_row' and key != 'max_col':
			data[key]=ws[metamap[key]['pos']].value

	data['transects'] = []

	for row in ws.iter_rows(min_row=metamap['min_row']['pos'], max_col=metamap['max_col']['pos']):
		# if we don't have enough transects in our list to store this number, keep adding them until we have enough
		transnum_pos = transect_datamap['transect_#']['pos']
		transnum = row[transnum_pos].value
		if transnum > len(data['transects']):
			i = len(data['transects'])
			while i < transnum:
				data['transects'].append({})
				i += 1

			trans = data['transects'][transnum - 1]

			for key in transect_datamap:
				trans[key] = row[transect_datamap[key]['pos']].value

			trans['encounters'] = []

		enc = {}
		for key in encounter_datamap:
			enc[key] = row[encounter_datamap[key]['pos']].value

		data['transects'][transnum - 1]['encounters'].append(enc)

	return data

def load(xlsx):
	data_sheets = {}
	wb = load_workbook(xlsx)
	for ws in wb:
		data_sheets[ws.title] = load_sheet(ws)
	return data_sheets

