import csv

class NameMap:
	def __init__(self, filename):
		self.map = {}

		with open(filename) as mapfile:
			for row in csv.DictReader(mapfile):
				if row['category'] not in self.map:
					self.map[row['category']] = [(row['field'], row['name'])]
				else:
					self.map[row['category']].append((row['field'], row['name']))

	def getCategories(self):
		return list(self.map.keys())

	def getCategory(self, category):
		return self.map[category]

	def getFields(self, category):
		return [elem[0] for elem in self.map[category]]

	def getNames(self, category):
		return [elem[1] for elem in self.map[category]]

	def getField(self, category, name):
		for elem in self.map[category]:
			if elem[1] == name:
				return elem[0]
		return None

	def getName(self, category, name):
		for elem in self.map[category]:
			if elem[0] == field:
				return elem[1]
		return None

