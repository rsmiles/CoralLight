#!/usr/bin/env python3

import agrra
from pprint import pprint

sheets = agrra.load(agrra.DATA_PATH + 'AGRRA Coral Data Entry - Punta Brava.xlsx')
pprint(sheets)
