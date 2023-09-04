# -*- enconding: utf-8 -*-

import miniC_parser
import sys

if __name__ == '__main__':

	tests = ['prueba.c']
	miniC_parser.VERBOSE = 0

	for test in tests:
		f = open(test, 'r')
		data = f.read()
		print ('test: ' + test + '..............\t')
		try:
			miniC_parser.parser.parse(data, tracking=True)
			print ('[ok]')
		except:
			print ('[ko]')
