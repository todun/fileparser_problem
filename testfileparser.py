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
		self.failUnless( fileparser.listdirfiles(datadir)[1] == 'testformat1_2015-06-28.txt' )


def main():
    unittest.main()

if __name__ == '__main__':
    main()
