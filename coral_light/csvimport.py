import csv, os, re, sqlite3

def scanTypes(fileName):
	types = {}
	with open(fileName) as inputFile:
		reader = csv.DictReader(inputFile)
		for row in reader:
			for key, value in enumerate(row):
				if key not in types:
					types[key] = []
				if re.match(r'[0-9]+\.[0-9]+', value):
					if 'REAL' not in types[key]:
						types[key].append('REAL')
				elif re.match(r'[0-9]+', value):
					if 'INTEGER' not in types[key]:
						types[key].append('INTEGER')
				else:
					if 'TEXT' not in types[key]:
						types[key].append('TEXT')
	result = []

	for field, typeList in enumerate(types):
		if 'TEXT' in typeList:
			result.append((field, 'TEXT'))
		elif 'REAL' in typeList:
			result.append((field, 'REAL'))
		else:
			result.append((field, 'INTEGER'))

	return result

class DB:
	def __init__(self, name):
		pass

	def close(self):
		pass

	def createTable(self, tableName, typeList):
		pass

	def importCSV(self, tableName, fileName):
		pass

