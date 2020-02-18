# agrra.py, by Robert Smiley
# Copyright (c) Global Volunteers International, All Rights Reserved
# Library for loading AGRRA coral transects

from openpyxl import load_workbook
from config import *
from matplotlib import pyplot
import atexit, csv, datetime, os, sqlite3

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

def open_db(name):
	db = sqlite3.connect(name)

	c = db.cursor()

	# Check if table structure has been initialized already. If not, initialize it.
	c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='doc'")
	if not c.fetchone()[0] == 1 :
		with open(DB_INIT) as initfile:
			init = initfile.read()
			for statement in init.split(';'):
				c.execute(statement)

	c.close()
	db.commit()
	return db

db = open_db(DB_PATH + 'agrra.db')
cursor = db.cursor()

def max_id(table):
	cursor.execute('SELECT MAX(' + table + '_id) from ' + table)
	mid = cursor.fetchone()[0]
	if not mid:
		mid = 0
	return mid

def sql_insert(table, params, values):
	values = [str(x) if type(x) == datetime.time else x for x in values]
	params_str = ', '.join(params)
	vals_str = ', '.join(['?' for x in values])
	ins_qry = 'INSERT INTO {0} ({1}) VALUES ({2})'.format(table, params_str, vals_str)
	cursor.execute(ins_qry, values)

def load_doc(xlsx):
	wb = load_workbook(xlsx)
	doc_id = max_id('doc') + 1

	cursor.execute('INSERT INTO doc (doc_id, doc_title) VALUES (?, ?)', [doc_id, os.path.basename(xlsx)])
	for ws in wb:
		sheet_id = str(max_id('sheet') + 1)
		sheet_params = ['sheet_id', 'sheet_title']
		sheet_values = [sheet_id, "'" + ws.title  + "'"]
		for key in sheet_datamap:
			if key != 'min_row' and key != 'max_col':
				sheet_params.append(key)
				sheet_values.append(ws[sheet_datamap[key]['pos']].value)

		sheet_params.append('doc_id')
		sheet_values.append(doc_id)

		sql_insert('sheet', sheet_params, sheet_values)

		trans_id = max_id('transect') + 1
		created_transects = {}
		for row in ws.iter_rows(min_row=sheet_datamap['min_row']['pos'], max_col=sheet_datamap['max_col']['pos']):
			transnum_pos = transect_datamap['transect_num']['pos']
			transnum = row[transnum_pos].value
			if transnum not in created_transects:
				created_transects[transnum] = trans_id
				trans_id += 1
				trans_params = ['transect_id']
				trans_values = [created_transects[transnum]]
				for key in transect_datamap:
					trans_params.append(key)
					trans_values.append(row[transect_datamap[key]['pos']].value)

				trans_params.append('sheet_id')
				trans_values.append(sheet_id)

				sql_insert('transect', trans_params, trans_values)

			enc_id = max_id('encounter') + 1
			enc_params = ['encounter_id']
			enc_values = [enc_id]
			for key in encounter_datamap:
				enc_params.append(key)
				enc_values.append(row[encounter_datamap[key]['pos']].value)
			enc_params.append('transect_id')
			enc_values.append(created_transects[transnum])

			sql_insert('encounter', enc_params, enc_values)

	db.commit()

