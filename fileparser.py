#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import csv
import re
import sqlite3 as lite
import sys

def listdirfiles(dir):
	"""
	read spec or data directory
	"""
	return os.listdir(dir)

def list2map(filename, delimiter):
	return dict(map(lambda x: [ x.split(delimiter)[0], x], filename))

def mapwithsamekeys(specsfilesmap, datafilesmap):
	"""
	map specfilepath with its datafilename
	"""
	specfilepath2datafilepath = {}
	for specsfileformat in specsfilesmap:
		if specsfileformat in datafilesmap:
			specfilepath2datafilepath[specsfileformat] = datafilesmap[specsfileformat]
	return specfilepath2datafilepath

def relativespecpath(specfilename):
	return 'specs/' + specfilename +'.csv'

def relativedatapath(datapath):
	return 'data/' + datapath

def relativedatacsvpath(datacsvfilename):
	return 'datacsv/' + datacsvfilename +'.csv'

def sqlcreatestatement(specfilename, specfilepath):
	"""
	make sql create statement from specfiles
	"""

	fileformatcolumnspecs = csv.DictReader(open(specfilepath), skipinitialspace=True)
	headerslist = []
	tablename = specfilename
	sqlcreatestatement = "CREATE TABLE" + " "+specfilename + "("
	for columnspec in fileformatcolumnspecs:
		sqlcreatestatement = sqlcreatestatement + columnspec['column name'] +' '+ columnspec['datatype']+ '('+ columnspec['width'] + ')' + ','
		headerslist.append(columnspec['column name'])
	sqlcreatestatement = sqlcreatestatement  +');'
	sqlcreatestatement = sqlcreatestatement.split(',);')[0] +');'
	return sqlcreatestatement, headerslist, tablename

def datatxt2datacsv(datacsvfilepath, headerslist, datafilepath):
	"""
	make formated csv data file from text datafile
	"""
	data = open(datafilepath, 'rU')
	datacsv = open(datacsvfilepath, "w")
	csv_out=csv.writer(datacsv)
	csv_out.writerow(headerslist)
	result = []
	for line in data:
		parseresult = re.split('(\d)', line)
		boolean = (parseresult[1] is '1')
		csvresult = (parseresult[0].strip(), boolean, int("".join(parseresult[2:len(parseresult)-1])))
		csv_out.writerow(csvresult)
		result.append(csvresult)
	return result

def createtableindb(dbconnection, dbcursor, aspeccreatestatement):
	"""
	"""
	with dbconnection:
		dbcursor = dbconnection.cursor()
		dbcursor.execute(aspeccreatestatement)


def dataloadintodb(dbconnection, dbcursor, datacsvfilepath, tablename):
	"""
	"""
	with dbconnection:
		#parse csv and read it into the database#
		creader = csv.reader(open(datacsvfilepath, 'rb'), delimiter=',', quotechar='|')
		t = (creader,)
		for t in creader:
			dbcursor.execute('INSERT INTO ' + tablename +' VALUES (?,?,?)', t )


def showdbdata(dbconnection, dbcursor, tablename):
	"""
	"""
	with dbconnection:

		dbcursor.execute("SELECT * FROM " + tablename)
		rows = dbcursor.fetchall()
		for row in rows:
			print row

def loaddb(dbname, aspeccreatestatement, datacsvfilepath, tablename):
	"""
	"""
	dbconnection = None
	dbconnection = None

	try:
		dbconnection = lite.connect(dbname)
		dbcursor = dbconnection.cursor()
		createtableindb(dbconnection, dbcursor, aspeccreatestatement)
		dataloadintodb(dbconnection, dbcursor, datacsvfilepath, tablename)
		showdbdata(dbconnection, dbcursor, tablename)

	except lite.Error, e:
		print "Error %s:" % e.args[0]
		sys.exit(1)
	finally:
		if dbconnection:
			dbconnection.close()

def dryrun(datadir, specsdir,dbname, DATA_FILE_DELIMITER,SPEC_FILE_DELIMITER):
	print

	#1. map of datafilename to datafilepath
	datafileslist = listdirfiles(datadir) ;
	datafilesmap = list2map(datafileslist, DATA_FILE_DELIMITER)
	print datafilesmap

	#2. map of specsfilename to specsfilepath
	specsfileslist = listdirfiles(specsdir) ;
	specsfilesmap = list2map(specsfileslist, SPEC_FILE_DELIMITER)
	print specsfilesmap

	#3. map specfilepath with its corresponding datafilename
	specfilepathwithdatamap = mapwithsamekeys(specsfilesmap, datafilesmap)
	print specfilepathwithdatamap

	#6. parse a specific spec file into a SQL statement create table statement with tablename == spec filename
	for specfilename, datafilename in specfilepathwithdatamap.iteritems():
		specfilepath = relativespecpath(specfilename)
		datafilepath = relativedatapath(datafilename)
		datacsvfilename = datafilename.split('.txt')[0]
		datacsvfilepath = relativedatacsvpath(datacsvfilename)
		#4. make sql create statement from specfiles
		aspeccreatestatement, headerslist, tablename = sqlcreatestatement(specfilename, specfilepath)
		print aspeccreatestatement
		#5. make formated csv data file from text datafile
		adatacsv = datatxt2datacsv(datacsvfilepath, headerslist, datafilepath)
		print adatacsv

		#6. load into db
		loaddb(dbname, aspeccreatestatement, datacsvfilepath, tablename)


datadir = "data"
specsdir = 'specs'
dbname = ':memory:'
DATA_FILE_DELIMITER = '_'
SPEC_FILE_DELIMITER = '.'
dryrun(datadir, specsdir, dbname, DATA_FILE_DELIMITER,SPEC_FILE_DELIMITER)

# read spec and data directory
# map specfilepath with its datafilename
# make relative path to a specfilepath
# make relative path to a datafilepath
# parse a specific spec file into a SQL statement create table statement with tablename == spec filename
	# make sql create statement from specfiles
	# make formated csv data file from text datafile

# check corresponding data in both directories
# convert datafile text file into proper csv file(anytime there is a number for the valid column, convert it to appropriate boolean)
# parse a data spec file into a SQL insert
# make lazy cache with key corresponding to file-format and value corresponding to path to data value
# check if the directories has changed since last update
# update database with new spec and data entry



