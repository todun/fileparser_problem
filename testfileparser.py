#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest

import fileparser

datadir = 'data'
specsdir = 'specs'
dbname = 'test.db'
DATA_FILE_DELIMITER = '_'
SPEC_FILE_DELIMITER = '.'


class FileParserTests(unittest.TestCase):
    def testlistdirfiles(self):
        """
        test that data directory is not empty
        :return:
        """
        self.failUnless(len(fileparser.listdirfiles(datadir)) is not 0)

    def testrunapp_debugon(self):
        """
        end to end testing of file parser with debug on
        :return:
        """
        self.failUnless(fileparser.runapp(1, None, None, datadir, specsdir, dbname, DATA_FILE_DELIMITER,
                                          SPEC_FILE_DELIMITER) == True)

    def testrunapp_debugoff(self):
        """
        end to end testing of file parser with debug off
        :return:
        """
        self.failUnless(fileparser.runapp(0, None, None, datadir, specsdir, dbname, DATA_FILE_DELIMITER,
                                          SPEC_FILE_DELIMITER) == True)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
