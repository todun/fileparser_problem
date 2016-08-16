#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os
import re
import sqlite3 as lite
import sys

from helpers import Enumeration as enums


def listdirfiles(dir):
    """
    read spec or data directory

    :param dir: directory name
    :return: list of files in the given directory
    """
    return os.listdir(dir)


def list2map(listoffilenames, delimiter):
    """
    convert a list to a map

    :param listoffilenames: list of filenames
    :param delimiter: common separator used in filenames
    :return: map/dictionary of list with key of filename before delimiter and value of complete filename
    """
    return dict(map(lambda x: [x.split(delimiter)[0], x], listoffilenames))


def mapwithsamekeys(specsfilesmap, datafilesmap):
    """
    map specfilepath with its datafilename.
    Map with same keys

    :param specsfilesmap:
    :param datafilesmap:
    :return:
    """
    specfilepath2datafilepath = {}
    for specsfileformat in specsfilesmap:
        if specsfileformat in datafilesmap:
            specfilepath2datafilepath[specsfileformat] = datafilesmap[specsfileformat]
    return specfilepath2datafilepath


def relativespecpath(specfilename):
    """
    relative spec path

    :param specfilename:
    :return:
    """
    return 'specs/' + specfilename + '.csv'


def relativedatapath(datapath):
    """
    relative data path

    :param datapath:
    :return:
    """
    return 'data/' + datapath


def relativedatacsvpath(datacsvfilename):
    """
    relative data csv path

    :param datacsvfilename:
    :return:
    """
    return 'datacsv/' + datacsvfilename + '.csv'


def supportedsqldatatypes():
    """
    supported sql datatypes
    :return:
    """
    return enums(["BOOLEAN", "TEXT", "INTEGER"])


def sqlconversiontype(pythonvalue, sqldatatype, sqldatatypes):
    """
    sql conversion types

    :param pythonvalue:
    :param sqldatatype:
    :param sqldatatypes:
    :return:
    """
    return {
        sqldatatypes.BOOLEAN: int(pythonvalue) == 1,
        sqldatatypes.TEXT: str(pythonvalue),
        sqldatatypes.INTEGER: int(pythonvalue)
    }.get(pythonvalue, sqldatatype)


def sqlcreatestatement(specfilename, specfilepath):
    """
    make sql create statement from specfiles
    sql create statement

    :param specfilename:
    :param specfilepath:
    :return:
    """
    fileformatcolumnspecs = csv.DictReader(open(specfilepath), skipinitialspace=True)
    headerslist = []
    tablename = specfilename
    sqlcreatestatement = "CREATE TABLE" + " " + specfilename + "("
    for columnspec in fileformatcolumnspecs:
        sqlcreatestatement = sqlcreatestatement + columnspec['column name'] + ' ' + columnspec['datatype'] + '(' + \
                             columnspec['width'] + ')' + ','
        headerslist.append(columnspec['column name'])
    sqlcreatestatement = sqlcreatestatement + ');'
    sqlcreatestatement = sqlcreatestatement.split(',);')[0] + ');'
    return sqlcreatestatement, headerslist, tablename


def datatxt2datacsv(datacsvfilepath, headerslist, datafilepath, sqldatatypes):
    """
    make formated csv data file from text datafile
    given data text to data csv

    :param datacsvfilepath:
    :param headerslist:
    :param datafilepath:
    :param sqldatatypes:
    :return:
    """
    data = open(datafilepath, 'rU')
    datacsv = open(datacsvfilepath, "w")
    csv_out = csv.writer(datacsv)
    result = []
    for line in data:
        parseresult = re.split('(\d)', line)
        boolean = sqlconversiontype(parseresult[1], sqldatatypes.BOOLEAN, sqldatatypes)
        csvresult = (parseresult[0].strip(), boolean, int("".join(parseresult[2:len(parseresult) - 1])))
        csv_out.writerow(csvresult)
        result.append(csvresult)
    return result


def createtableindb(dbconnection, dbcursor, aspeccreatestatement, tablename):
    """
    create table in sql database
    :param dbconnection:
    :param dbcursor:
    :param aspeccreatestatement:
    :param tablename:
    :return:
    """
    with dbconnection:
        dbcursor = dbconnection.cursor()
        dbcursor.execute("DROP TABLE IF EXISTS " + tablename)
        dbcursor.execute(aspeccreatestatement)


def dataloadintodb(dbconnection, dbcursor, datacsvfilepath, tablename):
    """
    data loading into database

    :param dbconnection:
    :param dbcursor:
    :param datacsvfilepath:
    :param tablename:
    :return:
    """
    with dbconnection:
        # parse csv and read it into the database#
        creader = csv.reader(open(datacsvfilepath, 'rb'), delimiter=',', quotechar='|')
        t = (creader,)
        for t in creader:
            dbcursor.execute('INSERT INTO ' + tablename + ' VALUES (?,?,?)', t)


def showdbdata(dbconnection, dbcursor, tablename):
    """
    show database tables

    :param dbconnection:
    :param dbcursor:
    :param tablename:
    :return:
    """
    with dbconnection:
        dbcursor.execute("SELECT * FROM " + tablename)
        rows = dbcursor.fetchall()
        for row in rows:
            print row


def loaddb(isdebug, dbconnection, dbcursor, dbname, aspeccreatestatement, datacsvfilepath, tablename):
    """
    load database with parsed data

    :param isdebug:
    :param dbconnection:
    :param dbcursor:
    :param dbname:
    :param aspeccreatestatement:
    :param datacsvfilepath:
    :param tablename:
    :return:
    """
    isloaded = False
    try:
        dbconnection = lite.connect(dbname)
        dbcursor = dbconnection.cursor()
        createtableindb(dbconnection, dbcursor, aspeccreatestatement, tablename)
        dataloadintodb(dbconnection, dbcursor, datacsvfilepath, tablename)

        if isdebug:
            showdbdata(dbconnection, dbcursor, tablename)

        dbconnection.commit()
        isloaded = True
    except lite.Error, e:
        if dbconnection:
            dbconnection.rollback()

        print "Error %s:" % e.args[0]
        sys.exit(1)
    finally:
        if dbconnection:
            dbconnection.close()
        return isloaded


def runapp(isdebug, dbconnection, dbcursor, datadir, specsdir, dbname, DATA_FILE_DELIMITER, SPEC_FILE_DELIMITER):
    """
    run this app

    :param isdebug:
    :param dbconnection:
    :param dbcursor:
    :param datadir:
    :param specsdir:
    :param dbname:
    :param DATA_FILE_DELIMITER:
    :param SPEC_FILE_DELIMITER:
    :return:
    """
    # 1. map of datafilename to datafilepath
    datafileslist = listdirfiles(datadir);
    datafilesmap = list2map(datafileslist, DATA_FILE_DELIMITER)

    # 2. map of specsfilename to specsfilepath
    specsfileslist = listdirfiles(specsdir);
    specsfilesmap = list2map(specsfileslist, SPEC_FILE_DELIMITER)

    # 3. map specfilepath with its corresponding datafilename
    specfilepathwithdatamap = mapwithsamekeys(specsfilesmap, datafilesmap)

    # 4. get supported sql datatypes
    sqldatatypes = supportedsqldatatypes()

    # 6. parse a specific spec file into a SQL statement create table statement with tablename == spec filename
    for specfilename, datafilename in specfilepathwithdatamap.iteritems():
        specfilepath = relativespecpath(specfilename)
        datafilepath = relativedatapath(datafilename)
        datacsvfilename = datafilename.split('.txt')[0]
        datacsvfilepath = relativedatacsvpath(datacsvfilename)
        # 4. make sql create statement from specfiles
        aspeccreatestatement, headerslist, tablename = sqlcreatestatement(specfilename, specfilepath)

        # 5. make formated csv data file from text datafile
        adatacsv = datatxt2datacsv(datacsvfilepath, headerslist, datafilepath, sqldatatypes)

        # 6. load into db
        isloaded = loaddb(isdebug, dbconnection, dbcursor, dbname, aspeccreatestatement, datacsvfilepath, tablename)

    print 'file parsing and load to SQL database completion status:', isloaded
    return isloaded


def main(argv):
    """
    defines commandline args and transformations
    """
    isdebug = sys.argv[1] == '1'  # 1
    dbconnection = sys.argv[2]  # None
    dbcursor = sys.argv[3]  # None
    datadir = sys.argv[4]  # "data"
    specsdir = sys.argv[5]  # 'specs'
    dbname = sys.argv[6]  # 'test.db'
    DATA_FILE_DELIMITER = sys.argv[7]  # '_'
    SPEC_FILE_DELIMITER = sys.argv[8]  # '.'
    runapp(isdebug, dbconnection, dbcursor, datadir, specsdir, dbname, DATA_FILE_DELIMITER, SPEC_FILE_DELIMITER)


if __name__ == "__main__":
    main(sys.argv[1:])
