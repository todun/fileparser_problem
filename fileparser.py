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

def dryrun(datadir, specsdir, DATA_FILE_DELIMITER,SPEC_FILE_DELIMITER):
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
		con = None
		try:
			con = lite.connect(':memory:')
			cur = con.cursor()
			with con:
				cur = con.cursor()
				cur.execute(aspeccreatestatement)

				#parse csv and read it into the database#
				creader = csv.reader(open(datacsvfilepath, 'rb'), delimiter=',', quotechar='|')
				t = (creader,)
				for t in creader:
					cur.execute('INSERT INTO ' + tablename +' VALUES (?,?,?)', t )

				cur.execute("SELECT * FROM " + tablename)
				rows = cur.fetchall()
				for row in rows:
					print row

		except lite.Error, e:
			print "Error %s:" % e.args[0]
			sys.exit(1)
		finally:
			if con:
				con.close()


datadir = "data"
specsdir = 'specs'
DATA_FILE_DELIMITER = '_'
SPEC_FILE_DELIMITER = '.'
dryrun(datadir, specsdir, DATA_FILE_DELIMITER,SPEC_FILE_DELIMITER)



# import sqlite3 as lite
# import sys
# con = None
# try:
#     con = lite.connect('test.db')
#     cur = con.cursor()
#     cur.execute('SELECT SQLITE_VERSION()')
#     data = cur.fetchone()
#     print "SQLite version: %s" % data
#     with con:
# 		cur = con.cursor()
# # 		cur.execute("CREATE TABLE Cars(Id INT, Name TEXT, Price INT)")
# # 		cur.execute("INSERT INTO Cars VALUES(1,'Audi',52642)")
# # 		cur.execute("INSERT INTO Cars VALUES(2,'Mercedes',57127)")
# # 		cur.execute("INSERT INTO Cars VALUES(3,'Skoda',9000)")
# # 		cur.execute("INSERT INTO Cars VALUES(4,'Volvo',29000)")
# # 		cur.execute("INSERT INTO Cars VALUES(5,'Bentley',350000)")
# # 		cur.execute("INSERT INTO Cars VALUES(6,'Citroen',21000)")
# # 		cur.execute("INSERT INTO Cars VALUES(7,'Hummer',41400)")
# # 		cur.execute("INSERT INTO Cars VALUES(8,'Volkswagen',21600)")
# 		cur.execute("SELECT * FROM Cars")
# 		rows = cur.fetchall()
# 		for row in rows:
# 			print row
# except lite.Error, e:
#     print "Error %s:" % e.args[0]
#     sys.exit(1)
# finally:
#     if con:
#         con.close()


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



