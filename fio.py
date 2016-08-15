#!/usr/bin/env python


import os
import csv
import re

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
	sqlcreatestatement = "CREATE TABLE" + " "+specfilename + "("
	for columnspec in fileformatcolumnspecs:
		sqlcreatestatement = sqlcreatestatement + columnspec['column name'] +' '+ columnspec['datatype']+ '('+ columnspec['width'] + ')' + ','
		headerslist.append(columnspec['column name'])
	sqlcreatestatement = sqlcreatestatement  +');'
	sqlcreatestatement = sqlcreatestatement.split(',);')[0] +');'
	return sqlcreatestatement, headerslist

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

def testlist2map():
	datadir = "data"
	specsdir = 'specs'
	DATA_FILE_DELIMITER = '_'
	SPEC_FILE_DELIMITER = '.'
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
		aspeccreatestatement, headerslist = sqlcreatestatement(specfilename, specfilepath)
		print aspeccreatestatement
		#5. make formated csv data file from text datafile
		adatacsv = datatxt2datacsv(datacsvfilepath, headerslist, datafilepath)
		print adatacsv

testlist2map()

# print
# import re
# data = open('data/testformat1_2015-06-28.txt', 'rU')
# datacsv = open('datacsv/testformat1_2015-06-28.csv', "w")
# headers = ['name','valid','count']
# csv_out=csv.writer(datacsv)
# csv_out.writerow(headers)
# for line in data:
# 	parseresult = re.split('(\d)', line)
# 	boolean = (parseresult[1] is '1')
# 	csvresult = (parseresult[0].strip(), boolean, int("".join(parseresult[2:len(parseresult)-1])))
# 	print csvresult
# 	csv_out.writerow(csvresult)
# 	print >> datacsv, csvresult



# 	print >> parseresult[0], boolean, "".join(parseresult[2:len(parseresult)-1])
# 	print >> love, line,

# with open('ur file.csv','w') as out:
#     csv_out=csv.writer(out)
#     csv_out.writerow(['name','num'])
#     for row in data:
#         csv_out.writerow(row)



# import re
# filenames = ['testformat1 _2015-06-28.txt', 'testfo rmat2_2015-06-28.txt']
# a = ''
# b = ''
# c = ''
# for filename in filenames:
# 	m = re.match("\A(\s+)(_)(.*)\Z", filename)
# 	if m:
# 		a = m.group(0)
# 		b = m.group(1)
# 	print a,b,c




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
