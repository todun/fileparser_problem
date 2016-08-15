#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
import fileparser


datadir = 'data'
specsdir = 'specs'
dbname = 'test.db'
DATA_FILE_DELIMITER = '_'
SPEC_FILE_DELIMITER = '.'

# Here's our "unit tests".
class FileParserTests(unittest.TestCase):

	def testlistdirfiles(self):
		self.failUnless( len(fileparser.listdirfiles(datadir)) is not 0 )

	def testrunapp(self):
		self.failUnless( fileparser.runapp(None, None, 'data', 'specs', 'test.db', '_', '.')  == True)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
